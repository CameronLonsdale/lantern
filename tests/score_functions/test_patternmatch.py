"""Testing the pattern match score fuction."""
from cckrypto.score_functions.patternmatch import PatternMatch


def test_patternmatch_with_word_found():
    """Test pattern match using single word succeeds"""
    matcher = PatternMatch("flag")
    assert matcher.score("flag{example}") == 0
    assert matcher.score("This is the flag") == 0


def test_patternmatch_with_word_notfound():
    """Test pattern match using single word fails.s"""
    matcher = PatternMatch("flag")
    assert matcher.score("junk") == -1
    assert matcher.score("Flag") == -1


def test_patternmatch_with_regex_found():
    match = PatternMatch("flag{.*}")
    assert matcher.score("flag{exampletest}") == 0
    assert matcher.score("flag{l33tH4ck0r}") == 0


def test_patternmatch_with_regex_found():
    matcher = PatternMatch("flag{.*}")
    assert matcher.score("This is a flag") == -1
    assert matcher.score("Incorrect") == -1
