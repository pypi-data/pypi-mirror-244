import asyncio
import base64
import csv
import io
import json
import time
import typing
import urllib.parse

import js
import pyodide.ffi
import pyodide.http

import sketching.abstracted
import sketching.const
import sketching.control_struct
import sketching.data_struct
import sketching.state_struct

DEFAULT_FPS = 20

KEY_MAP = {
    'ArrowLeft': sketching.const.KEYBOARD_LEFT_BUTTON,
    'ArrowUp': sketching.const.KEYBOARD_UP_BUTTON,
    'ArrowRight': sketching.const.KEYBOARD_RIGHT_BUTTON,
    'ArrowDown': sketching.const.KEYBOARD_DOWN_BUTTON,
    ' ': sketching.const.KEYBOARD_SPACE_BUTTON,
    'Control': sketching.const.KEYBOARD_CTRL_BUTTON,
    'Alt': sketching.const.KEYBOARD_ALT_BUTTON,
    'Shift': sketching.const.KEYBOARD_SHIFT_BUTTON,
    'Tab': sketching.const.KEYBOARD_TAB_BUTTON,
    'Home': sketching.const.KEYBOARD_HOME_BUTTON,
    'End': sketching.const.KEYBOARD_END_BUTTON,
    'Enter': sketching.const.KEYBOARD_RETURN_BUTTON,
    'Backspace': sketching.const.KEYBOARD_BACKSPACE_BUTTON,
    'null': None
}


class CanvasRegionEllipse:

    def __init__(self, x: float, y: float, radius_x: float, radius_y: float):
        self._x = x
        self._y = y
        self._radius_x = radius_x
        self._radius_y = radius_y
    
    def get_x(self) -> float:
        return self._x
    
    def get_y(self) -> float:
        return self._y
    
    def get_radius_x(self) -> float:
        return self._radius_x
    
    def get_radius_y(self) -> float:
        return self._radius_y


class CanvasRegionRect:

    def __init__(self, x: float, y: float, width: float, height: float):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    def get_x(self) -> float:
        return self._x
    
    def get_y(self) -> float:
        return self._y
    
    def get_width(self) -> float:
        return self._width
    
    def get_height(self) -> float:
        return self._height


