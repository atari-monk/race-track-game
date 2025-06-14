import arcade
from src.main_menu.main_menu_view import MainMenuView
from src.main_menu.settings_menu_view import SettingsMenuView
from src.main_menu.menu_navigation import NavigationController

def main_menu_factory(controller: NavigationController) -> MainMenuView:
    return MainMenuView(controller)

def settings_menu_factory(controller: NavigationController) -> SettingsMenuView:
    return SettingsMenuView(controller)

if __name__ == '__main__':
    window = arcade.Window(800, 600, "Race Track Game")
    controller = NavigationController(window, main_menu_factory, settings_menu_factory)
    controller.go_to_main_menu()
    arcade.run()
