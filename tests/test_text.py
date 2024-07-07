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
        ("24ssdf\\pi kld\\rho\\nu jfsf344", ["24", "s", "s", "d", "f", 
                                             "\\pi", "k", "l", "d", "\\rho", "\\nu", 
                                             "j", "f", "s", "f", "3", "4", "4"])
    ]
)
def test_furtherSplitting(text, fullString, expected):
    text.setText(fullString)
    text.furtherSplitting() == expected


@pytest.mark.parametrize(
    "fullString, slice, expected",
    [
        ("24ssdf\\pi kld\\rho\\nu jfsf344", slice(3, 7), Text("24ssdf\\pi"))
    ]
)
def test_subscriptable(text, fullString, slice, expected):
    text.setText(fullString)
    text[slice].text() == expected.text()