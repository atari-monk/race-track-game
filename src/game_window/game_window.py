from typing import Final, Callable
from arcade import View, Window, set_background_color, color, run
from pathlib import Path
from src.main_menu.menu_navigation import MenuNavigation
from src.settings.settings_crud import SettingsCRUD
from src.main_menu.main_menu_view import MainMenu
from src.main_menu.settings_menu_view import SettingsMenu
from src.game_window.game_view import GameView
from src.car.car import Car
from src.track.track import Track

class GameWindow(Window):
    WIDTH: Final[int] = 1024
    HEIGHT: Final[int] = 768
    TITLE: Final[str] = "Racing Track"

    def __init__(self, crud: SettingsCRUD) -> None:
        settings = crud.load()
        super().__init__(self.WIDTH, self.HEIGHT, self.TITLE, resizable=True, fullscreen=settings.fullscreen)
        set_background_color(color.BLACK)
        self._crud = crud

        self._track = Track()
        self._track.resize(self.width, self.height)

        self._car = Car()
        #self._car.state.center_x = self._track._center_x + (track._inner_radius_x + track._outer_radius_x) / 2
        #self._car.state.center_y = self._track._center_y
        self._car.state.heading = self._track.compute_heading_clockwise(self._car.state.center_x, self._car.state.center_y)
        
        factories: dict[str, Callable[[MenuNavigation], View]] = {
            "main_menu": self._main_menu_factory,
            "settings_menu": self._settings_menu_factory,
            "game_view": self._game_view_factory
        }
        self.controller = MenuNavigation(self, factories)
        self.controller.go_to_main_menu()

    def _main_menu_factory(self, controller: MenuNavigation) -> MainMenu:
        return MainMenu(controller)

    def _settings_menu_factory(self, controller: MenuNavigation) -> SettingsMenu:
        return SettingsMenu(controller, self._crud)

    def _game_view_factory(self, controller: MenuNavigation) -> GameView:
        return GameView(self._car, self._track)

    def on_resize(self, width: int, height: int) -> None:
        super().on_resize(width, height)
        self._track.resize(width, height)

if __name__ == "__main__":
    crud = SettingsCRUD(Path('settings.toml'))
    window = GameWindow(crud)
    run()

