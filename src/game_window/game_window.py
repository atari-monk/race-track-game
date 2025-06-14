from typing import Final
from arcade import Window, set_background_color, color, run
from pathlib import Path
from src.settings.settings_crud import SettingsCRUD
from src.main_menu.menu_navigation import NavigationController
from src.main_menu.main_menu_view import MainMenuView
from src.main_menu.settings_menu_view import SettingsMenu

class GameWindow(Window):
    WIDTH: Final[int] = 1024
    HEIGHT: Final[int] = 768
    TITLE: Final[str] = "Racing Track"

    def __init__(self, crud: SettingsCRUD) -> None:
        settings = crud.load()
        super().__init__(self.WIDTH, self.HEIGHT, self.TITLE, resizable=True, fullscreen=settings.fullscreen)
        set_background_color(color.BLACK)
        self._crud = crud
        controller = NavigationController(self, self._main_menu_factory, self._settings_menu_factory)
        controller.go_to_main_menu()

    def _main_menu_factory(self, controller: NavigationController) -> MainMenuView:
        return MainMenuView(controller)

    def _settings_menu_factory(self, controller: NavigationController) -> SettingsMenu:
        return SettingsMenu(controller, self._crud)

if __name__ == "__main__":
    crud = SettingsCRUD(Path('settings.toml'))
    window = GameWindow(crud)
    run()

