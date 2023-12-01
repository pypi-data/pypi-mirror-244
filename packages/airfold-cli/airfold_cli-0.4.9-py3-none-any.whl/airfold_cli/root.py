from functools import wraps

import typer
from airfold_common.log import log
from rich.traceback import install

from airfold_cli.cli import AirfoldTyper
from airfold_cli.error import AirfoldError
from airfold_cli.options import with_global_options
from airfold_cli.version import VersionOption

install()

app = AirfoldTyper(no_args_is_help=True, short_help="-h", rich_markup_mode="rich")


def exit_with_error(message, code=1, **kwargs):
    """
    Print an error message and exit with a non-zero code
    """
    return app.exit_with_error(message, code, **kwargs)


def exit_with_success(message, **kwargs):
    """
    Print a success message and exit with a zero code
    """
    return app.exit_with_success(message, **kwargs)


def print_warning(message, **kwargs):
    """
    Print a warning message
    """
    return app.print_warning(message, **kwargs)


def print_error(message, **kwargs):
    """
    Print an error message
    """
    return app.print_error(message, **kwargs)


def catch_airfold_error():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AirfoldError as e:
                log.error(e)
                exit_with_error(str(e))
            except Exception as e:
                raise e

        return wrapper

    return decorator


def is_interactive():
    """Check if the console is interactive."""
    return app.is_interactive()


@app.callback()
def default(
    version: bool = VersionOption,
) -> None:
    pass


@app.callback()
@with_global_options
def main(
    ctx: typer.Context,
    version: bool = VersionOption,
):
    app.apply_options(ctx)


def entrypoint():
    """Application entrypoint."""

    app()


if __name__ == "__main__":
    entrypoint()
