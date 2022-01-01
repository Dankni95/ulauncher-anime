from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem


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
                animes.append(ExtensionResultItem(icon="images/icon.png", name=link[0], description="Select anime",
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
            if episodes is None:
                animes.append(ExtensionResultItem(icon="images/icon.png", name="No episodes found", description="Please search again",
                                                       on_enter=DoNothingAction()))
            else:
                for ep in range(0, int(episodes)):
                    count += 1
                    if count >= int(selection):
                        animes.append(ExtensionSmallResultItem(icon="images/icon.png", name="Episode "+str(count),
                                                               on_enter=ExtensionCustomAction({"action": "episode", "number": count, "url": url}, keep_app_open=True)))
            return RenderResultListAction(animes)
        else:
            return RenderResultListAction([ExtensionSmallResultItem(icon="images/icon.png", name="Type s your anime", description="uLauncher anime",
                                                                    on_enter=DoNothingAction())])
