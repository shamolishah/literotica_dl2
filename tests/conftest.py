import pytest

from literotica_dl2.author import Author
from literotica_dl2.story import Story


@pytest.fixture
def story():
    return Story("e-beth-ch-01")


@pytest.fixture
def author():
    # return Author("silkstockingslover")
    return Author("aurelius1982")
