
# imports
import subprocess as sp
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


from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent, PreferencesUpdateEvent
from KeywordQueryEventListener import KeywordQueryEventListener
from ItemEnterEventListener import ItemEnterEventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction


class PlayerMain(Extension):
    def __init__(self):
        super(PlayerMain, self).__init__()
        self.logger.info("Inializing Extension")
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def render_main_page(self, action):
        print("main page")
        theme = self.preferences['change_icon_theme']
        animes = []
        print(action)
        if action is None:
            animes.append(ExtensionResultItem(icon="images/icon.png", name="Ulauncher anime", description="Keep typing to search anime",
                                              on_enter=DoNothingAction()))
        if action == "error":
            animes.append(ExtensionResultItem(icon="images/icon.png", name="Unexpected error", description="feel free to open a Issue on github: https://github.com/sdaqo/anipy-cli/issues",
                                              on_enter=DoNothingAction()))
        if action == "webdriver error":
            animes.append(ExtensionResultItem(icon="images/icon.png", name="Webdriver error", description="Did you install dependencies? : https://github.com/sdaqo/anipy-cli/issues",
                                              on_enter=DoNothingAction()))
        if action == "close ulauncher":
            return RenderResultListAction(None)
        
        

        return RenderResultListAction(animes)

    """query"""

    def pages(self, url):

        pages = []

        querys = requests.get(url)
        print(querys)
        soup = BeautifulSoup(querys.content, "html.parser")
        for link in soup.find_all('a', attrs={'data-page': re.compile("^ *\d[\d ]*$")}):
            pages.append(link.get('data-page'))

        try:
            # return the last item in pages-list to get number of result-pages
            return int(pages[-1])
        except:
            return 1

    links = None

    def query(self, search_input):
        global base_url

        """global base url"""

        base_url = "https://gogoanime.wiki/"
        global links
        links = []
        search_url = base_url + "/search.html?keyword=" + search_input

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
            selection.append("[" + str(list_index) + "]" +
                             " " + str(j.replace("/category/", "")))

            list_index += 1

        return selection

        # get the right anime

    def select_anime(self, selection):
        which_anime = selection

        try:
            link = links[int(which_anime) - 1]
        except:
            self.render_main_page("error")

        link = base_url + link.replace("/", "", 1)

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

    os.environ['WDM_LOG_LEVEL'] = '0'

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
                    self.render_main_page("webdriver error")

                browser.get(embed_url)
                # start the player in browser so the video-url is generated

                browser.execute_script(
                    'document.getElementsByClassName("jw-icon")[2].click()')
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "html.parser")
                # get quality options
                """skipped"""
                # extract video link
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "html.parser")
                link = soup.find("video")
                link = link.get('src')
                browser.quit()
            except KeyboardInterrupt:
                browser.quit()

        except Exception as e:
            try:
                browser.quit()
            except:
                pass

            self.render_main_page("error")

        return link

    def play(self, embed_url, video_url, link, start_at="0"):
        player = "mpv"
        player_command = player + f" --force-media-title={link.replace(base_url, '')} " + f" --start=+{str(start_at)}" + \
            " --cache=yes " + \
            f'--http-header-fields="Referer: {embed_url}" ' + f"'{video_url}'"
        try:
            sp.Popen(player_command,
                     stdout=sp.PIPE,
                     shell=True,
                     preexec_fn=os.setsid,
                     stderr=sp.DEVNULL)

        except sp.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            self.render_main_page("error")
            return "error"

        return "Success"


if __name__ == '__main__':
    PlayerMain().run()
