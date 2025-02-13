import datetime
import pathlib
import allure
import pytest
from allure_commons.types import AttachmentType


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_teardown(item, nextitem):
#     yield
    
#     try:
#         browser = item.funcargs.get("browser")
#         for ctx in browser.contexts:
#             for page in ctx.pages:
#                 if page.video:
#                     video_path = page.video.path()
#                     if video_path:
#                         print(f"Attaching video: {video_path}")
#                         timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                         allure.attach(
#                             file_source=video_path,
#                             name=f"failed-{timestamp}.webm",
#                             attachment_type=AttachmentType.WEBM
#                         )

#     except Exception as e:
#         print(f"Error attaching video: {e}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    try:
        artifacts_dir = item.funcargs.get("output_path")
        if artifacts_dir:
            artifacts_dir_path = pathlib.Path(artifacts_dir)
        
        if artifacts_dir_path.is_dir():            
            for file in artifacts_dir_path.iterdir():
                if file.is_file() and file.suffix == ".webm":
                    allure.attach.file(
                        file,
                        name=file.name,
                        attachment_type=allure.attachment_type.WEBM,
                    )

    except Exception as e:
        print(f"Error attaching video: {e}")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     if rep.when == "call" and rep.failed: # the text failed
#         if "context" in item.funcargs:
#             context = item.funcargs["context"]
#             page = context.pages[0] # assuming the first page is the one we want. Why?
#             attach_video(page)

# def attach_video(page):
#     video = page.video.path()
#     allure.attach(video, "video", AttachmentType.WEBM)