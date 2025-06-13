from arcade import View, draw_text, key, Window
from arcade.gui import UIManager
from typing import List

class MainMenuView(View):
    def __init__(self) -> None:
        super().__init__()
        self.options: List[str] = ['Start Game', 'Settings', 'Exit']
        self.selected_index: int = 0
        self.ui: UIManager = UIManager()
        self.window: Window

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self) -> None:
        self.clear()
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            draw_text(
                option,
                self.window.width // 2,
                self.window.height // 2 - i * 40,
                color,
                20,
                anchor_x="center"
            )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif symbol == key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif symbol == key.RETURN or symbol == key.ENTER:
            selected_option = self.options[self.selected_index]
            if selected_option == 'Exit':
                self.window.close()

if __name__ == '__main__':
    import arcade

    window = arcade.Window(800, 600, "Race Track Game")
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()

