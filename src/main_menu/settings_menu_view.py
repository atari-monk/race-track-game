from arcade import View, draw_text, key, get_window
from src.main_menu.menu_navigation import NavigationController
from src.settings.settings import Settings
from src.settings.settings_crud import SettingsCRUD

class SettingsMenu(View):
    def __init__(self, controller: NavigationController, crud: SettingsCRUD) -> None:
        super().__init__()
        self.options: list[str] = ['Fullscreen', 'Back']
        self.selected_index: int = 0
        self.crud: SettingsCRUD = crud
        self.settings: Settings = self.crud.load()
        self.controller: NavigationController = controller

    def on_draw(self) -> None:
        self.clear()
        w: int = get_window().width
        h: int = get_window().height
        for i, option in enumerate(self.options):
            color: tuple[int, int, int] = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            label: str = f"{option}: {'On' if self.settings.fullscreen else 'Off'}" if option == 'Fullscreen' else option
            draw_text(label, w // 2, h // 2 - i * 40, color, 24, anchor_x='center')

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in (key.UP, key.W):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif symbol in (key.DOWN, key.S):
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif symbol in (key.ENTER, key.RETURN, key.SPACE):
            option: str = self.options[self.selected_index]
            if option == 'Fullscreen':
                self.settings = Settings(fullscreen=not self.settings.fullscreen)
                self.crud.save(self.settings)
                get_window().set_fullscreen(self.settings.fullscreen)
            elif option == 'Back':
                self.controller.go_to_main_menu()

