import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


def pytest_addoption(parser) -> None:
    parser.addoption("--tmpdir", type=str, default=None)


@pytest.fixture
def tmpdir(request):
    if request.config.option.tmpdir:
        return Path(request.config.option.tmpdir)
    return TemporaryDirectory()
