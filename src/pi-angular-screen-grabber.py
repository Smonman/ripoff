import argparse
import logging
import logging.config
import pathlib
import signal
import subprocess
import time

from selenium import webdriver

logging.config.fileConfig("src/logging.conf")
LOGGER = logging.getLogger()


def run_angular_project(path: pathlib.Path, port: int) -> subprocess.Popen:
    LOGGER.debug(f"starting angular project at {path.absolute()} at port {port}")
    return subprocess.Popen(["ng", "serve", "--port", str(port)], shell=True, cwd=path.absolute())


def stop_angular_project(p: subprocess.Popen) -> None:
    if p is not None:
        LOGGER.debug(f"terminating angular project")
        p.terminate()


def get_webdriver(width: int, height: int, port: int) -> webdriver.Chrome:
    LOGGER.debug(f"getting webdriver with window size {width} {height}")
    return start_webdriver(f"http://localhost:{port}", width, height)


def start_webdriver(url: str, width: int = 800, height: int = 460) -> webdriver.Chrome:
    # TODO: window size does not work
    LOGGER.debug(f"starting new webdriver with window size {width} {height}")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument(f"--size={width},{height}")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome(options=options)
    LOGGER.debug(f"getting page {url}")
    driver.get(url)
    return driver


def stop_webdriver(driver: webdriver.Chrome) -> None:
    if driver:
        LOGGER.debug(f"quitting webdriver")
        driver.quit()


def grab_screenshot(driver: webdriver.Chrome) -> None:
    # TODO: specify output path
    driver.get_screenshot_as_file("screenshot.png")


def wait(seconds: int) -> None:
    time.sleep(seconds)


def main(args: dict) -> None:
    LOGGER.debug(args)
    driver = None
    try:
        ng = run_angular_project(pathlib.Path(args.angular_project_path), int(args.port))
        wait(args.delay)
        driver = get_webdriver(args.size[0], args.size[1], args.port)
        wait(args.delay)
        while (True):
            LOGGER.info("capture screenshot")
            grab_screenshot(driver)
            wait(args.interval)
    except KeyboardInterrupt:
        LOGGER.debug(f"captured keyboard interrupt")
    finally:
        stop_angular_project(ng)
        stop_webdriver(driver)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture screenshots of an angular application.")
    parser.add_argument("-a", "--angular-project-path", required=True)
    parser.add_argument("-p", "--port", type=int, default=4200)
    parser.add_argument("-o", "--output-path", default="./out")
    parser.add_argument("-s", "--size", type=int, nargs=2)
    parser.add_argument("-d", "--delay", type=int, default=5)
    parser.add_argument("-i", "--interval", type=int, default=10)
    main(parser.parse_args())
