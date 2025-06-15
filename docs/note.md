# Note

## draw_rect_filled, XYWH

def draw(self) -> None:
    rect = arcade.XYWH(self.center_x,
        self.center_y,
        self.WIDTH,
        self.LENGTH)
    arcade.draw_rect_filled(
        rect,
        arcade.color.RED,
        self.angle
    )
        