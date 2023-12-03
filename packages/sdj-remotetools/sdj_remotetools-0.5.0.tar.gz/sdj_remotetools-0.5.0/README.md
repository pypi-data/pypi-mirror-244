![](https://img.shields.io/badge/python-3.9-blue) ![](https://img.shields.io/badge/python-3.10-blue) ![](https://img.shields.io/badge/python-3.11-blue) ![](https://img.shields.io/badge/python-3.12-blue)
# SDJ-REMOTETOOLS

## Description
`sdj-remotetools` is a python collection of tools working through SSH.

## Tools
All tools handle SSH connection using Paramiko.

### rcat
Works like 'cat' command but for remote files through SSH and with few enhancements
```
usage: rcat [-h] [-p] [-e ENCODING] [-b] [-s] remote_files [remote_files ...]

Works like 'cat' but through SSH.

positional arguments:
  remote_files          SSH path to the remote files, space separate, ie: joe@remote.host:/path/to/file

options:
  -h, --help            show this help message and exit
  -p, --password        Ask user for password
  -e ENCODING, --encoding ENCODING
                        Character encoding, ie: utf-8 (default)
  -b, --border          Draw border around the content
  -s, --syntax_highlight
                        Enable console syntax highlighting
```

### rlist
Works like 'ls' command but for remote path through SSH (with fewer options).
```
usage: rlist [-h] [-a] [-l] [-p] ssh_url

Works almost liks 'ls' but through SSH

positional arguments:
  ssh_url         SSH path to a remote file or directory, space separate, ie: joe@remote.host:/remote/path

options:
  -h, --help      show this help message and exit
  -a, --all       Show hidden and 'dot' files. Default: False
  -l, --long      Display extended file metadata as a table
  -p, --password  Ask user for password. Default: False
```

### rexec
Executes command on a list of remote hosts and output results on screen or to a file.
```
usage: rexec [-h] [-u USERNAME] [-p PASSWORD] [-o OUTPUT] [-s] remote_hosts command

Executes command on a list of remote hosts and output result.

positional arguments:
  remote_hosts          A coma separated list of hosts. Ex: root@127.0.0.1,joe@example.org
  command               The command to execute on remote hosts

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username for ssh authentication. Must be the same for all hosts
  -p PASSWORD, --password PASSWORD
                        Password for ssh authentication. Must be the same for all hosts
  -o OUTPUT, --output OUTPUT
                        Write output to this file. It not set output will print on stdout
  -s, --syntax_highlight
                        Enable console syntax highlighting
```
