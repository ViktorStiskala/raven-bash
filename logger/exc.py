from pprint import pprint

a = {'exception': {'values': [{'module': 'builtins', 'type': 'ZeroDivisionError', 'stacktrace': {'frames': [
    {'filename': 'raven_logger.py', 'module': '__main__', 'context_line': '        1 / 0', 'abs_path': 'raven_logger.py',
     'vars': {'__loader__': '<_frozen_importlib.SourceFileLoader object at 0x1007d24e0>', 'client': '<raven.base.Client object at 0x1011dfe48>', '__package__': None,
              '__spec__': None, '__file__': "'raven_logger.py'", '__name__': "'__main__'", '__builtins__': "<module 'builtins' (built-in)>", '__cached__': None,
              'argparse': "<module 'argparse' from '/usr/local/Cellar/python3/3.4.3/Frameworks/Python.framework/Versions/3.4/lib/python3.4/argparse.py'>", '__doc__': None,
              'parser': "ArgumentParser(prog='raven_logger.py', usage=None, description='Send error to Sentry', formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)",
              'args': "Namespace(culprit='test', dsn='lol', message='test')", 'Client': "<class 'raven.base.Client'>"}, 'pre_context': ['    args = parser.parse_args()', '',
                                                                                                                                        "    client = Client(dsn='https://7f305642c44a4278bfe5443b459eb199:1c6e69c9f077409583858a7843e8823d@sentry.stiskala.cz/3')",
                                                                                                                                        '', '    try:'], 'lineno': 15,
     'function': '<module>', 'post_context': ['    except ZeroDivisionError:', '        client.captureException()']}]}, 'value': 'division by zero'}]}, 'level': 40}
pprint(a)
