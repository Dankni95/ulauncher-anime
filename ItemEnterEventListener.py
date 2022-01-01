from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):

        data = event.get_data()
        extension.logger.debug(str(data))

        if data["action"] == "episode":
            url = data["url"]
            episode_link = extension.episode_selection(
                url, data["number"])
            video_url = extension.get_urls(episode_link)
            if video_url == "error":
                return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="Unexpected error", description="Feel free to open a Issue on github: https://github.com/dankni95/ulauncher-anime/issues",
                                                                   on_enter=DoNothingAction())])

            message = extension.play(url, video_url, episode_link)
            """find a way to close ulauncher when anime loads"""
