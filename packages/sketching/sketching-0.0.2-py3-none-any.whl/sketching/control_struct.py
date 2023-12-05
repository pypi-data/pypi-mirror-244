import typing


class Button:

    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


Buttons = typing.Iterable[Button]
ControlCallback = typing.Callable[[Button], None]


class Mouse:

    def get_x(self):
        raise NotImplementedError('Use implementor.')

    def get_y(self):
        raise NotImplementedError('Use implementor.')

    def get_buttons_pressed(self) -> Buttons:
        raise NotImplementedError('Use implementor.')

    def on_press(self, callback: ControlCallback):
        raise NotImplementedError('Use implementor.')

    def on_release(self, callback: ControlCallback):
        raise NotImplementedError('Use implementor.')


class Keyboard:

    def get_keys_pressed(self) -> Buttons:
        raise NotImplementedError('Use implementor.')

    def on_key_press(self, callback: ControlCallback):
        raise NotImplementedError('Use implementor.')

    def on_key_release(self, callback: ControlCallback):
        raise NotImplementedError('Use implementor.')
