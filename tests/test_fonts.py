import pytest
from vimath.lineedit import MyLineEdit
from PySide6.QtWidgets import QWidget
from unittest.mock import Mock
from vimath.utils import translateUnicode, symbols


@pytest.fixture
def mock_scene():
    # Mock the scene and its nested dependencies
    mock_graphic_cursor = Mock()
    mock_window = Mock(graphicCursor=mock_graphic_cursor)
    mock_scene = Mock(window=mock_window, updateFrames=Mock())
    yield mock_scene


@pytest.fixture()
def mock_parent(qtbot, mock_scene):
    obj = QWidget()
    qtbot.add_widget(obj)
    obj.fontSize = 15
    obj.scene = mock_scene
    yield obj


@pytest.fixture()
def lineEdit(mock_parent):
    yield MyLineEdit(mock_parent)


def test_groupCharacters(lineEdit):
    lineEdit.setText("q23werty")
    expected_result = [("cmmi10", "q"), ("cmr10", "23"), ("cmmi10", "we")]
    assert lineEdit.groupCharacters(5) == expected_result
    expected_result = [("cmmi10", "q"), ("cmr10", "23"), ("cmmi10", "werty")]
    assert lineEdit.groupCharacters(None) == expected_result
    lineEdit.setText("qwert\\pi qwert")
    expected_result = [("cmmi10", "qwert"), ("cmmi10", chr(188)), ("cmmi10", "qwert")]
    assert lineEdit.groupCharacters(None) == expected_result

    