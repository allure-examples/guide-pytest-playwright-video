import pathlib
import allure
import pytest

PLAYWRIGHT_VIDEO_EXTENSION = ".webm"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    try:
        artifacts_dir = item.funcargs.get("output_path")
        if artifacts_dir:
            artifacts_dir_path = pathlib.Path(artifacts_dir)
        
        if artifacts_dir_path.is_dir():            
            for file in artifacts_dir_path.iterdir():
                if file.is_file() and file.suffix == PLAYWRIGHT_VIDEO_EXTENSION:
                    allure.attach.file(
                        file,
                        name=file.name,
                        attachment_type=allure.attachment_type.WEBM,
                    )

    except Exception as e:
        print(f"Error attaching video: {e}")
