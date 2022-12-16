from __future__ import annotations

import os
import sys
import warnings

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from pelutils import JobDescription, log
from tqdm import tqdm

SRCPATH = sys.argv[0]

TARGET = f"file:///" + os.path.realpath(os.path.join(SRCPATH, "..", "..", "webgl-site", "t4.html"))
DRIVER_PATH = os.path.realpath(os.path.join(SRCPATH, "..", "assets", "geckodriver"))


def _setup_driver(outpath: str) -> WebDriver:
    # Ignore Selenoium deprecation warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", outpath)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "image/octet-stream"
        )
        options = webdriver.FirefoxOptions()
        options.headless = True
        return webdriver.Firefox(
            options=options, executable_path=DRIVER_PATH, firefox_profile=profile
        )


def extract_image(driver: WebDriver, use_sc: bool):
    driver.get(TARGET)
    driver.find_element(value="recomputeButton").click()
    if use_sc:
        driver.find_element(value="scButton").click()
    driver.find_element(value="saveButton").click()
    driver.find_element(value="labelMapButton").click()
    driver.find_element(value="saveButton").click()


def run(args: JobDescription):
    driver = _setup_driver(os.path.realpath(args.location))
    for _ in tqdm(range(args.N)):
        extract_image(driver, args.use_sc)


if __name__ == "__main__":
    from pelutils import Parser, Argument, Flag

    parser = Parser(
        Argument("N", type=int, help="Number of images to generate"),
        Flag("use-sc"),
        multiple_jobs=True,
    )
    jobs = parser.parse_args()
    parser.document()
    for job in jobs:
        log.configure(os.path.join(job.location, f"dataset.log"))
        log.log_repo()
        log(f"Starting {job.name}")
        with log.log_errors:
            run(job)
