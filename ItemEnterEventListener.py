from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from threading import Thread


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):

        data = event.get_data()
        extension.logger.debug(str(data))

        if data["action"] == "episode":
            url = data["data"]
            episode_link = extension.episode_selection(
                url, data["number"])

            video_url = extension.get_urls(episode_link)

            if video_url == "error":
                return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="Unexpected error", description="Feel free to open a Issue on github: https://github.com/dankni95/ulauncher-anime/issues",
                                                                   on_enter=DoNothingAction())])

            Thread(target=extension.play, args=(
                url, video_url, episode_link,)).start()

        if data["action"] == "history":
            data = data["data"]
            anime = data.split("-episode-")

            temp_url = str(anime[0]).rstrip().replace(" ", "")
            url = extension.base_url + "category/" + \
                temp_url.split(extension.base_url)[1]

            episode_link = extension.episode_selection(
                url, anime[1])

            video_url = extension.get_urls(episode_link)

            if video_url == "error":
                return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="Unexpected error", description="Feel free to open a Issue on github: https://github.com/dankni95/ulauncher-anime/issues",
                                                                   on_enter=DoNothingAction())])
            if video_url == "episode not found":
                return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="Episode not found", description="The episode is probably not out yet",
                                                                   on_enter=DoNothingAction())])

            Thread(target=extension.play, args=(
                url, video_url, episode_link,)).start()

        """find a way to close ulauncher when anime loads"""
