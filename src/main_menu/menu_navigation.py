from arcade import Window, View
from typing import Callable, Optional

class NavigationController:
    def __init__(
        self,
        window: Window,
        main_menu_factory: Callable[['NavigationController'], View],
        settings_menu_factory: Callable[['NavigationController'], View]
    ) -> None:
        self.window = window
        self._main_menu_factory = main_menu_factory
        self._settings_menu_factory = settings_menu_factory
        self._main_menu_view: Optional[View] = None
        self._settings_menu_view: Optional[View] = None

    def go_to_main_menu(self, reuse: bool = True) -> None:
        if reuse and self._main_menu_view:
            self.window.show_view(self._main_menu_view)
        else:
            self._main_menu_view = self._main_menu_factory(self)
            self.window.show_view(self._main_menu_view)

    def go_to_settings(self, reuse: bool = True) -> None:
        if reuse and self._settings_menu_view:
            self.window.show_view(self._settings_menu_view)
        else:
            self._settings_menu_view = self._settings_menu_factory(self)
            self.window.show_view(self._settings_menu_view)