class Sketch2DWeb(sketching.abstracted.Sketch):

    def __init__(self, width: float, height: float, element_id: str):
        super().__init__()

        # Save elements required for running the canvas
        self._element_id = element_id
        self._element = js.document.getElementById(element_id)
        self._element.width = width
        self._element.height = height
        self._element.style.display = 'none';
        self._context = self._element.getContext('2d')
        self._last_render = None

        # Internal only elements
        self._internal_loop_callback = None
        self._internal_mouse_x = 0
        self._internal_mouse_y = 0
        self._internal_pre_show_actions = []

        # User configurable state
        self._state_frame_rate = DEFAULT_FPS
        self._stopped = False

        # Callback
        self._callback_step = None
        self._callback_quit = None

        # Control
        self._keyboard = PygameKeyboard(self._element)
        self._mouse = PyscriptMouse(self._element)

    ############
    # Controls #
    ############

    def get_keyboard(self) -> sketching.control_struct.Keyboard:
        return self._keyboard

    def get_mouse(self) -> sketching.control_struct.Mouse:
        return self._mouse

    ########
    # Data #
    ########

    def get_data_layer(self) -> sketching.data_struct.DataLayer:
        return WebDataLayer()

    ###########
    # Drawing #
    ###########

    def clear(self, color: str):
        self._context.clearRect(0, 0, self._element.width, self._element.height);
        self._context.fillStyle = color
        self._context.fillRect(0, 0, self._element.width, self._element.height);

    def draw_arc(self, x1: float, y1: float, x2: float, y2: float, a1: float, a2: float):
        self._load_draw_params()

        a1_rad = self._convert_to_radians(a1) - js.Math.PI / 2
        a2_rad = self._convert_to_radians(a2) - js.Math.PI / 2
        
        current_machine = self._get_current_state_machine()
        mode_native = current_machine.get_arc_mode_native()
        mode_str = current_machine.get_arc_mode()

        self._draw_arc_rad(x1, y1, x2, y2, a1_rad, a2_rad, mode_native, mode_str)

    def draw_ellipse(self, x1: float, y1: float, x2: float, y2: float):
        current_machine = self._get_current_state_machine()
        mode_native = current_machine.get_ellipse_mode_native()
        mode_str = current_machine.get_ellipse_mode()

        self._draw_arc_rad(x1, y1, x2, y2, 0, 2 * js.Math.PI, mode_native, mode_str)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        current_machine = self._get_current_state_machine()
        if not current_machine.get_stroke_enabled():
            return

        self._load_draw_params()

        self._context.beginPath()
        self._context.moveTo(x1, y1);
        self._context.lineTo(x2, y2);
        self._context.stroke();

    def draw_rect(self, x1: float, y1: float, x2: float, y2: float):
        self._load_draw_params()

        current_machine = self._get_current_state_machine()
        native_mode = current_machine.get_rect_mode_native()
        mode_str = current_machine.get_rect_mode_native()

        region = self._get_canvas_region_rect_like(x1, y1, x2, y2, native_mode, mode_str)

        self._context.beginPath()
        self._context.rect(region.get_x(), region.get_y(), region.get_width(), region.get_height())

        if current_machine.get_fill_enabled():
            self._context.fill()

        if current_machine.get_stroke_enabled():
            self._context.stroke()

    def draw_shape(self, shape: sketching.shape_struct.Shape):
        current_machine = self._get_current_state_machine()

        self._load_draw_params()

        self._context.beginPath()
        self._context.moveTo(shape.get_start_x(), shape.get_start_y())

        for segment in shape.get_segments():
            strategy = segment.get_strategy()
            if strategy == 'straight':
                self._context.lineTo(segment.get_destination_x(), segment.get_destination_y())
            elif strategy == 'bezier':
                self._context.bezierCurveTo(
                    segment.get_control_x1(),
                    segment.get_control_y1(),
                    segment.get_control_x2(),
                    segment.get_control_y2(),
                    segment.get_destination_x(),
                    segment.get_destination_y()
                )
            else:
                raise RuntimeError('Unsupported segment type: ' + strategy)

        if shape.get_is_closed():
            self._context.closePath()

        if current_machine.get_fill_enabled():
            self._context.fill()

        if current_machine.get_stroke_enabled():
            self._context.stroke()

    def draw_text(self, x: float, y: float, content: str):
        current_machine = self._get_current_state_machine()

        self._load_draw_params()
        self._load_font_params()

        if current_machine.get_fill_enabled():
            self._context.fillText(content, x, y)

        if current_machine.get_stroke_enabled():
            self._context.strokeText(content, x, y)

    ##########
    # Events #
    ##########

    def on_step(self, callback: sketching.abstracted.StepCallback):
        self._callback_step = callback

    def on_quit(self, callback: sketching.abstracted.QuitCallback):
        self._callback_quit = callback

    #########
    # Image #
    #########

    def load_image(self, src: str) -> sketching.abstracted.Image:
        return WebImage(src)

    def draw_image(self, x: float, y: float, image: sketching.abstracted.Image):
        if not image.get_is_loaded():
            return

        self._load_draw_params()

        current_machine = self._get_current_state_machine()
        native_mode = current_machine.get_image_mode_native()
        mode_str = current_machine.get_image_mode_native()

        width = image.get_width()
        height = image.get_height()

        region = self._get_canvas_region_rect_like(x, y, width, height, native_mode, mode_str)

        self._context.drawImage(
            image.get_native(),
            region.get_x(),
            region.get_y(),
            region.get_width(),
            region.get_height()
        )

    def save_image(self, path: str):
        if not path.endswith('.png'):
            raise RuntimeError('Web export only supported to PNG.')
        
        link = js.document.createElement('a')
        link.download = path
        link.href = self._element.toDataURL('image/png')
        link.click()

    #########
    # State #
    #########

    def push_transform(self):
        self._context.save()

    def pop_transform(self):
        self._context.restore()

    ##########
    # System #
    ##########

    def set_fps(self, rate: int):
        self._state_frame_rate = rate

    def set_title(self, title: str):
        js.document.title = title

    def quit(self):
        self._stopped = True

    def show(self):
        self._element.style.display = 'block';

        for action in self._internal_pre_show_actions:
            action()

        self._stopped = False

        self._last_render = time.time()
        self._internal_loop_callback = pyodide.ffi.create_proxy(lambda: self._inner_loop())
        self._inner_loop()

    #############
    # Transform #
    #############

    def translate(self, x: float, y: float):
        self._context.translate(x, y)

    def rotate(self, angle: float):
        angle_rad = self._convert_to_radians(angle)
        self._context.rotate(angle_rad)

    def scale(self, scale: float):
        self._context.scale(scale, scale)

    ###########
    # Support #
    ###########

    def _inner_loop(self):
        if js.document.getElementById(self._element_id) == None:
            self._stopped = True

        if self._stopped:
            if self._callback_quit is not None:
                self._callback_quit()
            return

        if self._callback_step is not None:
            self._callback_step()

        time_elapsed = (time.time() - self._last_render) * 1000
        time_delay = round(1000 / self._state_frame_rate - time_elapsed)

        js.setTimeout(self._internal_loop_callback, time_delay)

    def _create_state_machine(self):
        return PyscriptSketchStateMachine()

    def _get_canvas_region_arc_ellipse(self, x1: float, y1: float, x2: float,
        y2: float, mode_native: int, mode_str: str) -> CanvasRegionEllipse:
        if mode_native == sketching.const.CENTER:
            center_x = x1
            center_y = y1
            radius_x = x2 / 2
            radius_y = y2 / 2
        elif mode_native == sketching.const.RADIUS:
            center_x = x1
            center_y = y1
            radius_x = x2
            radius_y = y2
        elif mode_native == sketching.const.CORNER:
            center_x = x1 + x2 / 2
            center_y = y1 + y2 / 2
            radius_x = x2 / 2
            radius_y = y2 / 2
        elif mode_native == sketching.const.CORNERS:
            (x1, y1, x2, y2) = sketching.abstracted.reorder_coords(x1, y1, x2, y2)
            width = x2 - x1
            height = y2 - y1
            center_x = x1 + width / 2
            center_y = y1 + height / 2
            radius_x = width / 2
            radius_y = height / 2
        else:
            raise RuntimeError('Unknown mode: ' + mode_str)

        return CanvasRegionEllipse(center_x, center_y, radius_x, radius_y)

    def _get_canvas_region_rect_like(self, x1: float, y1: float, x2: float,
        y2: float, native_mode: int, mode_str: str) -> CanvasRegionRect:
        if native_mode == sketching.const.CENTER:
            start_x = x1 - x2 / 2
            start_y = y1 - y2 / 2
            width = x2
            height = y2
        elif native_mode == sketching.const.RADIUS:
            start_x = x1 - x2
            start_y = y1 - y2
            width = x2 * 2
            height = y2 * 2
        elif native_mode == sketching.const.CORNER:
            start_x = x1
            start_y = y1
            width = x2
            height = y2
        elif native_mode == sketching.const.CORNERS:
            (x1, y1, x2, y2) = sketching.abstracted.reorder_coords(x1, y1, x2, y2)
            start_x = x1
            start_y = y1
            width = x2 - x1
            height = y2 - y1
        else:
            raise RuntimeError('Unknown mode: ' + mode_str)

        return CanvasRegionRect(start_x, start_y, width, height)

    def _load_draw_params(self):
        current_machine = self._get_current_state_machine()
        self._context.fillStyle = current_machine.get_fill_native()
        self._context.strokeStyle = current_machine.get_stroke_native()
        self._context.lineWidth = current_machine.get_stroke_weight_native()

    def _load_font_params(self):
        current_machine = self._get_current_state_machine()

        self._context.font = current_machine.get_text_font_native()

        text_align = current_machine.get_text_align_native()
        self._context.textAlign = text_align.get_horizontal_align()
        self._context.textBaseline = text_align.get_vertical_align()

    def _draw_arc_rad(self, x1: float, y1: float, x2: float, y2: float, a1: float, a2: float,
        mode_native: int, mode_str: str):
        self._load_draw_params()

        current_machine = self._get_current_state_machine()
        region = self._get_canvas_region_arc_ellipse(x1, y1, x2, y2, mode_native, mode_str)

        self._context.beginPath();

        self._context.ellipse(
            region.get_x(),
            region.get_y(),
            region.get_radius_x(),
            region.get_radius_y(),
            0,
            a1,
            a2
        )

        if current_machine.get_fill_enabled():
            self._context.fill()

        if current_machine.get_stroke_enabled():
            self._context.stroke()


