from arcade import View, color, set_background_color
from src.car.car import Car

class GameView(View):
    def __init__(self, car: Car) -> None:
        super().__init__()
        self._car = car

    def on_show_view(self) -> None:
        set_background_color(color.BLACK)

    def on_draw(self) -> None:
        self.clear()
        self._car.draw() # type: ignore

    def on_update(self, delta_time: float) -> None:
        self._car.update()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._car.on_key_press(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self._car.on_key_release(symbol)
