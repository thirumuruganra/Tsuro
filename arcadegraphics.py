import arcade
import arcade.color
import math


# Simple mouse event object compatible with classes.py expectations
class _MouseEvent:
    def __init__(self, button):
        # Use string names similar to cs110graphics
        self._button = button
        self._x = None
        self._y = None

    def get_button(self):
        # Map arcade button constants to string names if necessary
        return self._button
    def get_mouse_location(self):
        return (self._x, self._y)

    def _set_mouse_location(self, x, y):
        self._x = x
        self._y = y


def _resolve_color(color):
    """Resolve a color name or tuple used in the original code into an
    arcade color. Accepts '', color name string, or an (r,g,b) tuple.
    """
    if not color:
        return None
    if isinstance(color, tuple) and len(color) in (3, 4):
        return color
    if isinstance(color, str):
        # try hex (with or without leading '#')
        if color.startswith('#') or all(c in '0123456789abcdefABCDEF' for c in color):
            hex_str = color if color.startswith('#') else f'#{color}'
            try:
                return arcade.color_from_hex_string(hex_str)
            except Exception:
                return arcade.color.WHITE
        # try attribute on arcade.color
        try:
            return getattr(arcade.color, color.upper())
        except Exception:
            return arcade.color.WHITE
    return color


def _map_button(button):
    """Map arcade mouse button constant (int) to cs110graphics-like
    string names used by the game code.
    Accept common arcade mouse constants; if a string is passed through,
    return it unchanged.
    """
    try:
        # If caller already passed a string (some code paths), return it
        if isinstance(button, str):
            return button
        # arcade constants: arcade.MOUSE_BUTTON_LEFT, etc., are ints
        if button == arcade.MOUSE_BUTTON_LEFT:
            return "Left Mouse Button"
        if button == arcade.MOUSE_BUTTON_RIGHT:
            return "Right Mouse Button"
        if button == arcade.MOUSE_BUTTON_MIDDLE:
            return "Middle Mouse Button"
    except Exception:
        pass
    # Fallback to string conversion
    return str(button)

