from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from threading import Thread


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):

        args = event.get_argument()
        global link
        global count
        count = 0
        if str(args) == "type episode nr >":
            args = "type episode nr > 0"

        if "s " in str(args):
            anime = str(args).replace("s ", "")
            link = extension.query(anime)
            animes = []
            if link is None:
                animes.append(ExtensionResultItem(icon="images/icon.png", name="No anime found by this name", description="Please search again",
                                                       on_enter=DoNothingAction()))
            else:
                animes.append(ExtensionResultItem(icon="images/icon.png", name=link[0].replace(extension.base_url, "").replace("-", " ").capitalize(), description="Select anime",
                                                  on_enter=SetUserQueryAction("ani type episode nr > ")))
            return RenderResultListAction(animes)

        elif str(args).startswith("type episode nr > ") and str(args)[-1].isdigit():
            if str(args) == "type episode nr > 0":
                selection = str(args).replace("type episode nr > 0", "")
                selection = 0

            else:
                selection = str(args).replace("type episode nr > ", "")

            url = extension.select_anime(1)
            episodes = extension.episode(url)

            animes = []
            if episodes is None or episodes == "not found":
                animes.append(ExtensionResultItem(icon="images/icon.png", name="Not found or not out yet", description="Please search again",
                                                       on_enter=DoNothingAction()))
            else:
                for ep in range(0, int(episodes)):
                    count += 1
                    if count >= int(selection):
                        animes.append(ExtensionSmallResultItem(icon="images/icon.png", name="Episode "+str(count),
                                                               on_enter=ExtensionCustomAction({"action": "episode", "number": count, "data": url}, keep_app_open=True)))
            return RenderResultListAction(animes)

        elif str(args) == "h":
            extension.done_writing_queue.put(True)
            picked_history = extension.pick_history()
            
            if str(picked_history) == "error" or str(picked_history) == "empty history" :
                return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="No history found or unexpected error", description="Feel free to open a Issue on github: https://github.com/dankni95/ulauncher-anime/issues",
                                                                   on_enter=DoNothingAction())])

            animes = []
            count = 1
            for picked in picked_history:
                anime = str(picked.replace(extension.base_url, "").replace("-", " ")).rstrip()
                if count == 1:
                    animes.append(ExtensionResultItem(icon="images/icon.png", name="Next episode: "+anime,
                                                      on_enter=ExtensionCustomAction({"action": "history", "data": picked}, keep_app_open=True)))
                else:
                    animes.append(ExtensionSmallResultItem(icon="images/icon.png", name="Next episode: "+anime,
                                                           on_enter=ExtensionCustomAction({"action": "history", "data": picked}, keep_app_open=True)))
                count += 1
            return RenderResultListAction(animes)

        else:
            return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="Type s your anime", description="uLauncher anime",
                                                                    on_enter=DoNothingAction())])
