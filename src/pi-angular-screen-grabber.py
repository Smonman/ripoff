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


def run_angular(path: pathlib.Path, port: int) -> subprocess.Popen:
    LOGGER.debug(f"starting angular at {path.absolute()} at port {port}")
    return subprocess.Popen(["ng", "serve", "--port", str(port)], shell=True, cwd=path.absolute())


def stop_angular(p: subprocess.Popen) -> None:
    if p is not None:
        LOGGER.debug(f"terminating angular")
        p.terminate()


def get_webdriver(width: int, height: int, port: int) -> webdriver.Chrome:
    LOGGER.debug(f"getting webdriver with window size {width}x{height}")
    return start_webdriver(f"http://localhost:{port}", width, height)


def start_webdriver(url: str, width: int = 256, height: int = 256) -> webdriver.Chrome:
    # TODO: window size does not work
    LOGGER.debug(f"starting new webdriver with window size {width}x{height}")
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


def grab_screenshot(driver: webdriver.Chrome, dest: pathlib.Path) -> None:
    LOGGER.debug(f"grabbing screenshot")
    filepath = dest.joinpath("screenshot.png").resolve().absolute()
    filepath.parent.mkdir(parents=True, exist_ok=True)
    driver.get_screenshot_as_file(filepath)
    LOGGER.info(f"saved screenshot under {filepath}")


def wait(seconds: int) -> None:
    LOGGER.debug(f"wait for {seconds} seconds")
    time.sleep(seconds)


def main(args: dict) -> None:
    LOGGER.debug(args)
    driver = None
    try:
        ng = run_angular(pathlib.Path(args.angular_project_path), int(args.port))
        wait(args.delay)
        driver = get_webdriver(args.size[0], args.size[1], args.port)
        wait(args.delay)
        while (True):
            LOGGER.info("capture screenshot")
            grab_screenshot(driver, args.output_path)
            wait(args.interval)
    except KeyboardInterrupt:
        LOGGER.info(f"captured keyboard interrupt")
    finally:
        LOGGER.info("stopping angular client and webdriver")
        stop_angular(ng)
        stop_webdriver(driver)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture screenshots of an angular application.")
    parser.add_argument("-a", "--angular-project-path", type=pathlib.Path, required=True)
    parser.add_argument("-p", "--port", type=int, default=4200)
    parser.add_argument("-o", "--output-path", type=pathlib.Path, default=pathlib.Path("./out"))
    parser.add_argument("-s", "--size", type=int, nargs=2, default=[800, 480])
    parser.add_argument("-d", "--delay", type=int, default=5)
    parser.add_argument("-i", "--interval", type=int, default=10)
    main(parser.parse_args())
