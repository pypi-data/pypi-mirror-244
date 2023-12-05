import typing

Columns = typing.Iterable[str]
Records = typing.Iterable[typing.Dict]


class DataLayer:

    def get_csv(self, path: str) -> Records:
        raise NotImplementedError('Use implementor.')

    def write_csv(self, records: Records, columns: Columns, path: str):
        raise NotImplementedError('Use implementor.')

    def get_json(self, path: str):
        raise NotImplementedError('Use implementor.')

    def write_json(self, target, path: str):
        raise NotImplementedError('Use implementor.')
