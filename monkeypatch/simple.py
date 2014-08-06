import hy.cmdline
import hy.lex

# commence the monkey patching!

from pygments.lexers import get_lexer_by_name
hy_lexer = lambda: get_lexer_by_name('hylang')
import bpython._py3compat
bpython._py3compat.PythonLexer = hy_lexer

import bpython.repl
bpython.repl.Repl.ps1 = property(lambda self: '=> ')

import shlex, tempfile, subprocess
def send_to_external_editor(self, text, filename=None):
    """Returns modified text from an editor, or the oriignal text if editor exited with non-zero"""
    editor_args = shlex.split(self.config.editor)
    with tempfile.NamedTemporaryFile(suffix='.hy') as temp:
        temp.write(text)
        temp.flush()
        if subprocess.call(editor_args + [temp.name]) == 0:
            with open(temp.name) as f:
                return f.read()
        else:
            return text
bpython.repl.Repl.send_to_external_editor = send_to_external_editor

import bpython.curtsiesfrontend.repl
def buffer_finished_will_parse(self):
    """Returns a tuple of whether the buffer could be complete and whether it will parse

    True, True means code block is finished and no predicted parse error
    True, False means code block is finished because a parse error is predicted
    False, True means code block is unfinished
    False, False isn't possible - an predicted error makes code block done"""
    try:
        hy.lex.tokenize('\n'.join(self.buffer))
    except hy.lex.PrematureEndOfInput:
        finished = False
        code_will_parse = True
    except hy.lex.LexException:
        finished = True
        code_will_parse = False
    else:
        finished = True
        code_will_parse = True
    return finished, code_will_parse
bpython.curtsiesfrontend.repl.Repl.buffer_finished_will_parse = buffer_finished_will_parse

