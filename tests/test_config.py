from src.doc2markdown.config import (
    PROJECT_ROOT,
    INPUT_DIR,
    OUTPUT_DIR,
    LOG_DIR,
)


def test_project_root_exists():
    assert PROJECT_ROOT.exists()


def test_input_directory():
    assert INPUT_DIR.name == "input"


def test_output_directory():
    assert OUTPUT_DIR.name == "output"


def test_log_directory():
    assert LOG_DIR.name == "logs"