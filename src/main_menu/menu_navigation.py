from arcade import Window, View
from typing import Callable

class MenuNavigation:
    def __init__(
        self,
        window: Window,
        factories: dict[str, Callable[['MenuNavigation'], View]]
    ) -> None:
        self.window = window
        self._factories = factories
        self._views: dict[str, View] = {}

    def go_to(self, view_name: str, reuse: bool = True) -> None:
        if reuse and view_name in self._views:
            self.window.show_view(self._views[view_name])
        else:
            view = self._factories[view_name](self)
            self._views[view_name] = view
            self.window.show_view(view)

    def go_to_main_menu(self, reuse: bool = True) -> None:
        self.go_to("main_menu", reuse)

    def go_to_settings(self, reuse: bool = True) -> None:
        self.go_to("settings_menu", reuse)

    def go_to_game(self, reuse: bool = True) -> None:
        self.go_to("game_view", reuse)

