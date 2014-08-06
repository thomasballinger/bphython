from __future__ import absolute_import

import hy.cmdline

import monkeypatch # does hy monkeypatching

import sys
import code
import logging
from optparse import Option

from bpython.translations import _
from bpython.curtsiesfrontend.coderunner import SystemExitFromCodeGreenlet
from bpython import args as bpargs

repl = None # global for `from bpython.curtsies import repl`
#WARNING Will be a problem if more than one repl is ever instantiated this way

from bpython.curtsies import mainloop

def main(args=None, locals_=None, banner=None):
    config, options, exec_args = bpargs.parse(args, (
        'scroll options', None, [
            Option('--log', '-L', action='store_true',
                help=_("log debug messages to bpython.log")),
            Option('--type', '-t', action='store_true',
                help=_("enter lines of file as though interactively typed")),
            ]))
    if options.log:
        handler = logging.FileHandler(filename='bpython.log')
        logging.getLogger('curtsies').setLevel(logging.DEBUG)
        logging.getLogger('curtsies').addHandler(handler)
        logging.getLogger('curtsies').propagate = False
        logging.getLogger('bpython').setLevel(logging.DEBUG)
        logging.getLogger('bpython').addHandler(handler)
        logging.getLogger('bpython').propagate = False
    else:
        logging.getLogger('bpython').setLevel(logging.WARNING)

    interp = hy.cmdline.HyREPL()
    paste = None
    if exec_args:
        assert options, "don't pass in exec_args without options"
        exit_value = 0
        if options.type:
            paste = curtsies.events.PasteEvent()
            sourcecode = open(exec_args[0]).read()
            paste.events.extend(sourcecode)
        else:
            try:
                interp = code.InteractiveInterpreter(locals=locals_)
                bpargs.exec_code(interp, exec_args)
            except SystemExit as e:
                exit_value = e.args
            if not options.interactive:
                raise SystemExit(exit_value)
    else:
        sys.path.insert(0, '') # expected for interactive sessions (vanilla python does it)

    mainloop(config, locals_, banner, interp, paste, interactive=(not exec_args))

if __name__ == '__main__':
    sys.exit(main())
