from pathlib import Path
from arcade import View, draw_text, key, get_window
from src.settings.settings_crud import SettingsCRUD
from src.settings.settings import Settings

class SettingsMenuView(View):
    def __init__(self) -> None:
        super().__init__()
        self.options = ['Fullscreen', 'Back']
        self.selected_index = 0
        self.crud = SettingsCRUD(Path('settings.toml'))
        self.settings = self.crud.load()

    def on_draw(self) -> None:
        self.clear()
        w, h = get_window().width, get_window().height
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_index
            color = (255, 255, 0) if is_selected else (255, 255, 255)
            label = f"{option}: {'On' if self.settings.fullscreen else 'Off'}" if option == 'Fullscreen' else option
            draw_text(label, w // 2, h // 2 - i * 40, color, 24, anchor_x='center')

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in (key.UP, key.W):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif symbol in (key.DOWN, key.S):
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif symbol in (key.ENTER, key.RETURN, key.SPACE):
            option = self.options[self.selected_index]
            if option == 'Fullscreen':
                self.settings = Settings(fullscreen=not self.settings.fullscreen)
                self.crud.save(self.settings)
                get_window().set_fullscreen(self.settings.fullscreen)
            elif option == 'Back':
                # self.window.show_view(MainMenuView())
                pass

if __name__ == '__main__':
    import arcade

    window = arcade.Window(800, 600, 'Settings Menu')
    view = SettingsMenuView()
    window.show_view(view)
    arcade.run()

