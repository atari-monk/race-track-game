from arcade import View, color, set_background_color
#from arcade import draw_text

class GameView(View):
    def on_show_view(self) -> None:
        set_background_color(color.GREEN)

    def on_draw(self) -> None:
        self.clear()

