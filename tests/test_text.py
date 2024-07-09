import pytest
from vimath.text import Text


@pytest.fixture
def text():
    text_instance = Text()
    yield text_instance

    
@pytest.mark.parametrize(
    "fullString, expected",
    [
        ("24ssdf\\pi kld\\rho\\nu jfsf344", ["24", "ssdf", "\\pi", "kld", "\\rho", "\\nu", "jfsf", "344"])
    ]
)
def test_splitText(text, fullString, expected):
    text.setText(fullString)
    assert  text.splitText() == expected

        
@pytest.mark.parametrize(
    "fullString, expected",
    [
        ("24ssdf\\pi kld\\rho\\nu jfsf344", 19)
    ]
)
def test_length(text, fullString, expected):
    text.setText(fullString)
    assert  len(text) == expected
        

@pytest.mark.parametrize(
    "fullString, expected",
    [
        ("24ssdf\\pi kld\\rho\\nu jfsf344", ["2", "4", "s", "s", "d", "f", 
                                             "\\pi", "k", "l", "d", "\\rho", "\\nu", 
                                             "j", "f", "s", "f", "3", "4", "4"])
    ]
)
def test_furtherSplitting(text, fullString, expected):
    text.setText(fullString)
    assert text.furtherSplitting() == expected


@pytest.mark.parametrize(
    "fullString, slice, expected",
    [
        ("24ssdf\\pi kld\\rho\\nu jfsf344", slice(3, 7), Text("sdf\\pi")),
        ("24ssdf\\pi kld\\rho\\nu jfsf344", slice(3, 8), Text("sdf\\pi k")),
    ]
)
def test_subscriptable(text, fullString, slice, expected):
    text.setText(fullString)
    assert text[slice].text() == expected.text()

    
@pytest.mark.parametrize(
    "initialPlainText, eventText, cursorPosition, expected",
    [
        ("", "qwerty", 0, "qwerty"),
        ("qwerty", "1234", 1, "q1234werty"),
        ("qwerty", "\\pi", 1, "q\\pi werty"),
        ("qwerty", "\\pi", 6, "qwerty\\pi"),
        ("qwerty\\pi", "\\pi", 7, "qwerty\\pi\\pi"),
        ("qwer\\pi ty", "\\pi", 5, "qwer\\pi\\pi ty"),
    ]
)
def test_insertTextOnCursorPosition(text, initialPlainText, eventText, cursorPosition, expected):
    text.plain_text = initialPlainText
    text._cursorPosition = cursorPosition
    text.insertTextOnCursorPosition(eventText)
    assert text.plain_text == expected
