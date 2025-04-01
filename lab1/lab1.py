import builtins
import difflib
import inspect
import os

# Hack that modifies the built-in `open` function in such a way that
# an assignment can be done even at other places than the server.

def find_filename(filename):
    if os.path.exists(filename):
        return filename
    path = os.path.dirname(inspect.getfile(inspect.currentframe()))
    path = os.path.join(path, os.path.basename(filename))
    if os.path.exists(path):
        return path
    return filename

old_open = builtins.open

def new_open(filename, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    return old_open(find_filename(filename), mode, buffering, encoding, errors, newline, closefd, opener)

builtins.open = new_open

# Lab code proper

def _diff(gold_tokens, pred_tokens):
    """Iterator over pairs describing longest differing subsequences
    within `gold_tokens` and `pred_tokens`.

    """
    matcher = difflib.SequenceMatcher(None, gold_tokens, pred_tokens)
    a_lo = b_lo = 0
    for a_hi, b_hi, n in matcher.get_matching_blocks():
        if a_lo < a_hi or b_lo < b_hi:
            yield gold_tokens[a_lo:a_hi], pred_tokens[b_lo:b_hi]
        a_lo = a_hi + n
        b_lo = b_hi + n

def diff(gold_tokens, pred_tokens):
    """Return a list of pairs describing longest differing subsequences
    within `gold_tokens` and `pred_tokens`.

    """
    return list(_diff(gold_tokens, pred_tokens))

def _n_matches(gold_tokens, pred_tokens):
    """Return the number of elements that match within `gold_tokens` and
    `pred_tokens`.

    """
    matcher = difflib.SequenceMatcher(None, gold_tokens, pred_tokens)
    return sum(match.size for match in matcher.get_matching_blocks())

def n_errors(gold_tokens, pred_tokens):
    """Return the number of errors in the tokenization given by
    `pred_tokens`, relative to the gold-standard tokenization given by
    `gold_tokens`.

    """
    return len(gold_tokens) + len(pred_tokens) - 2 * _n_matches(gold_tokens, pred_tokens)

def precision(gold_tokens, pred_tokens):
    """Return the precision of the tokenization given by `pred_tokens`,
    relative to the gold-standard tokenization given by `gold_tokens`.

    """
    n_pred_tokens = len(pred_tokens)
    n_matches = _n_matches(gold_tokens, pred_tokens)
    return n_matches / n_pred_tokens if n_pred_tokens > 0 else float('NaN')

def recall(gold_tokens, pred_tokens):
    """Return the recall of the tokenization given by `pred_tokens`,
    relative to the gold-standard tokenization given by `gold_tokens`.

    """
    n_gold_tokens = len(gold_tokens)
    n_matches = _n_matches(gold_tokens, pred_tokens)
    return n_matches / n_gold_tokens if n_gold_tokens > 0 else float('NaN')
