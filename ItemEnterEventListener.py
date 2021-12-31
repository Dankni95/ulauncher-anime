from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.action.ActionList import ActionList


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):

        data = event.get_data()
        extension.logger.debug(str(data))

        if data["action"] == "name":
            link = extension.query(data["search"])
            animes = []
            count = 0
            if link is None:
                animes.append(ExtensionResultItem(icon="images/icon.png", name="No anime found", description="Please search again",
                                                  on_enter=ExtensionCustomAction({"action": "error", "number": count}, keep_app_open=True)))
            else:
                for anime in link:
                    count += 1
                    animes.append(ExtensionResultItem(icon="images/icon.png", name=anime, description="Select anime",
                                                      on_enter=ExtensionCustomAction({"action": "anime", "number": count}, keep_app_open=True)))
            return RenderResultListAction(animes)

        if data["action"] == "anime":
            url = extension.select_anime(data["number"])
            episodes = extension.episode(url)
            
            """not enough space for all episodes :/"""

            animes = []
            count = 0
            if episodes is None:
                animes.append(ExtensionSmallResultItem(icon="images/icon.png", name="No episodes found", description="Please search again",
                                                       on_enter=ExtensionCustomAction({"action": "error", "number": count}, keep_app_open=True)))
            else:
                for ep in range(0, int(episodes)):
                    count += 1
                    animes.append(ExtensionResultItem(icon="images/icon.png", name="Episode "+str(count),
                                                      on_enter=ExtensionCustomAction({"action": "episode", "number": count, "url": url}, keep_app_open=True)))
            return RenderResultListAction(animes)

        if data["action"] == "episode":
            url = data["url"]
            episode_link = extension.episode_selection(
                url, data["number"])
            video_url = extension.get_urls(episode_link)
            message = extension.play(url, video_url, episode_link)
            """find a way to close ulauncher when anime loads"""
