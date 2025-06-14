from arcade import View, draw_text, key, Window
from arcade.gui import UIManager
from typing import List
from src.main_menu.menu_navigation import MenuNavigation

class MainMenu(View):
    def __init__(self, controller: MenuNavigation) -> None:
        super().__init__()
        self.options: List[str] = ['Start Game', 'Settings', 'Exit']
        self.selected_index = 0
        self.ui = UIManager()
        self.window: Window
        self.controller = controller

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self) -> None:
        self.clear()
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            draw_text(option, self.window.width // 2, self.window.height // 2 - i * 40, color, 20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif symbol == key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif symbol in (key.RETURN, key.ENTER):
            selected = self.options[self.selected_index]
            if selected == 'Exit':
                self.window.close()
            elif selected == 'Settings':
                self.controller.go_to_settings()
            elif selected == 'Start Game':
                self.controller.go_to_game()

