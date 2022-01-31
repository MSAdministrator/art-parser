import pytest


@pytest.fixture
def default_art_parser_fixture():
    from art_parser import ARTParser
    return ARTParser()
