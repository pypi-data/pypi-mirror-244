import os
from re import T
import art
import typer
import logging
import tomlkit
import backtest_view
import importlib.metadata
from pathlib import Path
from rich import print
from rich.text import Text
from typing import Optional, List
from backtest_view.constants import Timeframe, Envs
from typer import rich_utils
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing_extensions import Annotated
from backtest_view.draw.plot import Plot

# load in the env file if there is one
load_dotenv('.env')

# monkey patch this function, so we can add in header ascii art
rich_format_help = rich_utils.rich_format_help


def override_help(*args, **kwargs):
    text = Text(art.text2art('BACKTEST VIEW'))
    text.stylize("bold red")
    print(text)
    rich_format_help(*args, **kwargs)


rich_utils.rich_format_help = override_help

# create cli app
app = typer.Typer(
    pretty_exceptions_show_locals=False
)


def validate_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if not value:
        raise typer.BadParameter(
            f"You must set this or the environment variable '{param.envvar}'"
        )
    return value


project_folder_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.PROJECT_FOLDER.description,
    envvar=Envs.PROJECT_FOLDER.value
)

config_path_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.CONFIG_PATH.description,
    envvar=Envs.CONFIG_PATH.value
)

strategy_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.STRATEGY.description,
    envvar=Envs.STRATEGY.value
)

pair_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.PAIR.description,
    envvar=Envs.PAIR.value
)

timeframe_option = typer.Option(
    Timeframe.HOUR.value,
    callback=validate_callback,
    show_default=False,
    help=Envs.TIME_FRAME.description,
    envvar=Envs.TIME_FRAME.value
)

start_option = typer.Option(
    (datetime.now(tz=timezone.utc) - timedelta(days=30)),
    help="The date and time to start viewing the backtest"
)

end_option = typer.Option(
    datetime.now(tz=timezone.utc),
    help="The date and time to end viewing the backtest"
)

show_subplots_option = typer.Option(
    True,
    help="Whether to show the subplots."
)

replay_option = typer.Option(
    True,
    help="Whether to replay the backtest or show the full result at once."
)

download_option = typer.Option(
    True,
    help="Try and download missing data each run. Set this to false if you the tool to launch faster."
)

isolate_pair_option = typer.Option(
    None,
    help="Try and download missing data each run. Set this to false if you the tool to launch faster."
)


def get_version():
    """
    Gets the package version.
    """
    project_file_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'pyproject.toml')
    if os.path.exists(project_file_path):
        with open(project_file_path, "rb") as project_file:
            data = tomlkit.load(project_file)
            return data.get('tool', {}).get('poetry', {}).get('version', '0.0.1')
    return importlib.metadata.version(backtest_view.__name__)


def version_callback(value: bool):
    """
    Shows the current cli version

    :param bool value: Whether the version flag was passed.
    """
    if value:
        print(f"Backtest View CLI Version: {get_version()}")
        raise typer.Exit()


@app.callback(no_args_is_help=True)
def callback(version: Optional[bool] = typer.Option(None, "--version", callback=version_callback)):
    """
    The Backtest View CLI tool launches a GUI that visualizes your backtests.
    """


@app.command()
def freqtrade(
        project_folder: Path = project_folder_option,
        config_path: Path = config_path_option,
        strategy: str = strategy_option,
        pair: str = pair_option,
        timeframe: str = timeframe_option,
        start: datetime = start_option,
        end: datetime = end_option,
        download: bool = download_option,
        replay: bool = replay_option,
        show_subplots: bool = show_subplots_option,
        isolate_pair: Optional[str] = isolate_pair_option
):
    """
    Plots a backtest from the freqtrade algo trading framework.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)

    from backtest_view.data_source.backtest.freqtrade import FreqtradeBacktestDataSource

    data_source = FreqtradeBacktestDataSource(
        config=config_path,
        strategy=strategy,
        pair=pair,
        timeframe=Timeframe(timeframe),
        project_folder=project_folder,
        download=download,
        start=start,
        end=end
    )

    plot = Plot(
        data_sources=[
            data_source
        ],
        timeframe=Timeframe(timeframe),
        show_subplots=show_subplots,
        replay=replay,
        isolate_pair=isolate_pair
    )

    plot.show()

