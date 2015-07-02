import argparse
import re
from collections import namedtuple
import configparser
import sys
import os
from raven import Client


CONFIG_FILE = '/etc/raven-bash.conf'


class LoggerClient:
    def __init__(self, dsn):
        self._client = Client(dsn=dsn, context={})

    def _process_sourcefile(self, file_path, line_number, context_lines=10):
        FileContext = namedtuple('FileContext', ['pre_context', 'context', 'post_context', 'local_vars'])

        start = max(line_number - context_lines, 0)
        stop = line_number + context_lines

        pre_context = []
        post_context = []
        local_vars = []
        context = None

        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                current_line = i + 1
                if current_line < start:
                    continue
                elif current_line > stop:
                    break

                # search for variable declaration
                var = re.match(r'^(?P<name>[a-z]{1}\w*)=\S', line, re.IGNORECASE)
                if var:
                    local_vars.append(var.group('name'))

                if current_line < line_number:
                    pre_context.append(line.rstrip('\n'))
                elif current_line == line_number:
                    context = line.rstrip('\n')
                else:
                    post_context.append(line.rstrip('\n'))

        return FileContext(pre_context, context, post_context, local_vars)

    def _get_declares(self, declare_output, local_vars):
        """Parse `declare -p` output and get values from local variables"""
        out = {}
        for var in local_vars:
            m = re.search(r'^(?P<name>' + re.escape(var) + r')=(?P<value>\S.*)', declare_output, re.MULTILINE)
            if m:
                out[m.group('name')] = m.group('value')

        return out

    def capture(self, shell_args):
        frame = {
            'filename': shell_args.script,
            'function': shell_args.function or 'main',
            'lineno': shell_args.lineno,
            'module': shell_args.command,
            'vars': {},
        }

        if shell_args.pwd:
            abspath = os.path.abspath(os.path.join(shell_args.pwd, shell_args.script))
            filename = os.path.basename(abspath)

            try:
                srcfile = self._process_sourcefile(abspath, shell_args.lineno)
                if shell_args.declares:
                    frame['vars'] = self._get_declares(shell_args.declares, srcfile.local_vars)

                frame.update(
                    filename=filename,
                    abs_path=abspath,
                    pre_context=srcfile.pre_context,
                    context_line=srcfile.context,
                    post_context=srcfile.post_context
                )
            except FileNotFoundError:
                sys.stderr.write('Could not process file "{}"\n'.format(abspath))

        data = {
            'exception': {
                'values': [{
                    'module': 'builtins',
                    'stacktrace': {
                        'frames': [frame]
                    },
                    'type': shell_args.script,
                    'value': 'error on line {}'.format(shell_args.lineno) if not shell_args.function else "error in '{}' on line {}".format(shell_args.function, shell_args.lineno)
                }]
            },
        }

        # add ENV vars and stderr if provided
        extra = {}
        if shell_args.env:
            extra['environment'] = dict([item.split('=', maxsplit=1) for item in shell_args.env.split('\n')])

        if shell_args.stderr:
            extra['stderr'] = shell_args.stderr

        self._client.capture('raven.events.Exception', data=data, extra=extra)

def main():
    try:
        dsn = os.environ['SENTRY_DSN']
    except KeyError:
        config = configparser.ConfigParser()
        config.sections()
        config.read(CONFIG_FILE)

        dsn = config['DEFAULT'].get('SENTRY_DSN')

    if not dsn:
        sys.stderr.write('Missing SENTRY_DSN config from {}\n'.format(CONFIG_FILE))
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Send error to Sentry')

    parser.add_argument('--env', help='Script environment')
    parser.add_argument('--cmdline-args', help='Command line arguments')
    parser.add_argument('--stderr', help='Standard error output')
    parser.add_argument('--pwd', help='Working directory')
    parser.add_argument('--function', help='Error function')
    parser.add_argument('--declares', help='declare -p output')

    parser.add_argument('script', help='Source script')
    parser.add_argument('command', help='Error command')
    parser.add_argument('lineno', type=int, help='Error line number')

    args = parser.parse_args()

    client = LoggerClient(dsn)
    client.capture(args)

if __name__ == '__main__':
    main()
