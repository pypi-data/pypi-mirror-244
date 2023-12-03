from fabric import ThreadingGroup
from sdj_remotetools.utils import get_parser, get_std_consoles
from fabric.exceptions import GroupException
from rich.panel import Panel
from rich.text import Text
from rich._emoji_codes import EMOJI
from pathlib import Path

EMOJI.clear()               # Workaround to avoid emoji substitution

PARSER_CONFIG = {
    'header': {
        'prog': 'rexec',
        'description': 'Executes command on a list of remote hosts and output result.'
    },
    'args': [
        {
            'name_or_flags': ['remote_hosts'],
            'type': str,
            'help': 'A coma separated list of hosts. Ex: root@127.0.0.1,joe@example.org',
        },
        {
            'name_or_flags': ['command'],
            'type': str,
            'help': 'The command to execute on remote hosts',
        },
        {
            'name_or_flags': ['-u', '--username'],
            'type': str,
            'help': 'Username for ssh authentication. Must be the same for all hosts',
        },
        {
            'name_or_flags': ['-p', '--password'],
            'type': str,
            'help': 'Password for ssh authentication. Must be the same for all hosts',
        },
        {
            'name_or_flags': ['-o', '--output'],
            'type': str,
            'help': 'Write output to this file. It not set output will print on stdout',
        },
        {
            'name_or_flags': ['-s', '--syntax_highlight'],
            'action': 'store_true',
            'default': False,
            'help': 'Enable console syntax highlighting',
        },
    ]
}


def rexec():
    """Execute a command on a list of remote hosts.

    Arguments:
        remote_hosts (str): A comma separated list of hosts.
        command (str):      The command to execute.
        password (str):     The password used for SSH authentication if needed.
        output (str):       Path to the file to write the output

    """
    # Build the command line arguments parser
    parser = get_parser(PARSER_CONFIG)

    # Parse command line arguments
    args = parser.parse_args()

    # Build stdout and stdin consoles
    stdout, stderr = get_std_consoles(highlight=args.syntax_highlight)

    remote_hosts = args.remote_hosts.split(',')
    password = args.password

    ssh_args = {
        'connect_kwargs': {'password': password}
    }
    if args.username is not None:
        ssh_args['user'] = args.username

    try:
        group = ThreadingGroup(*remote_hosts, **ssh_args).run(args.command, hide=True)
    except GroupException as e:
        group = e.result
    except ValueError as e:
        stderr.print(f"ERROR: {e}")
        exit(1)

    errors = {}
    outputs = {}

    for connection, result in group.items():
        if isinstance(result, Exception):
            errors[connection.host] = result
        else:
            outputs[connection.host] = result

    if errors:
        failed_hosts = [f"{host}: {errors[host]}" for host in errors]
        stdout.print(Panel('\n'.join(sorted(failed_hosts)), title="[yellow]WARNINGS", expand=False,
                           title_align='left', highlight=args.syntax_highlight, safe_box=True))

    if args.output is None:
        for host in outputs:
            stdout.print(Panel(Text(outputs[host].stdout.strip(), ), title=f"[green]{host} => {args.command}", expand=False,
                               title_align='left', highlight=args.syntax_highlight, safe_box=True))

    else:
        content = []
        if errors:
            content.append("The execution failed on the following hosts:\n")
            for host in sorted(errors):
                content.append(f"{host}: {errors[host]}\n")
            content.append("\n\n")

        for host in outputs:
            content.append(f"---------- BEGIN {host} ----------\n")
            content.append(outputs[host].stdout)
            content.append(f"----------- END {host} -----------\n")
            content.append("\n")

        try:
            with open(Path(args.output), 'w') as output_file:
                output_file.writelines(content)
        except (PermissionError, FileNotFoundError) as e:
            stderr.print(f"ERROR: {e}")
