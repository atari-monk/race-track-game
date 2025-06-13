from arcade import Window
from src.main_menu.main_menu_view import MainMenuView
from src.main_menu.settings_menu_view import SettingsMenuView

class NavigationController:
    def __init__(self, window: Window) -> None:
        self.window = window
        self._main_menu_view: MainMenuView | None = None
        self._settings_menu_view: SettingsMenuView | None = None

    def go_to_main_menu(self, reuse: bool = False) -> None:
        if reuse:
            if not self._main_menu_view:
                self._main_menu_view = MainMenuView()
            self.window.show_view(self._main_menu_view)
        else:
            self.window.show_view(MainMenuView())

    def go_to_settings(self, reuse: bool = False) -> None:
        if reuse:
            if not self._settings_menu_view:
                self._settings_menu_view = SettingsMenuView()
            self.window.show_view(self._settings_menu_view)
        else:
            self.window.show_view(SettingsMenuView())

if __name__ == '__main__':
    import arcade

    window = arcade.Window(800, 600, "Race Track Game")
    controller = NavigationController(window)
    controller.go_to_main_menu()
    arcade.run()
