import arcade
from src.draft.polygon_generator.track_collision import TrackCollision
from src.draft.polygon_generator.track_generator import TrackGenerator
from src.draft.polygon_generator.track_viewer import TrackViewer

def main():
    screen_width, screen_height = arcade.get_display_size()
    
    generator = TrackGenerator(screen_width, screen_height)
    track_data = generator.track_data
    
    _track_collision = TrackCollision(track_data)

    _viewer = TrackViewer(track_data)
    arcade.run()

if __name__ == "__main__":
    main()