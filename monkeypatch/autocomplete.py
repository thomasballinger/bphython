from bpython.autocomplete import *
def get_completer(cursor_offset, current_line, locals_, argspec, full_code, mode, complete_magic_methods):
    """Returns a list of matches and a class for what kind of completion is happening

    If no completion type is relevant, returns None, None

    argspec is an output of inspect.getargspec
    """

    kwargs = {'locals_':locals_, 'argspec':argspec, 'full_code':full_code,
              'mode':mode, 'complete_magic_methods':complete_magic_methods}

    # mutually exclusive if matches: If one of these returns [], try the next one
    for completer in [DictKeyCompletion]:
        matches = completer.matches(cursor_offset, current_line, **kwargs)
        if matches:
            return sorted(set(matches)), completer

    # mutually exclusive matchers: if one returns [], don't go on
    for completer in [StringLiteralAttrCompletion, ImportCompletion,
            FilenameCompletion, MagicMethodCompletion, GlobalCompletion]:
        matches = completer.matches(cursor_offset, current_line, **kwargs)
        if matches is not None:
            return sorted(set(matches)), completer

    matches = AttrCompletion.matches(cursor_offset, current_line, **kwargs)

    # cumulative completions - try them all
    # They all use current_word replacement and formatting
    current_word_matches = []
    for completer in [AttrCompletion, ParameterNameCompletion]:
        matches = completer.matches(cursor_offset, current_line, **kwargs)
        if matches is not None:
            current_word_matches.extend(matches)

    if len(current_word_matches) == 0:
        return None, None
    return sorted(set(current_word_matches)), AttrCompletion
import bpython.autocomplete
bpython.autocomplete.get_completer = get_completer

