
# imports
import requests
from bs4 import BeautifulSoup
import re
import platform
import os
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import subprocess
import time
import queue
from pathlib import Path
from threading import Thread


from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from KeywordQueryEventListener import KeywordQueryEventListener
from ItemEnterEventListener import ItemEnterEventListener


class UlauncherAnime(Extension):
    def __init__(self):
        super(UlauncherAnime, self).__init__()
        self.logger.info("Inializing Extension")
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    """query"""

    def pages(self, url):

        pages = []

        querys = requests.get(url)
        soup = BeautifulSoup(querys.content, "html.parser")
        for link in soup.find_all('a', attrs={'data-page': re.compile("^ *\d[\d ]*$")}):
            pages.append(link.get('data-page'))

        try:
            # return the last item in pages-list to get number of result-pages
            return int(pages[-1])
        except:
            return 1

    links = None

    """global base url"""

    base_url = "https://gogoanime.wiki/"

    def query(self, search_input):

        global links
        links = []
        search_url = self.base_url + "/search.html?keyword=" + search_input

        for i in range(self.pages(search_url)):
            querys = requests.get(search_url + "&page=" + str(i + 1))
            soup = BeautifulSoup(querys.content, "html.parser")

            for link in soup.find_all('a', attrs={'href': re.compile("^/category")}):
                links.append(link.get('href'))

        if not links:
            return None

        # delete double entrys and append to previous list

        temp_list = []
        for i in links:
            if i not in temp_list:
                temp_list.append(i)
            else:
                pass

        links.clear()
        links.extend(temp_list)
        temp_list.clear()

        list_index = 1
        selection = []

        for j in links:
            selection.append(str(j.replace("/category/", "")))

            list_index += 1

        return selection

        # get the right anime

    def select_anime(self, selection):
        which_anime = selection

        try:
            link = links[int(which_anime) - 1]
        except:
            return "error"

        link = self.base_url + link.replace("/", "", 1)

        return link

    def episode(self, url):
        ep_count = []
        querys = requests.get(url)
        soup = BeautifulSoup(querys.content, "html.parser")
        for link in soup.find_all('a', attrs={'ep_end': re.compile("^ *\d[\d ]*$")}):
            ep_count.append(link.get('ep_end'))
            return ep_count[-1]

    def episode_selection(self, url, selection):
        video_url = url.replace("/category", "") + "-episode-" + str(selection)

        return video_url

    def get_urls(self, link_with_episode):
        global embed_url
        embed_url = self.get_embed_url(link_with_episode)

        return self.get_video_url(embed_url)

    """url"""

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
    }

    def get_default_browser(self):

        if platform.system() in ('Linux'):
            program_name = "xdg-mime"
            arguments = ["query", "default"]
            last_argument = ["x-scheme-handler/https"]

            command = [program_name]
            command.extend(arguments)
            command.extend(last_argument)

            output = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]
            return output.decode('utf-8').splitlines()[0]
        else:
            return ""

    def get_embed_url(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        link = soup.find("a", {"href": "#", "rel": "100"})
        if link is None:
            return "episode not found"

        return f'https:{link["data-video"]}'

    def get_video_url(self, embed_url):
        print("Getting video url")

        try:
            try:
                """new code"""
                os.environ['MOZ_HEADLESS'] = '1'
                try:
                    if "chrome" in self.get_default_browser():
                        from webdriver_manager.chrome import ChromeDriverManager

                        browser = webdriver.Chrome(
                            executable_path=ChromeDriverManager().install(), service_log_path=os.devnull)

                    elif "chromium" in self.get_default_browser():
                        from webdriver_manager.chrome import ChromeDriverManager
                        from webdriver_manager.utils import ChromeType

                        browser = webdriver.Chrome(ChromeDriverManager(
                            chrome_type=ChromeType.CHROMIUM).install(), service_log_path=os.devnull)

                    else:
                        print("Defaulting to firefox")
                        from webdriver_manager.firefox import GeckoDriverManager

                        browser = webdriver.Firefox(
                            executable_path=GeckoDriverManager().install(), service_log_path=os.devnull)

                except:
                    return "error"

                if embed_url == "episode not found":
                    return embed_url

                browser.get(embed_url)
                # start the player in browser so the video-url is generated

                browser.execute_script(
                    'document.getElementsByClassName("jw-icon")[2].click()')
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "html.parser")

                # get quality options
                try:
                    user_quality = self.preferences['change_quality']

                    qualitys = soup.find(id="jw-settings-submenu-quality")

                    user_quality = self.quality(qualitys, user_quality)
                    # Click the quality, the user picked, in the quality selection, so the right link is being generated.
                    browser.execute_script(
                        "document.evaluate('//*[@id=\"jw-settings-submenu-quality\"]/div/button[{0}]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
                        .format(user_quality + 1))
                except:
                    print(
                        "Something went wrong with the quality selection. Loading default quality."
                    )
                    return "error"
                # extract video link
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "html.parser")
                link = soup.find("video")
                link = link.get('src')
                browser.quit()
            except KeyboardInterrupt:
                browser.quit()

        except Exception as e:
            print(e)
            return "error"

        return link

    def quality(self, html_code, quality):

        if quality == None:
            quality = "best"
        else:
            pass

        try:

            qualitys = re.findall(r'\d+ P', str(html_code))

            temp_list = []
            for i in qualitys:
                if i not in temp_list:
                    temp_list.append(i)
                else:
                    pass
            qualitys.clear()
            qualitys.extend(temp_list)

            for i in range(len(qualitys)):
                qualitys[i] = qualitys[i].replace(" P", "")

            if quality == "best" or quality == "worst":
                if quality == "best":
                    quality = qualitys.index(qualitys[-1])
                else:
                    quality = qualitys.index(qualitys[0])
            else:
                print(qualitys)
                print(quality)
                if quality in qualitys:
                    quality = qualitys.index(quality)
                else:
                    quality = qualitys.index(qualitys[-1])
                    print("Your quality is not avalible using: " +
                          qualitys[quality] + "p")
                    time.sleep(1.5)
                    pass

        except:

            pass

        return quality

    def play(self, embed_url, video_url, link, start_at="0"):
        player = "mpv"
        player_command = player + f" --force-media-title={link.replace(self.base_url, '')} " + f" --start=+{str(start_at)}" + \
            " --cache=yes " + \
            f'--http-header-fields="Referer: {embed_url}" ' + f"'{video_url}'"
        try:
            sub_proc = subprocess.Popen(player_command,
                                        stdout=subprocess.PIPE,
                                        shell=True,
                                        preexec_fn=os.setsid,
                                        stderr=subprocess.DEVNULL)

        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return "error"

        Thread(target=self.write_history, args=(link,)).start()

        return "Success"

    """History"""

    done_writing_queue = queue.Queue()
    history_folder_path = Path(Path(__file__).parent) / "history"
    history_file_path = history_folder_path / "history.txt"

    def write_history(self, link):

        # Make the history folder and file if they doesn't exist
        try:
            self.history_folder_path.mkdir(parents=True, exist_ok=True)
            self.history_file_path.touch(exist_ok=True)
        except PermissionError:
            print(
                "Unable to write/read to where history file is suposed to be due to permissions.")
            return "error"

        with self.history_file_path.open('r') as history_file:
            data = history_file.readlines()

        index = 0
        in_data = False

        for i in data:
            anime = link.rsplit("-", 1)[0]
            if anime in i:
                index = index
                in_data = True
                break
            else:
                pass

            index += 1

        if in_data == True:
            ep = link.rsplit("-", 1)[1].replace("-", "")
            episode = int(ep) + 1

            next_episode = anime + "-" + str(episode) + "\n"
            data[index] = ""
            data.append(next_episode)
            data.reverse()
            with self.history_file_path.open('w') as history_file:
                for element in data:
                    history_file.write(element)
        else:
            with self.history_file_path.open('a') as history_file:
                link.reverse()
                history_file.write(link + "\n")

        self.done_writing_queue.put(True)

    def read_history(self):
        while True:
            check = self.done_writing_queue.get()
            if check == True:
                break
            time.sleep(0.2)

        try:
            with self.history_file_path.open('r') as history_file:
                data = history_file.readlines()
                links = []
                resume_seconds = []

            for i in data:
                links.append(i)

        except:
            pass

        return links, resume_seconds

    def pick_history(self):

        # read history and reverse lists so last history-point is first in selection
        history = self.read_history()
        links = history[0]

        if not links:
            return "error"
        animes = []
        for i in links:
            animes.append(i.rstrip())

        return animes


if __name__ == '__main__':
    UlauncherAnime().run()