class PyscriptSketchStateMachine(sketching.state_struct.SketchStateMachine):

    def __init__(self):
        super().__init__()
        self._text_align_native = self._transform_text_align(super().get_text_align_native())

    def set_text_align(self, text_align: sketching.state_struct.TextAlign):
        super().set_text_align(text_align)
        self._text_align_native = self._transform_text_align(super().get_text_align_native())

    def get_text_align_native(self):
        return self._text_align_native

    def get_text_font_native(self):
        font = self.get_text_font()
        return '%dpx %s' % (int(font.get_size()), font.get_identifier())

    def _transform_text_align(self,
        text_align: sketching.state_struct.TextAlign) -> sketching.state_struct.TextAlign:
        
        HORIZONTAL_ALIGNS = {
            sketching.const.LEFT: 'left',
            sketching.const.CENTER: 'center',
            sketching.const.RIGHT: 'right'
        }

        VERTICAL_ALIGNS = {
            sketching.const.TOP: 'top',
            sketching.const.CENTER: 'middle',
            sketching.const.BASELINE: 'alphabetic',
            sketching.const.BOTTOM: 'bottom'
        }
        
        return sketching.state_struct.TextAlign(
            HORIZONTAL_ALIGNS[text_align.get_horizontal_align()],
            VERTICAL_ALIGNS[text_align.get_vertical_align()]
        )


