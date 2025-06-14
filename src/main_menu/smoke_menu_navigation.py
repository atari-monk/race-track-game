import arcade
from pathlib import Path
from src.main_menu.main_menu_view import MainMenuView
from src.main_menu.settings_menu_view import SettingsMenu
from src.main_menu.menu_navigation import NavigationController
from src.settings.settings_crud import SettingsCRUD

def main_menu_factory(controller: NavigationController) -> MainMenuView:
    return MainMenuView(controller)

def settings_menu_factory(controller: NavigationController) -> SettingsMenu:
    path = Path('settings.toml')
    crud = SettingsCRUD(path)
    return SettingsMenu(controller, crud)

if __name__ == '__main__':
    window = arcade.Window(800, 600, "Race Track Game")
    controller = NavigationController(window, main_menu_factory, settings_menu_factory)
    controller.go_to_main_menu()
    arcade.run()
