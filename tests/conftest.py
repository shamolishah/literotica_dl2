import pytest

from literotica_dl2.story import Story


@pytest.fixture
def story():
    return Story("e-beth-ch-01")
