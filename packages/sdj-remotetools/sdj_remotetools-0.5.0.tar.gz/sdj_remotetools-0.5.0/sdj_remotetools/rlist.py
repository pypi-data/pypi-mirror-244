import paramiko
import sys
from getpass import getpass
from rich.columns import Columns
from sdj_remotetools.utils import get_parser, get_std_consoles, ssh_url_type

PARSER_CONFIG = {
    'header': {
        'prog': 'rlist',
        'description': 'Works almost like \'ls\' but through SSH'
    },
    'args': [
        {
            'name_or_flags': ['ssh_url'],
            'type': ssh_url_type,
            'help': 'SSH path to a remote file or directory, space separate, ie: joe@remote.host:/remote/path',
        },
        {
            'name_or_flags': ['-a', '--all'],
            'action': 'store_true',
            'default': False,
            'help': 'Show hidden and \'dot\' files. Default: False',
        },
        {
            'name_or_flags': ['-l', '--long'],
            'action': 'store_true',
            'default': False,
            'help': 'Display extended file metadata as a table',
        },
        {
            'name_or_flags': ['-p', '--password'],
            'action': 'store_true',
            'default': False,
            'help': 'Ask user for password. Default: False',
        },
    ]
}


def get_remote_list_content(remote_host: str, username: str, password: bool, path_to_file: str,
                            show_all: bool = False):
    """Gets and returns the list of element for the remote path through SSH

     Arguments:
         remote_host (str):     address or hostname of the remote host
         username (str):        username used to connect to the remote host
         password (bool):       should password authentication be used or not. Default: False
         path_to_file (str):    path to the file on the remote host
         show_all (bool):            include hidden \'dotter\' files. Default: False

     Returns:
         A list of elements found int the remote path.
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

        content = []

        # If remote_path is a file, get its attribute
        if not str(ftp.stat(path_to_file)).startswith('d'):
            file_attr = ftp.stat(path_to_file)
            file_attr.filename = path_to_file.split('/')[-1]
            content.append(file_attr)

        # If it's a directory remove hidden elements if show_all=False
        else:
            if show_all:
                content = ftp.listdir_attr(path_to_file)
            else:
                content = [element for element in ftp.listdir_attr(path_to_file)
                           if not element.filename.startswith('.')]
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


def rlist():
    """rlist command main routine"""

    # Build the command line arguments parser
    parser = get_parser(PARSER_CONFIG)

    # Parse command line arguments
    args = parser.parse_args()

    # Build stdout and stdin consoles
    stdout, stderr = get_std_consoles()

    # Sets SSH arguments
    ssh_args = args.ssh_url
    ssh_args.update({'password': args.password, 'show_all': args.all})

    # Get remote content for the given path
    try:
        directory_content = get_remote_list_content(**ssh_args)

    except (paramiko.AuthenticationException, paramiko.SSHException) as e:
        stderr.print(f"SSH ERROR: {e} -> {ssh_args['username']}@{ssh_args['remote_host']} "
                     f"using password: {'Yes' if args.password else 'No'}", style="red")
        sys.exit(71)
    except paramiko.SFTPError as e:
        stderr.print(f"SFTP ERROR: {e}", style="red")
        sys.exit(71)
    except (FileNotFoundError, PermissionError) as e:
        stderr.print(f"FILE ERROR: {e} -> {ssh_args['path_to_file']}", style="red")
        sys.exit(e.errno)

    else:
        output = ""

        # No need to sort if only one element in the list
        if len(directory_content) > 1:
            directory_content = sorted(directory_content, key=lambda x: x.filename.lower())

        # Display elements arranged in columns (default behavior)
        if not args.long:
            output = Columns(
                [element.filename for element in directory_content],
                column_first=True,
                padding=(0, 2)
            )

        # Display long information in list format
        elif args.long:
            output = '\n'.join([str(element) for element in directory_content])

        stdout.print(output)
