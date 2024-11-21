import pytest
from unittest.mock import MagicMock, Mock
from solutions.task2.solution import WikiParser


@pytest.fixture
def wiki_parser():
    return WikiParser()


@pytest.mark.parametrize("names, result_dict, _return", [
    (["Аист", "Бобер", "Волк", "А", "KIBI"], {"А": 1, "Б": 1, "В": 1}, True),
    (["заяц", "яСтреб", "сТЕРВЯТНИК"], {"З": 1, "Я": 1, "С": 1}, None),
])
def test_manager(wiki_parser, names, result_dict, _return):
    parser = wiki_parser
    result = parser.manager(names)
    for key, value in result_dict.items():
        assert value == parser.counter_cyrillic[key]
    assert result == _return


class Table:
    def __init__(self, rows: list):
        self.text = rows


@pytest.mark.parametrize("names, call_count", [
    (["Аист", "Бобер", "Волк", "А", "KIBI"], 3),
])
def test_parse(wiki_parser, names, call_count):
    wiki_parser.manager = MagicMock(side_effect=(None, None, True))
    wiki_parser.brawser.find_element = MagicMock()
    WebDriverWait = MagicMock()
    WebDriverWait.utils = MagicMock(return_value=Table(names))
    wiki_parser.parse()
    assert wiki_parser.manager.call_count == call_count
