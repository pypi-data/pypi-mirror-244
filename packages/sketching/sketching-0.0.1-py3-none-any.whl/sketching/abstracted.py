import copy
import math
import typing

import sketching.const
import sketching.control_struct
import sketching.data_struct
import sketching.shape_struct
import sketching.state_struct

StepCallback = typing.Callable[[], None]
QuitCallback = StepCallback


class Image:

    def __init__(self, src: str):
        self._src = src

    def get_src(self) -> str:
        return self._src

    def get_width(self) -> float:
        raise NotImplementedError('Use implementor.')

    def get_height(self) -> float:
        raise NotImplementedError('Use implementor.')

    def resize(self, width: float, height: float):
        raise NotImplementedError('Use implementor.')

    def get_native(self):
        raise NotImplementedError('Use implementor.')

    def get_is_loaded(self):
        raise NotImplementedError('Use implementor.')


class Sketch:

    def __init__(self):
        self._state_current_machine = self._create_state_machine()
        self._state_machine_stack = []

    ##########
    # Colors #
    ##########

    def set_fill(self, color_hex: str):
        self._get_current_state_machine().set_fill(color_hex)

    def clear_fill(self):
        self._get_current_state_machine().clear_fill()

    def set_stroke(self, color_hex: str):
        self._get_current_state_machine().set_stroke(color_hex)

    def clear_stroke(self):
        self._get_current_state_machine().clear_stroke()

    ############
    # Controls #
    ############

    def get_keyboard(self) -> sketching.control_struct.Keyboard:
        raise NotImplementedError('Use implementor.')

    def get_mouse(self) -> sketching.control_struct.Mouse:
        raise NotImplementedError('Use implementor.')

    ########
    # Data #
    ########

    def get_data_layer(self) -> sketching.data_struct.DataLayer:
        raise NotImplementedError('Use implementor.')

    ###########
    # Drawing #
    ###########

    def clear(self, color: str):
        raise NotImplementedError('Use implementor.')

    def set_arc_mode(self, mode: str):
        self._get_current_state_machine().set_arc_mode(mode)

    def draw_arc(self, x1: float, y1: float, x2: float, y2: float, a1: float, a2: float):
        raise NotImplementedError('Use implementor.')

    def set_ellipse_mode(self, mode: str):
        self._get_current_state_machine().set_ellipse_mode(mode)

    def draw_ellipse(self, x1: float, y1: float, x2: float, y2: float):
        raise NotImplementedError('Use implementor.')

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        raise NotImplementedError('Use implementor.')

    def set_rect_mode(self, mode: str):
        self._get_current_state_machine().set_rect_mode(mode)

    def draw_rect(self, x1: float, y1: float, x2: float, y2: float):
        raise NotImplementedError('Use implementor.')

    def start_shape(self, x: float, y: float) -> sketching.shape_struct.Shape:
        return sketching.shape_struct.Shape(x, y)

    def draw_shape(self, shape: sketching.shape_struct.Shape):
        raise NotImplementedError('Use implementor.')

    def set_stroke_weight(self, weight: float):
        self._get_current_state_machine().set_stroke_weight(weight)

    def set_text_font(self, identifier: str, size: float):
        font = sketching.state_struct.Font(identifier, size)
        self._get_current_state_machine().set_text_font(font)

    def set_text_align(self, horizontal_align: str, vertical_align: str = 'baseline'):
        align_struct = sketching.state_struct.TextAlign(horizontal_align, vertical_align)
        self._get_current_state_machine().set_text_align(align_struct)

    def draw_text(self, x: float, y: float, content: str):
        raise NotImplementedError('Use implementor.')

    ##########
    # Events #
    ##########

    def on_step(self, callback: StepCallback):
        raise NotImplementedError('Use implementor.')

    def on_quit(self, callback: QuitCallback):
        raise NotImplementedError('Use implementor.')

    #########
    # Image #
    #########

    def set_image_mode(self, mode: str):
        self._get_current_state_machine().set_image_mode(mode)

    def load_image(self, src: str) -> Image:
        raise NotImplementedError('Use implementor.')

    def draw_image(self, x: float, y: float, image: Image):
        raise NotImplementedError('Use implementor.')

    def save_image(self, path: str):
        raise NotImplementedError('Use implementor.')

    ################
    # Other Params #
    ################

    def set_angle_mode(self, mode: str):
        self._get_current_state_machine().set_angle_mode(mode)

    #########
    # State #
    #########

    def push_transform(self):
        raise NotImplementedError('Use implementor.')

    def pop_transform(self):
        raise NotImplementedError('Use implementor.')

    def push_style(self):
        current = self._get_current_state_machine()
        current_copy = copy.deepcopy(current)
        self._state_machine_stack.append(current_copy)

    def pop_style(self):
        if len(self._state_machine_stack) == 0:
            raise RuntimeError('Cannot pop an empty style stack.')

        self._state_current_machine = self._state_machine_stack.pop()

    ##########
    # System #
    ##########

    def set_fps(self, rate: int):
        raise NotImplementedError('Use implementor.')

    def set_title(self, title: str):
        raise NotImplementedError('Use implementor.')

    def quit(self):
        raise NotImplementedError('Use implementor.')

    def show(self):
        raise NotImplementedError('Use implementor.')

    #############
    # Transform #
    #############

    def translate(self, x: float, y: float):
        raise NotImplementedError('Use implementor.')

    def rotate(self, angle: float):
        raise NotImplementedError('Use implementor.')

    def scale(self, scale: float):
        raise NotImplementedError('Use implementor.')

    ###########
    # Support #
    ###########

    def _create_state_machine(self) -> sketching.state_struct.SketchStateMachine:
        raise NotImplementedError('Use implementor.')

    def _get_current_state_machine(self) -> sketching.state_struct.SketchStateMachine:
        return self._state_current_machine

    def _convert_to_radians(self, angle: float) -> float:
        current_angle_mode = self._get_current_state_machine()

        if current_angle_mode == sketching.const.RADIANS:
            return angle
        else:
            return math.radians(angle)


def reorder_coords(x1, y1, x2, y2):
    x_coords = [x1, x2]
    y_coords = [y1, y2]
    x_coords.sort()
    y_coords.sort()
    return [x_coords[0], y_coords[0], x_coords[1], y_coords[1]]
