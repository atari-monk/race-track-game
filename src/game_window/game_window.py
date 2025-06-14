from typing import Final
from arcade import Window, set_background_color, color, run
from src.main_menu.menu_navigation import NavigationController
from src.main_menu.main_menu_view import MainMenuView
from src.main_menu.settings_menu_view import SettingsMenuView

class GameWindow(Window):
    WIDTH: Final[int] = 1024
    HEIGHT: Final[int] = 768
    TITLE: Final[str] = "Racing Track"

    def __init__(self) -> None:
        super().__init__(self.WIDTH, self.HEIGHT, self.TITLE, resizable=True)
        self.set_fullscreen(False)
        set_background_color(color.BLACK)
        controller = NavigationController(self, self._main_menu_factory, self._settings_menu_factory)
        controller.go_to_main_menu()

    def _main_menu_factory(self, controller: NavigationController) -> MainMenuView:
        return MainMenuView(controller)

    def _settings_menu_factory(self, controller: NavigationController) -> SettingsMenuView:
        return SettingsMenuView(controller)

if __name__ == "__main__":
    window = GameWindow()
    run()