class WebImage(sketching.abstracted.Image):

    def __init__(self, src: str):
        super().__init__(src)

        image = js.document.createElement("img");
        image.src = src

        self._native = image
        self._width = None
        self._height = None

    def get_width(self) -> float:
        if self._width is None:
            return self._native.width
        else:
            return self._width

    def get_height(self) -> float:
        if self._height is None:
            return self._native.height
        else:
            return self._height

    def resize(self, width: float, height: float):
        self._width = width
        self._height = height

    def get_native(self):
        return self._native

    def get_is_loaded(self):
        return self._native.naturalWidth > 0


class PyscriptMouse(sketching.control_struct.Mouse):

    def __init__(self, element):
        self._element = element

        self._x = 0
        self._y = 0

        self._buttons_pressed = set()

        mouse_move_callback = pyodide.ffi.create_proxy(
            lambda event: self._report_mouse_move(event)
        )
        self._element.addEventListener(
            'mousemove',
            mouse_move_callback
        )

        mouse_down_callback = pyodide.ffi.create_proxy(
            lambda event: self._report_mouse_down(event)
        )
        self._element.addEventListener(
            'mousedown',
            mouse_down_callback
        )

        click_callback = pyodide.ffi.create_proxy(
            lambda event: self._report_click(event)
        )
        self._element.addEventListener(
            'click',
            click_callback
        )

        context_menu_callback = pyodide.ffi.create_proxy(
            lambda event: self._report_context_menu(event)
        )
        self._element.addEventListener(
            'contextmenu',
            context_menu_callback
        )

        self._press_callback = None
        self._release_callback = None

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_buttons_pressed(self) -> sketching.control_struct.Buttons:
        return map(lambda x: sketching.control_struct.Button(x), self._buttons_pressed)

    def on_press(self, callback: sketching.control_struct.ControlCallback):
        self._press_callback = callback

    def on_release(self, callback: sketching.control_struct.ControlCallback):
        self._release_callback = callback

    def _report_mouse_move(self, event):
        self._x = event.clientX - self._element.offsetLeft
        self._y = event.clientY - self._element.offsetTop

    def _report_mouse_down(self, event):
        if event.button == 0:
            self._buttons_pressed.add(sketching.const.MOUSE_LEFT_BUTTON)
            if self._press_callback is not None:
                button = sketching.control_struct.Button(sketching.const.MOUSE_LEFT_BUTTON)
                print(button)
                self._press_callback(button)
        elif event.button == 2:
            self._buttons_pressed.add(sketching.const.MOUSE_RIGHT_BUTTON)
            if self._press_callback is not None:
                button = sketching.control_struct.Button(sketching.const.MOUSE_RIGHT_BUTTON)
                self._press_callback(button)

    def _report_click(self, event):
        self._buttons_pressed.remove(sketching.const.MOUSE_LEFT_BUTTON)

        if self._release_callback is not None:
            button = sketching.control_struct.Button(sketching.const.MOUSE_LEFT_BUTTON)
            self._release_callback(button)
        
        event.preventDefault()

    def _report_context_menu(self, event):
        self._buttons_pressed.remove(sketching.const.MOUSE_RIGHT_BUTTON)

        if self._release_callback is not None:
            button = sketching.control_struct.Button(sketching.const.MOUSE_RIGHT_BUTTON)
            self._release_callback(button)

        event.preventDefault()


