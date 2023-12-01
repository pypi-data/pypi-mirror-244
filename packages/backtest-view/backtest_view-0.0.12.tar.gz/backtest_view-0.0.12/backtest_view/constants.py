import enum

NAME = 'backtest_view'


class BaseEnum(str, enum.Enum):
    value: str
    description: str

    def __new__(
            cls, value: str, description: str = ""
    ) -> 'BaseEnum':
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def list(cls):
        return list(map(lambda e: (e.value, e.description), cls))


class FileFormats(enum.Enum):
    JSON = 'json'


class Timeframe(enum.Enum):
    YEAR = '1Y'
    MONTH = '1M'
    DAY = '1d'
    HOUR = '1h'
    MINUTE = '1m'


FREQUENCY = {
    Timeframe.YEAR: 'y',
    Timeframe.MONTH: 'm',
    Timeframe.DAY: 'D',
    Timeframe.HOUR: 'h',
    Timeframe.MINUTE: '1min'
}


class PlotType(enum.Enum):
    CANDLE_PLOTS = 'candle_plots'
    SUB_PLOTS = 'sub_plots'


class Envs(BaseEnum):
    PROJECT_FOLDER = (
        f'{NAME.upper()}_PROJECT_FOLDER',
        'The project folder.'
    )
    CONFIG_PATH = (
        f'{NAME.upper()}_CONFIG_PATH',
        'The path to your bot config.'
    )
    STRATEGY = (
        f'{NAME.upper()}_STRATEGY',
        'The strategy to analyse'
    )
    PAIR = (
        f'{NAME.upper()}_PAIR',
        'The pair to analyse'
    )
    TIME_FRAME = (
        f'{NAME.upper()}_TIME_FRAME',
        'The time frame to display'
    )


