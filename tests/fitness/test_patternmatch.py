"""Test the pattern match score fuction"""

from lantern.fitness import PatternMatch


def test_patternmatch_with_word_found():
    """Testing pattern match using single word success"""
    match_scorer = PatternMatch("flag")
    assert match_scorer("flag{example}") == 0
    assert match_scorer("This is the flag") == 0


def test_patternmatch_with_word_notfound():
    """Testing pattern match using single word failure"""
    match_scorer = PatternMatch("flag")
    assert match_scorer("junk") == -1
    assert match_scorer("Flag") == -1


def test_patternmatch_with_regex_found():
    """Testing pattern match using regular expression success"""
    match_scorer = PatternMatch("flag{.*}")
    assert match_scorer("flag{exampletest}") == 0
    assert match_scorer("flag{l33tH4ck0r}") == 0


def test_patternmatch_with_regex_not_found():
    """Test pattern match using regular expression faillure"""
    match_scorer = PatternMatch("flag{.*}")
    assert match_scorer("This is a flag") == -1
    assert match_scorer("Incorrect") == -1