class PygameKeyboard(sketching.control_struct.Keyboard):

    def __init__(self, element):
        super().__init__()
        self._element = element
        self._pressed = set()
        self._press_callback = None
        self._release_callback = None

        keydown_callback = pyodide.ffi.create_proxy(
            lambda event: self._report_key_down(event)
        )
        self._element.addEventListener(
            'keydown',
            keydown_callback
        )

        keyup_callback = pyodide.ffi.create_proxy(
            lambda event: self._report_key_up(event)
        )
        self._element.addEventListener(
            'keyup',
            keyup_callback
        )

    def get_keys_pressed(self) -> sketching.control_struct.Buttons:
        return map(lambda x: sketching.control_struct.Button(x), self._pressed)

    def on_key_press(self, callback: sketching.control_struct.ControlCallback):
        self._press_callback = callback

    def on_key_release(self, callback: sketching.control_struct.ControlCallback):
        self._release_callback = callback

    def _report_key_down(self, event):
        key = self._map_key(event.key)
        
        if key is None:
            return

        self._pressed.add(key)

        if self._press_callback is not None:
            button = sketching.control_struct.Button(key)
            self._press_callback(button)
        
        event.preventDefault()
    
    def _report_key_up(self, event):
        key = self._map_key(event.key)
        
        if key is None:
            return

        self._pressed.remove(key)

        if self._release_callback is not None:
            button = sketching.control_struct.Button(key)
            self._release_callback(button)
        
        event.preventDefault()

    def _map_key(self, target: str) -> typing.Optional[str]:
        if target in KEY_MAP:
            return KEY_MAP[target]
        else:
            return target.lower()


class WebDataLayer(sketching.data_struct.DataLayer):

    def get_csv(self, path: str) -> sketching.data_struct.Records:
        string_io = pyodide.http.open_url(path)
        reader = csv.DictReader(string_io)
        return list(reader)

    def write_csv(self, records: sketching.data_struct.Records,
        columns: sketching.data_struct.Columns, path: str):
        def build_record(target: typing.Dict) -> typing.Dict:
            return dict(map(lambda key: (key, target[key]), columns))

        records_serialized = map(build_record, records)

        target = io.StringIO()

        writer = csv.DictWriter(target, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records_serialized)

        self._download_text(target.getvalue(), path, 'text/csv')

    def get_json(self, path: str):
        string_io = pyodide.http.open_url(path)
        return json.loads(string_io.read())

    def write_json(self, target, path: str):
        self._download_text(json.dumps(target), path, 'application/json')

    def _download_text(self, text: str, filename: str, mime: str):
        text_encoded = urllib.parse.quote(text)

        link = js.document.createElement('a')
        link.download = filename
        link.href = 'data:%s;charset=utf-8,%s' % (mime, text_encoded)
        
        link.click()
