from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):

        args = event.get_argument()
        print(args)

        if args is not None:
            return RenderResultListAction([ExtensionResultItem(icon="images/icon.png", name="Searching: "+args, description="Enter anime to watch",
                                                               on_enter=ExtensionCustomAction({"action": "name", "search": args}, keep_app_open=True))])
        return extension.render_main_page(None)
