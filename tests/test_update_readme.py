import pytest
import shutil
import subprocess
from pathlib import Path


def test_update_readme(tmpdir: Path) -> None:
    readme_path = tmpdir / "README.md"
    shutil.copy("README.md", readme_path)

    # Run the script
    subprocess.run(["python", "update_readme.py", "--path", readme_path])

    # Verify tags are replaced
    with open(readme_path, "r") as file:
        text = file.read()

    # Should be content between start and end markers
    start_marker = "<!-- START_SECTION:films -->"
    end_marker = "<!-- END_SECTION:films -->"
    assert start_marker in text
    assert end_marker in text
    assert text.index(start_marker) < text.index(end_marker)
