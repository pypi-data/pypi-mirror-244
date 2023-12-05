import typing


class Line:

    def get_destination_x(self) -> float:
        raise NotImplementedError('Use implementor.')

    def get_destination_y(self) -> float:
        raise NotImplementedError('Use implementor.')
    
    def get_min_x(self) -> float:
        raise NotImplementedError('Use impelentor.')
    
    def get_max_x(self) -> float:
        raise NotImplementedError('Use impelentor.')
    
    def get_min_y(self) -> float:
        raise NotImplementedError('Use impelentor.')
    
    def get_max_y(self) -> float:
        raise NotImplementedError('Use impelentor.')

    def get_strategy(self) -> str:
        raise NotImplementedError('Use implementor.')


class StraightLine(Line):

    def __init__(self, destination_x: float, destination_y: float):
        self._destination_x = destination_x
        self._destination_y = destination_y

    def get_destination_x(self) -> float:
        return self._destination_x

    def get_destination_y(self) -> float:
        return self._destination_y

    def get_min_x(self) -> float:
        return self._destination_x

    def get_max_x(self) -> float:
        return self._destination_x

    def get_min_y(self) -> float:
        return self._destination_y

    def get_max_y(self) -> float:
        return self._destination_y

    def get_strategy(self) -> str:
        return 'straight'


class BezierLine(Line):

    def __init__(self, control_x1: float, control_y1: float, control_x2: float, control_y2: float,
        destination_x: float, destination_y: float):
        self._control_x1 = control_x1
        self._control_y1 = control_y1
        self._control_x2 = control_x2
        self._control_y2 = control_y2
        self._destination_x = destination_x
        self._destination_y = destination_y

    def get_control_x1(self):
        return self._control_x1
    
    def get_control_y1(self):
        return self._control_y1
    
    def get_control_x2(self):
        return self._control_x2
    
    def get_control_y2(self):
        return self._control_y2
    
    def get_destination_x(self):
        return self._destination_x
    
    def get_destination_y(self):
        return self._destination_y

    def get_min_x(self) -> float:
        return min([
            self._control_x1,
            self._control_x2,
            self._destination_x
        ])

    def get_max_x(self) -> float:
        return max([
            self._control_x1,
            self._control_x2,
            self._destination_x
        ])

    def get_min_y(self) -> float:
        return min([
            self._control_y1,
            self._control_y2,
            self._destination_y
        ])

    def get_max_y(self) -> float:
        return max([
            self._control_y1,
            self._control_y2,
            self._destination_y
        ])

    def get_strategy(self) -> str:
        return 'bezier'


class Shape:

    def __init__(self, start_x: float, start_y: float):
        self._start_x = start_x
        self._start_y = start_y
        self._closed = False
        self._finished = False
        self._segments: typing.List[Line] = []

    def add_line_to(self, x: float, y: float):
        self._assert_not_finished()
        self._segments.append(StraightLine(x, y))

    def add_bezier_to(self, control_x1: float, control_y1: float, control_x2: float,
        control_y2: float, destination_x: float, destination_y: float):
        self._assert_not_finished()
        self._segments.append(BezierLine(
            control_x1,
            control_y1,
            control_x2,
            control_y2,
            destination_x,
            destination_y
        ))

    def get_start_x(self) -> float:
        return self._start_x

    def get_start_y(self) -> float:
        return self._start_y

    def get_segments(self) -> typing.Iterable[Line]:
        return self._segments

    def get_is_finished(self) -> bool:
        return self._finished

    def end(self):
        self._assert_not_finished()
        self._finished = True
        self._closed = False

    def close(self):
        self._assert_not_finished()
        self._finished = True
        self._closed = True

    def get_is_closed(self) -> bool:
        self._assert_finished()
        return self._closed

    def get_min_x(self):
        self._assert_finished()
        return min([self._start_x] + [x.get_min_x() for x in self._segments])

    def get_max_x(self):
        self._assert_finished()
        return max([self._start_x] + [x.get_max_x() for x in self._segments])

    def get_min_y(self):
        self._assert_finished()
        return min([self._start_y] + [x.get_min_y() for x in self._segments])

    def get_max_y(self):
        self._assert_finished()
        return max([self._start_y] + [x.get_max_y() for x in self._segments])

    def _assert_not_finished(self):
        if self._finished:
            raise RuntimeError('Whoops! This shape is already finished.')

    def _assert_finished(self):
        if not self._finished:
            raise RuntimeError('Whoops! This shape is not yet finished.')