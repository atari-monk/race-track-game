import arcade
from src.draft.polygon_generator.track_data import TrackData

class TrackViewer(arcade.Window):
    def __init__(self, track_data: TrackData):
        super().__init__(fullscreen=True)
        self.track_data = track_data
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.draw_polygon_filled(self.track_data.outer_points, arcade.color.DARK_SLATE_GRAY)
        arcade.draw_polygon_filled(self.track_data.inner_points, arcade.color.BLACK)
        arcade.draw_line_strip(self.track_data.spline_points, arcade.color.RED, 2)