#-------------------------------------------------------------------------------
# Window Wrapper (equivalent to cs110graphics.Window)
#-------------------------------------------------------------------------------
class Window(arcade.Window):
    def __init__(self, width=400, height=400, background="white", title="Graphics Window", first_function=None):
        super().__init__(width, height, title)
        self.background = arcade.color_from_hex_string(background) if background.startswith('#') else getattr(arcade.color, background.upper(), arcade.color.WHITE)
        self.first_function = first_function
        # shapes holds all drawable objects
        self.shapes = []
        # handlers holds tuples (shape, handler) registered via shape.add_handler
        self.handlers = []
        arcade.set_background_color(self.background)
        if first_function:
            first_function(self)

    def add(self, shape):
        self.shapes.append(shape)

    def remove(self, shape):
        if shape in self.shapes:
            self.shapes.remove(shape)
        # Also remove any event handlers associated with this shape
        if self.handlers:
            self.handlers = [(s, h) for (s, h) in self.handlers if s is not shape]

    def on_draw(self):
        arcade.start_render()
        # draw shapes in a stable order by depth (higher depth drawn first)
        for shape in sorted(self.shapes, key=lambda s: getattr(s, 'depth', 0), reverse=True):
            shape.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse press: deliver to the single top-most shape under the
        cursor. If that shape has no handler, the click is ignored (blocks
        objects below), matching cs110 behavior.
        """
        btn_name = _map_button(button)
        cs_x = x
        cs_y = self.height - y
        evt = _MouseEvent(btn_name)
        evt._set_mouse_location(cs_x, cs_y)

        # Find all shapes under the cursor
        under_cursor = []
        for idx, shape in enumerate(self.shapes):
            try:
                if shape.contains_point(cs_x, cs_y):
                    # whether this shape has any registered handler
                    has_handler = any(s is shape for (s, _) in self.handlers)
                    under_cursor.append((shape, idx, has_handler))
            except Exception:
                # shapes without hit-test just ignore
                pass

        if not under_cursor:
            return

        # Determine the top-most shape: lowest depth draws last; for ties,
        # later insertion is on top (larger index in self.shapes)
        def _shape_order(item):
            shape, idx, has_handler = item
            # Lower depth is on top; prefer shapes WITH handlers at same depth;
            # for ties, later insertion (higher idx) is on top.
            return (getattr(shape, 'depth', 0), 0 if has_handler else 1, -idx)

        top_shape, _, _ = min(under_cursor, key=_shape_order)

        # Collect handlers for this shape if any
        target_handlers = [h for (s, h) in self.handlers if s is top_shape]
        if not target_handlers:
            # No handler on top-most shape: block underlying shapes
            return
        # Call handlers (typically one)
        for handler in target_handlers:
            if hasattr(handler, 'handle_mouse_press'):
                handler.handle_mouse_press(evt)
        

    def on_mouse_release(self, x, y, button, modifiers):
        # Dispatch mouse release to the top-most shape only
        btn_name = _map_button(button)
        cs_x = x
        cs_y = self.height - y
        evt = _MouseEvent(btn_name)
        evt._set_mouse_location(cs_x, cs_y)

        under_cursor = []
        for idx, shape in enumerate(self.shapes):
            try:
                if shape.contains_point(cs_x, cs_y):
                    has_handler = any(s is shape for (s, _) in self.handlers)
                    under_cursor.append((shape, idx, has_handler))
            except Exception:
                pass

        if not under_cursor:
            return

        def _shape_order(item):
            shape, idx, has_handler = item
            return (getattr(shape, 'depth', 0), 0 if has_handler else 1, -idx)

        top_shape, _, _ = min(under_cursor, key=_shape_order)
        target_handlers = [h for (s, h) in self.handlers if s is top_shape]
        if not target_handlers:
            return
        for handler in target_handlers:
            if hasattr(handler, 'handle_mouse_release'):
                handler.handle_mouse_release(evt)

    def on_key_press(self, key, modifiers):
        for _, handler in self.handlers:
            if hasattr(handler, 'handle_key_press'):
                try:
                    handler.handle_key_press(key)
                except Exception:
                    pass

    def on_key_release(self, key, modifiers):
        for _, handler in self.handlers:
            if hasattr(handler, 'handle_key_release'):
                try:
                    handler.handle_key_release(key)
                except Exception:
                    pass


#-------------------------------------------------------------------------------
# EventHandler Equivalent
#-------------------------------------------------------------------------------
class EventHandler:
    def handle_key_press(self, key):
        pass

    def handle_key_release(self, key):
        pass


#-------------------------------------------------------------------------------
# Basic Shape Classes (Polygon, Circle, Rectangle, Square, Text, Image)
#-------------------------------------------------------------------------------
class Rectangle:
    def __init__(self, window, width=80, height=120, center=(200, 200), color=arcade.color.WHITE):
        self.window = window
        self.width = width
        self.height = height
        self.center_x, self.center_y = center
        self.color = color
        self.fill_color = color
        self.border_color = arcade.color.BLACK
        self.border_width = 2
        self.depth = 0
        # handlers registered on this shape
        self._handlers = []

    def draw(self):
        # Convert cs110 (top-left origin) center to arcade coordinates (bottom-left origin)
        arcade_y = self.window.height - self.center_y
        # draw fill if present
        if self.fill_color:
            arcade.draw_rectangle_filled(self.center_x, arcade_y, self.width, self.height, self.fill_color)
        # draw border if requested
        if self.border_width and self.border_color:
            arcade.draw_rectangle_outline(self.center_x, arcade_y, self.width, self.height, self.border_color, self.border_width)

    def move(self, dx, dy):
        self.center_x += dx
        self.center_y += dy

    # cs110graphics-like helpers used by classes.py
    def move_to(self, center):
        self.center_x, self.center_y = center

    def set_fill_color(self, color):
        self.fill_color = _resolve_color(color)

    def set_border_color(self, color):
        self.border_color = _resolve_color(color)

    def set_border_width(self, w):
        self.border_width = w

    def set_depth(self, depth):
        self.depth = depth

    def add_handler(self, handler):
        # Register handler on this shape and on the window so mouse events
        # will be dispatched to it when the shape is clicked.
        self._handlers.append(handler)
        if (self, handler) not in self.window.handlers:
            self.window.handlers.append((self, handler))

    def contains_point(self, x, y):
        half_w = self.width / 2
        half_h = self.height / 2
        return (self.center_x - half_w) <= x <= (self.center_x + half_w) and (self.center_y - half_h) <= y <= (self.center_y + half_h)


class Square(Rectangle):
    def __init__(self, window, side_length=80, center=(200, 200), color=arcade.color.WHITE):
        super().__init__(window, side_length, side_length, center, color)


class Circle:
    def __init__(self, window, radius=40, center=(200, 200), color=arcade.color.WHITE):
        self.window = window
        self.radius = radius
        self.center_x, self.center_y = center
        self.color = color
        self.fill_color = color
        self.border_color = arcade.color.BLACK
        self.border_width = 2
        self.depth = 0
        self._handlers = []

    def draw(self):
        arcade_y = self.window.height - self.center_y
        if self.fill_color:
            arcade.draw_circle_filled(self.center_x, arcade_y, self.radius, self.fill_color)
        if self.border_width and self.border_color:
            arcade.draw_circle_outline(self.center_x, arcade_y, self.radius, self.border_color, self.border_width)

    def move(self, dx, dy):
        self.center_x += dx
        self.center_y += dy

    def move_to(self, center):
        self.center_x, self.center_y = center

    def set_fill_color(self, color):
        self.fill_color = _resolve_color(color)

    def set_border_color(self, color):
        self.border_color = _resolve_color(color)

    def set_border_width(self, w):
        self.border_width = w

    def set_depth(self, depth):
        self.depth = depth

    def add_handler(self, handler):
        self._handlers.append(handler)
        if (self, handler) not in self.window.handlers:
            self.window.handlers.append((self, handler))

    def contains_point(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y
        return dx * dx + dy * dy <= self.radius * self.radius


class Polygon:
    def __init__(self, window, points, color=arcade.color.WHITE):
        self.window = window
        self.points = points
        self.color = color
        self.depth = 0

    def draw(self):
        # points are expected in cs110 coords; convert each y
        conv = [(x, self.window.height - y) for (x, y) in self.points]
        arcade.draw_polygon_filled(conv, self.color)

    def set_depth(self, depth):
        self.depth = depth


class Text:
    def __init__(self, window, text, size=12, center=(200, 200), color=arcade.color.BLACK):
        self.window = window
        self.text = text
        self.size = size
        self.center_x, self.center_y = center
        self.color = color
        self.depth = 0
        self._handlers = []

    def draw(self):
        arcade_y = self.window.height - self.center_y
        arcade.draw_text(self.text, self.center_x, arcade_y, self.color, self.size, anchor_x="center", anchor_y="center")

    def move_to(self, center):
        self.center_x, self.center_y = center

    def set_depth(self, depth):
        self.depth = depth

    def add_handler(self, handler):
        self._handlers.append(handler)
        if (self, handler) not in self.window.handlers:
            self.window.handlers.append((self, handler))

    def contains_point(self, x, y):
        # approximate bounding box for text clickable area
        w = max(40, len(self.text) * (self.size // 2))
        h = max(20, self.size + 6)
        half_w = w / 2
        half_h = h / 2
        return (self.center_x - half_w) <= x <= (self.center_x + half_w) and (self.center_y - half_h) <= y <= (self.center_y + half_h)


class Image:
    def __init__(self, window, image_loc, width=100, height=100, center=(200, 200)):
        self.window = window
        self.texture = arcade.load_texture(image_loc)
        self.center_x, self.center_y = center
        self.width = width
        self.height = height
        self.angle = 0
        self.depth = 0
        self._handlers = []

    def draw(self):
        # draw with the exact width/height requested (to match cs110 sizing)
        arcade_y = self.window.height - self.center_y
        # If this is a standard tile image (100x100), draw it slightly inset
        # so that the selection frame drawn behind remains visible.
        if self.width == 100 and self.height == 100:
            draw_w = max(1, self.width - 10)
            draw_h = max(1, self.height - 10)
        else:
            draw_w = self.width
            draw_h = self.height
        arcade.draw_texture_rectangle(self.center_x, arcade_y, draw_w, draw_h, self.texture, angle=self.angle)

    def move_to(self, center):
        self.center_x, self.center_y = center

    def set_depth(self, depth):
        self.depth = depth

    def add_handler(self, handler):
        self._handlers.append(handler)
        if (self, handler) not in self.window.handlers:
            self.window.handlers.append((self, handler))

    def contains_point(self, x, y):
        half_w = self.width / 2
        half_h = self.height / 2
        return (self.center_x - half_w) <= x <= (self.center_x + half_w) and (self.center_y - half_h) <= y <= (self.center_y + half_h)

    def rotate(self, angle):
        # angle in degrees; accumulate
        self.angle = (self.angle + angle) % 360

    def set_fill_color(self, color):
        # No-op for image but present for compatibility
        pass

    def set_border_color(self, color):
        # No-op for image compatibility
        pass

    def set_border_width(self, w):
        # No-op for image compatibility
        pass


#-------------------------------------------------------------------------------
# StartGraphicsSystem Equivalent
#-------------------------------------------------------------------------------
def StartGraphicsSystem(first_function, width=400, height=400, background="white", name="Graphics Window"):
    window = Window(width, height, background, name, first_function)
    arcade.run()
