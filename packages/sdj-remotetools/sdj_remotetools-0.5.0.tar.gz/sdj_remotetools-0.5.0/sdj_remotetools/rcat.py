import getpass
import paramiko
import sys
from getpass import getpass
from rich.panel import Panel
from sdj_remotetools.utils import get_parser, ssh_url_type, get_std_consoles


PARSER_CONFIG = {
    'header': {
        'prog': 'rcat',
        'description': 'Works like \'cat\' but through SSH.'
    },
    'args': [
        {
            'name_or_flags': ['remote_files'],
            'nargs': '+',
            'type': ssh_url_type,
            'help': 'SSH path to the remote files, space separate, ie: joe@remote.host:/path/to/file',
        },
        {
            'name_or_flags': ['-b', '--border'],
            'action': 'store_true',
            'default': False,
            'help': 'Draw border around the content',
        },
        {
            'name_or_flags': ['-e', '--encoding'],
            'type': str,
            'default': 'utf-8',
            'help': 'Character encoding, ie: utf-8 (default)',
        },
        {
            'name_or_flags': ['-p', '--password'],
            'action': 'store_true',
            'default': False,
            'help': 'Ask user for password',
        },
        {
            'name_or_flags': ['-s', '--syntax_highlight'],
            'action': 'store_true',
            'default': False,
            'help': 'Enable console syntax highlighting',
        },
    ]
}


def get_remote_file_content(remote_host: str, username: str, password: bool, path_to_file: str,
                            encoding: str = 'utf8') -> str:
    """Gets and returns the content of a remote file through SSH

    Arguments:
        remote_host (str):  address or hostname of the remote host
        username (str):     username used to connect to the remote host
        password (bool):    should password authentication be used or not, default: False
        path_to_file (str): path to the file on the remote host
        encoding (str):     encoding to use to read the file content, default: 'utf-8'

    Returns:
        Content of the remote file as a string.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if password:
            user_password = getpass(f'({username}@{remote_host}) Password: ')
            ssh.connect(hostname=remote_host, username=username, password=user_password)
        else:
            ssh.connect(hostname=remote_host, username=username)

        ftp = ssh.open_sftp()
        if str(ftp.stat(path_to_file)).startswith('d'):
            raise FileNotFoundError('Cannot read a directory')
        content = ftp.open(path_to_file).read().decode(encoding)
        ssh.close()
        return content

    except (
            paramiko.SSHException,
            paramiko.AuthenticationException,
            paramiko.SFTPError,
            FileNotFoundError,
            PermissionError,
    ):
        raise


def rcat():
    """rcat command main routine"""

    # Build the command line arguments parser
    parser = get_parser(PARSER_CONFIG)

    # Parse command line arguments
    args = parser.parse_args()

    # Build stdout and stdin consoles
    stdout, stderr = get_std_consoles(highlight=args.syntax_highlight)

    # Loops through each SSH url passed to rcat
    for remote_file_args in args.remote_files:
        ssh_args = remote_file_args
        ssh_args.update({'password': args.password, 'encoding': args.encoding})

        try:
            # Get content from remote file and add it to the outputs list
            file_content = get_remote_file_content(**ssh_args)
            if args.border:
                file_content = Panel(file_content, highlight=args.syntax_highlight, expand=False,
                                     title=remote_file_args['path_to_file'])
            stdout.print(file_content)
        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            stderr.print(f"SSH ERROR: {e} -> {remote_file_args['username']}@{remote_file_args['remote_host']} "
                         f"using password: {'Yes' if args.password else 'No'}", style="red")
            sys.exit(71)
        except paramiko.SFTPError as e:
            stderr.print(f"SFTP ERROR: {e}", style="red")
            sys.exit(71)
        except (FileNotFoundError, PermissionError) as e:
            stderr.print(f"FILE ERROR: {e} -> {remote_file_args['path_to_file']}", style="red")
            sys.exit(e.errno)
