import itertools
import math
import typing

import PIL.Image
import PIL.ImageColor
import PIL.ImageDraw

import sketching.bezier_util
import sketching.shape_struct
import sketching.state_struct

COLOR_MAYBE = typing.Optional[typing.Tuple[int]]


class PillowUtilImage:

    def __init__(self, x: float, y: float, width: float, height: float, image: PIL.Image.Image):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._image = image

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def get_image(self) -> PIL.Image.Image:
        return self._image


def make_arc_image(min_x: float, min_y: float, width: float, height: float, start_rad: float,
    end_rad: float, stroke_enabled: bool, fill_enabled: bool, stroke_color: COLOR_MAYBE,
    fill_color: COLOR_MAYBE, stroke_weight: float) -> PillowUtilImage:

    width_offset = width + stroke_weight * 2
    height_offset = height + stroke_weight * 2

    size = (width_offset, height_offset)
    target_image = PIL.Image.new('RGBA', size, (255, 255, 255, 0))
    target_surface = PIL.ImageDraw.Draw(target_image, 'RGBA')

    bounds = (
        (stroke_weight, stroke_weight),
        (width + stroke_weight, height + stroke_weight)
    )

    start_deg = math.degrees(start_rad) - 90
    end_deg = math.degrees(end_rad) - 90

    if fill_enabled:
        target_surface.chord(
            bounds,
            start_deg,
            end_deg,
            fill=fill_color,
        )

    if stroke_enabled:
        target_surface.arc(
            bounds,
            start_deg,
            end_deg,
            fill=stroke_color,
            width=stroke_weight
        )

    return PillowUtilImage(
        min_x - stroke_weight,
        min_y - stroke_weight,
        width_offset,
        height_offset,
        target_image
    )


class SegmentSimplifier:

    def __init__(self, start_x: float, start_y: float):
        self._previous_x = start_x
        self._previous_y = start_y

    def simplify(self, segment) -> typing.Iterable[typing.Iterable[float]]:
        strategy = segment.get_strategy()
        if strategy == 'straight':
            ret_vals = ((segment.get_destination_x(), segment.get_destination_y()),)
        elif strategy == 'bezier':
            change_y = abs(segment.get_control_y2() - segment.get_control_y1())
            change_x = abs(segment.get_control_x2() - segment.get_control_x1())
            
            num_segs = (change_y**2 + change_x**2) ** 0.5 / 10
            num_segs_int = int(num_segs)
            num_segs_float = float(num_segs_int)
            
            fractions = map(lambda x: x / num_segs_float, range(0, num_segs_int + 1))
            bezier_gen = sketching.bezier_util.make_bezier((
                (self._previous_x, self._previous_y),
                (segment.get_control_x1(), segment.get_control_y1()),
                (segment.get_control_x2(), segment.get_control_y2()),
                (segment.get_destination_x(), segment.get_destination_y())
            ))
            ret_vals = bezier_gen(fractions)
        else:
            raise RuntimeError('Unknown segment strategy: ' + strategy)

        self._previous_x = segment.get_destination_x()
        self._previous_y = segment.get_destination_y()

        return ret_vals


def make_shape_image(shape: sketching.shape_struct.Shape, stroke_enabled: bool, fill_enabled: bool,
    stroke_color: COLOR_MAYBE, fill_color: COLOR_MAYBE, stroke_weight: float) -> PillowUtilImage:
    
    if not shape.get_is_finished():
        raise RuntimeError('Finish shape before drawing.')

    min_x = shape.get_min_x()
    max_x = shape.get_max_x()
    min_y = shape.get_min_y()
    max_y = shape.get_max_y()

    width = max_x - min_x
    height = max_y - min_y
    width_offset = width + stroke_weight * 2
    height_offset = height + stroke_weight * 2
    
    size = (width_offset, height_offset)
    target_image = PIL.Image.new('RGBA', size, (255, 255, 255, 0))
    target_surface = PIL.ImageDraw.Draw(target_image, 'RGBA')

    def adjust_coord(coord):
        return (
            coord[0] - min_x + stroke_weight,
            coord[1] - min_y + stroke_weight
        )

    start_x = shape.get_start_x()
    start_y = shape.get_start_y()
    start_coords = [(start_x, start_y)]
    
    simplified_segements = []
    simplifier = SegmentSimplifier(start_x, start_y)
    for segment in shape.get_segments():
        simplified_segements.append(simplifier.simplify(segment))
    
    later_coords = itertools.chain(*simplified_segements)
    all_coords = itertools.chain(start_coords, later_coords)
    coords = [adjust_coord(x) for x in all_coords]

    if shape.get_is_closed():
        target_surface.polygon(coords, fill=fill_color, outline=stroke_color, width=stroke_weight)
    else:
        target_surface.line(coords, fill=stroke_color, width=stroke_weight, joint='curve')

    return PillowUtilImage(
        min_x - stroke_weight,
        min_y - stroke_weight,
        width_offset,
        height_offset,
        target_image
    )


def make_text_image(x: float, y: float, content: str, font: PIL.ImageFont.ImageFont,
    fill_enabled: bool, fill: COLOR_MAYBE, stroke_enabled: bool, stroke: COLOR_MAYBE,
    stroke_weight: float, anchor: str):

    temp_image = PIL.Image.new('RGBA', (1,1), (255, 255, 255, 0))
    temp_surface = PIL.ImageDraw.Draw(temp_image, 'RGBA')
    bounding_box = temp_surface.textbbox(
        (stroke_weight, stroke_weight),
        content,
        font=font,
        anchor=anchor,
        stroke_width=stroke_weight
    )

    start_x = bounding_box[0]
    end_x = bounding_box[2]

    start_y = bounding_box[1]
    end_y = bounding_box[3]

    width = end_x - start_x
    height = end_y - start_y

    width_offset = width + stroke_weight * 2
    height_offset = height + stroke_weight * 2

    size = (width_offset, height_offset)
    target_image = PIL.Image.new('RGBA', size, (255, 255, 255, 0))
    target_surface = PIL.ImageDraw.Draw(target_image, 'RGBA')

    if stroke_enabled:
        target_surface.text(
            (-1 * start_x + stroke_weight, -1 * start_y + stroke_weight),
            content,
            font=font,
            anchor=anchor,
            stroke_width=stroke_weight,
            stroke_fill=stroke,
            fill=(0, 0, 0, 0)
        )

    if fill_enabled:
        target_surface.text(
            (-1 * start_x + stroke_weight, -1 * start_y + stroke_weight),
            content,
            font=font,
            anchor=anchor,
            fill=fill
        )

    return PillowUtilImage(
        start_x - stroke_weight + x,
        start_y - stroke_weight + y,
        width_offset,
        height_offset,
        target_image
    )
