import sketching.const


class TextAlign:

    def __init__(self, horizontal_align, vertical_align):
        self._horizontal_align = horizontal_align
        self._vertical_align = vertical_align
    
    def get_horizontal_align(self):
        return self._horizontal_align
    
    def get_vertical_align(self):
        return self._vertical_align


class Font:

    def __init__(self, identifier, size):
        self._identifier = identifier
        self._size = size

    def get_identifier(self):
        return self._identifier

    def get_size(self):
        return self._size


class SketchStateMachine:

    def __init__(self):
        self._fill_enabled = True
        self._fill_str = '#F0F0F0'
        self._stroke_str = '#333333'
        self._stroke_weight = 1

        self._angle_mode = 'radians'
        self._angle_mode_enum = sketching.const.ANGLE_MODES[self._angle_mode]

        self._arc_mode = 'radius'
        self._arc_mode_enum = sketching.const.SHAPE_MODES[self._arc_mode]

        self._ellipse_mode = 'radius'
        self._ellipse_mode_enum = sketching.const.SHAPE_MODES[self._ellipse_mode]

        self._rect_mode = 'corner'
        self._rect_mode_enum = sketching.const.SHAPE_MODES[self._rect_mode]

        self._text_font = None
        self._text_align = TextAlign('left', 'baseline')
        self._text_align_enum = TextAlign(
            sketching.const.ALIGN_OPTIONS['left'],
            sketching.const.ALIGN_OPTIONS['baseline']
        )
        
        self._image_mode = 'corner'
        self._image_mode_enum = sketching.const.SHAPE_MODES[self._image_mode]

    ##########
    # Colors #
    ##########

    def set_fill(self, fill: str):
        self._fill_enabled = True
        self._fill_str = fill

    def get_fill(self) -> str:
        return self._fill_str

    def get_fill_native(self):
        return self._fill_str

    def get_fill_enabled(self) -> bool:
        return self._fill_enabled

    def clear_fill(self):
        self._fill_enabled = False

    def set_stroke(self, stroke: str):
        self._stroke_str = stroke

    def get_stroke(self) -> str:
        return self._stroke_str

    def get_stroke_native(self):
        return self._stroke_str

    def get_stroke_enabled(self) -> bool:
        return self._stroke_weight > 0

    def clear_stroke(self):
        self._stroke_weight = 0

    ###########
    # Drawing #
    ###########

    def set_arc_mode(self, mode: str):
        if mode not in sketching.const.SHAPE_MODES:
            raise RuntimeError('Unknown arc mode: ' + mode)

        self._arc_mode = mode
        self._arc_mode_enum = sketching.const.SHAPE_MODES[self._arc_mode]

    def get_arc_mode(self) -> str:
        return self._arc_mode

    def get_arc_mode_native(self):
        return self._arc_mode_enum

    def set_ellipse_mode(self, mode: str):
        if mode not in sketching.const.SHAPE_MODES:
            raise RuntimeError('Unknown ellipse mode: ' + mode)

        self._ellipse_mode = mode
        self._ellipse_mode_enum = sketching.const.SHAPE_MODES[self._ellipse_mode]

    def get_ellipse_mode(self) -> str:
        return self._ellipse_mode

    def get_ellipse_mode_native(self):
        return self._ellipse_mode_enum

    def set_rect_mode(self, mode: str):
        if mode not in sketching.const.SHAPE_MODES:
            raise RuntimeError('Unknown rect mode: ' + mode)

        self._rect_mode = mode
        self._rect_mode_enum = sketching.const.SHAPE_MODES[self._rect_mode]

    def get_rect_mode(self) -> str:
        return self._rect_mode

    def get_rect_mode_native(self):
        return self._rect_mode_enum

    def set_stroke_weight(self, stroke_weight: float):
        if stroke_weight < 0:
            raise RuntimeError('Stroke weight must be zero or positive.')

        self._stroke_weight = stroke_weight

    def get_stroke_weight(self) -> float:
        return self._stroke_weight

    def get_stroke_weight_native(self):
        return self._stroke_weight

    def set_text_font(self, font: Font):
        self._text_font = font

    def get_text_font(self) -> Font:
        if self._text_font is None:
            raise RuntimeError('Font not yet set.')

        return self._text_font

    def get_text_font_native(self):
        return self.get_text_font()
    
    def set_text_align(self, text_align: TextAlign):
        def check_align(name):
            if name not in sketching.const.ALIGN_OPTIONS:
                raise RuntimeError('Unknown align: ' + name)

        check_align(text_align.get_horizontal_align())
        check_align(text_align.get_vertical_align())

        self._text_align = text_align
        self._text_align_enum = TextAlign(
            sketching.const.ALIGN_OPTIONS[self._text_align.get_horizontal_align()],
            sketching.const.ALIGN_OPTIONS[self._text_align.get_vertical_align()]
        )

    def get_text_align(self) -> TextAlign:
        return self._text_align

    def get_text_align_native(self):
        return self._text_align_enum

    #########
    # Image #
    #########

    def set_image_mode(self, mode: str):
        if mode not in ['center', 'corner']:
            raise RuntimeError('Unknown image mode: ' + mode)

        self._image_mode = mode
        self._image_mode_enum = sketching.const.SHAPE_MODES[self._image_mode]

    def get_image_mode(self) -> str:
        return self._image_mode

    def get_image_mode_native(self):
        return self._image_mode_enum

    ################
    # Other Params #
    ################

    def set_angle_mode(self, mode: str):
        if mode not in sketching.const.ANGLE_MODES:
            raise RuntimeError('Unknown angle mode: ' + mode)

        self._angle_mode = mode
        self._angle_mode_enum = sketching.const.ANGLE_MODES[self._angle_mode]

    def get_angle_mode(self) -> str:
        return self._angle_mode

    def get_angle_mode_native(self):
        return self._angle_mode_enum