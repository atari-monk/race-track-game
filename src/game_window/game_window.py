# File: C:\atari-monk\code\race-track-game\src\game_window\game_window.py
from typing import Final
from arcade import Window, set_background_color, color, run
from src.main_menu.main_menu_view import MainMenuView

class GameWindow(Window):
    WIDTH: Final[int] = 1024
    HEIGHT: Final[int] = 768
    TITLE: Final[str] = "Racing Track"

    def __init__(self) -> None:
        super().__init__(self.WIDTH, self.HEIGHT, self.TITLE, resizable=True)
        self.set_fullscreen(False)
        set_background_color(color.BLACK)

if __name__ == "__main__":
    window = GameWindow()
    window.show_view(MainMenuView())
    run()

