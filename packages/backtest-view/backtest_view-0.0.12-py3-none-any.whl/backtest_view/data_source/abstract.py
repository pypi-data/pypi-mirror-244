import logging
import pandas as pd
from typing import List, Optional, Callable, Dict
from datetime import datetime, timedelta, timezone
from abc import abstractmethod
from backtest_view.constants import Timeframe


logger = logging.getLogger(__name__)


class AbstractDataSource:

    def __init__(
            self,
            config: str,
            strategy: str,
            pair: str,
            timeframe: Timeframe.HOUR,
            project_folder: Optional[str],
            label: str = None,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            download: bool = True
    ):
        self.config = config
        self.strategy = strategy
        self.pair = pair
        self.timeframe = timeframe
        self.project_folder = project_folder
        self.start = start
        self.end = end
        self.download = download
        self.label = label

        self._dataframes = {}
        self._trades = None
        self._replay_config = None
        self._startup_time_delta = None
        self._strategy_instance = None

        # initialize data
        self.set_strategy_instance()
        self._set_timerange()

    def _set_timerange(self) -> None:
        # don't dynamically determine start end if start and end have already been set
        if self.start and self.end:
            return

        if not self.trades:
            logger.warning(f'There were no trades found in the backtest.')
            if not self.start and not self.end:
                raise RuntimeError(
                    'You must specify a start and end timeframe when no time range get be determined '
                    'from the first and last trade.'
                )

        first_trade = None
        last_trade = None

        # calculate the start and end based on the first and last trade
        if self.trades:
            for pair, trades in self.trades.items():
                open_date = pd.Timestamp(trades[0]['open_date'])
                if not first_trade or open_date < first_trade:
                    first_trade = open_date

        if self.trades:
            for pair, trades in self.trades.items():
                close_date = pd.Timestamp(trades[-1]['close_date'])
                if not last_trade or close_date > last_trade:
                    last_trade = close_date

        self.start = (first_trade - self.startup_time_delta).to_pydatetime()
        self.end = last_trade.to_pydatetime()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def trades(self) -> dict:
        if self._trades:
            return self._trades
        trades = self.get_trades(self.strategy)
        self._trades = self._normalize_trade_format(trades)
        return self._trades

    @property
    def replay_config(self) -> dict:
        if self._replay_config:
            return self._replay_config

        replay_config_callback = self.get_backtest_view_config_callback()
        self._replay_config = replay_config_callback(self.pair)
        return self._replay_config

    @property
    def startup_time_delta(self) -> pd.Timedelta:
        if self._startup_time_delta:
            return self._startup_time_delta
        self._startup_time_delta = self.get_startup_time_delta()
        return self._startup_time_delta

    @property
    def dataframes(self) -> Dict[str, pd.DataFrame]:
        if self._dataframes:
            return self._dataframes

        for candle_plot in self.replay_config['candle_plots']:
            pair = candle_plot['pair']
            self._dataframes[pair] = self.get_evaluated_strategy(
                pair=pair,
                start=self.start,
                end=self.end,
                timeframe=self.timeframe,
                download=self.download,
            )
        return self._dataframes

    @abstractmethod
    def get_trades(
            self,
            strategy: str
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_candles(
            self,
            pair: str,
            start: datetime = datetime.now(tz=timezone.utc) - timedelta(days=90),
            end: datetime = datetime.now(tz=timezone.utc),
            download: bool = True,
            timeframe: Timeframe = Timeframe.HOUR
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_evaluated_strategy(
            self,
            pair: str,
            start: datetime = datetime.now(tz=timezone.utc) - timedelta(days=90),
            end: datetime = datetime.now(tz=timezone.utc),
            timeframe: Timeframe = Timeframe.HOUR,
            download: bool = True
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_backtest_view_config_callback(self) -> Callable:
        raise NotImplementedError

    @abstractmethod
    def get_startup_time_delta(self) -> pd.Timedelta:
        raise NotImplementedError

    @abstractmethod
    def set_strategy_instance(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _normalize_trade_format(
            self,
            trades: dict
    ) -> dict:
        raise NotImplementedError

