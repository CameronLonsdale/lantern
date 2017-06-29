"""Tests for DynamicDict"""

import pytest

from lantern.structures import DynamicDict


def test_dynamicdict():
    """Testing entries are built and returned correctly"""
    container = DynamicDict({'example': lambda: 9})
    assert container.example == 9
   #assert container['example'] == 9


def test_dynamicdict_operations():
    """Testing various operations on the DynamicDict"""
    container = DynamicDict()

    container.invalid = "hello"
    assert container.invalid == "hello"
    #assert container['invalid'] == "hello"

    # container['example'] = "example"
    # assert container.example == "example"
    # assert container['example'] == "example"


def test_dynamicdict_invalid_access():
    """Testing invalid accesses raise exceptions"""
    container = DynamicDict({'example': lambda: 9})

    with pytest.raises(AttributeError):
        container.invalid

    # with pytest.raises(KeyError):
    #     container['invalid']
