import argparse
import re
from argparse import ArgumentTypeError as ArgparseArgumentError
from rich.console import Console


def get_parser(parser_configuration: dict) -> argparse.ArgumentParser:
    """Builds and returns a ArgumentParser based on the given configuration"""
    parser = argparse.ArgumentParser(**parser_configuration['header'])
    for arg in parser_configuration['args']:
        flags = arg.pop('name_or_flags')
        parser.add_argument(*flags, **arg)
    return parser


def get_std_consoles(highlight: bool = False) -> tuple[Console, Console]:
    """Returns a tuple of rich consoles

    Arguments:
        highlight (bool): Enable or not syntax highlighting for stdout Rich Console

    Returns:
        A tuple of rich Console

        Example:
            stdout, stderr = get_sdt_consoles(highlight=True)
    """
    return Console(highlight=highlight), Console(stderr=True, highlight=False)


def ssh_url_type(ssh_url: str) -> dict[str]:
    """Parses an SSH url and returns a dictionary of values

    Arguments:
        ssh_url (str): an SSH url, ie: user@host.tld:/path/to/file

    Returns:
        A dictionary of the url fields, ie:
        {
            'username': 'user',
            'remote_host': 'host.tld',
            'path_to_file': '/path/to/file',
        }
    """
    url_regex = '^(?P<username>\S+)@(?P<remote_host>\S+):(?P<path_to_file>/(\S+)?)'
    result = re.search(url_regex, ssh_url)

    if result is None:
        raise ArgparseArgumentError(f'{ssh_url!r} is not a valid SSH url')

    return result.groupdict()
