from typing import Final
from arcade import View, color, set_background_color
from src.track.track import Track
from src.car.car import Car

class GameView(View):
    _car: Final[Car]
    _track: Final[Track]

    def __init__(self, car: Car, track: Track) -> None:
        super().__init__()
        self._car = car
        self._track = track

    def on_show_view(self) -> None:
        set_background_color(color.BLACK)
    def on_draw(self) -> None:
        self.clear()
        self._track.draw()
        self._car.draw()

    def on_update(self, delta_time: float) -> None:
        self._car.update()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._car.on_key_press(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self._car.on_key_release(symbol)
