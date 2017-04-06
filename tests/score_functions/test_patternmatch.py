"""Testing the pattern match score fuction."""
from cckrypto.score_functions.patternmatch import PatternMatch


def test_patternmatch_with_word_found():
    """Test pattern match using single word succeeds"""
    match_scorer = PatternMatch("flag")
    assert match_scorer("flag{example}") == 0
    assert match_scorer("This is the flag") == 0


def test_patternmatch_with_word_notfound():
    """Test pattern match using single word fails.s"""
    match_scorer = PatternMatch("flag")
    assert match_scorer("junk") == -1
    assert match_scorer("Flag") == -1


def test_patternmatch_with_regex_found():
    match_scorer = PatternMatch("flag{.*}")
    assert match_scorer("flag{exampletest}") == 0
    assert match_scorer("flag{l33tH4ck0r}") == 0


def test_patternmatch_with_regex_found():
    match_scorer = PatternMatch("flag{.*}")
    assert match_scorer("This is a flag") == -1
    assert match_scorer("Incorrect") == -1
