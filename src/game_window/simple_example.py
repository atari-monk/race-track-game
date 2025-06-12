from arcade import Window, run, set_background_color, color, Text
from typing import Final

class GameWindow(Window):
    WIDTH: Final[int] = 1024
    HEIGHT: Final[int] = 768
    TITLE: Final[str] = "Racing Track"

    def __init__(self) -> None:
        super().__init__(self.WIDTH, self.HEIGHT, self.TITLE, resizable=True)
        self.set_fullscreen(False)
        set_background_color(color.BLACK)
        self.text = Text("test", self.width // 2, self.height // 2, color.WHITE, 24, anchor_x="center", anchor_y="center")

    def on_draw(self) -> None:
        self.clear()
        self.text.x = self.width // 2
        self.text.y = self.height // 2
        self.text.draw()


if __name__ == "__main__":
    window = GameWindow()
    run()
