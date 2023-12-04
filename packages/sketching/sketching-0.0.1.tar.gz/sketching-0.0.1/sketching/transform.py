import math
import typing

import numpy


class TransformedPoint:

    def __init__(self, x: float, y: float, scale: float, rotation: float):
        self._x = x
        self._y = y
        self._scale = scale
        self._rotation = rotation

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_scale(self) -> float:
        return self._scale

    def get_rotation(self) -> float:
        return self._rotation


class Transformer:

    def __init__(self, matrix: typing.Optional[numpy.ndarray] = None, scale: float = 1,
        rotation: float = 0):
        matrix_unset = matrix is None
        scale_unset = abs(scale - 1) < 0.00001
        rotation_unset = abs(rotation - 0) < 0.00001

        self._is_default = matrix_unset and scale_unset and rotation_unset
        self._matrix = numpy.identity(3) if matrix is None else matrix
        self._scale = scale
        self._rotation = rotation

    def translate(self, x: float, y: float):
        transformation = numpy.identity(3)
        transformation[0][2] = x
        transformation[1][2] = y
        self._matrix = numpy.dot(self._matrix, transformation)
        self._is_default = False

    def scale(self, scale: float):
        transformation = numpy.identity(3)
        transformation[0][0] = scale
        transformation[1][1] = scale
        self._matrix = numpy.dot(self._matrix, transformation)
        self._scale *= scale
        self._is_default = False

    def rotate(self, angle: float):
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        transformation = numpy.identity(3)
        transformation[0][0] = cos_angle
        transformation[1][1] = cos_angle
        transformation[1][0] = -1 * sin_angle
        transformation[0][1] = sin_angle
        
        self._matrix = numpy.dot(self._matrix, transformation)
        self._rotation += angle
        self._is_default = False

    def transform(self, x: float, y: float) -> TransformedPoint:
        if self._is_default:
            return TransformedPoint(x, y, self._scale, self._rotation)

        input_array = numpy.array([x, y, 1])
        output = numpy.dot(self._matrix, input_array)
        
        x = output[0]
        y = output[1]

        return TransformedPoint(x, y, self._scale, self._rotation)

    def quick_copy(self) -> 'Transformer':
        return Transformer(self._matrix, self._scale, self._rotation)
