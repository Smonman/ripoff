import argparse
import io
import logging
import logging.config
import pathlib
import time
import signal

from PIL import Image
from selenium import webdriver

config_path = pathlib.Path(__file__).parent.resolve().joinpath("logging.conf")
logging.config.fileConfig(config_path)
LOGGER = logging.getLogger()

run = True


def sigterm_handler(signum, frame):
    global run
    run = False


def get_webdriver(url: str, options: dict) -> webdriver.Chrome:
    LOGGER.debug(f"getting webdriver with options {options}")
    return start_webdriver(url, options)


def start_webdriver(url: str, options: dict) -> webdriver.Chrome:
    LOGGER.debug(f"starting new webdriver with options {options}")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={options['width']},{options['height'] + 139}")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--mute-audio")
    driver = webdriver.Chrome(options=chrome_options)
    LOGGER.debug(f"getting page {url}")
    driver.get(url)
    return driver


def stop_webdriver(driver: webdriver.Chrome) -> None:
    if driver:
        LOGGER.debug(f"quitting webdriver")
        driver.quit()


def grab_screenshot(driver: webdriver.Chrome, dest: pathlib.Path) -> None:
    LOGGER.debug(f"grabbing screenshot")
    image_bytes = driver.get_screenshot_as_png()
    save_screenshot(image_bytes, dest)


def save_screenshot(data: bytes, dest: pathlib.Path) -> None:
    try:
        filepath = dest.joinpath("screenshot.bmp").resolve().absolute()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        Image.open(io.BytesIO(data)).save(filepath)
        LOGGER.info(f"saved screenshot under {filepath}")
        print(filepath, end="\n")
    except:
        LOGGER.error("cannot save screenshot")


def wait(seconds: int) -> None:
    LOGGER.debug(f"wait for {seconds} seconds")
    time.sleep(seconds)


def setup_logger(args: dict) -> None:
    if args.verbose:
        LOGGER.setLevel(logging.INFO)
    if args.debug:
        LOGGER.setLevel(logging.DEBUG)


def main(args: dict) -> None:
    LOGGER.debug(args)
    driver = None
    try:
        options = {
            "width": args.size[0],
            "height": args.size[1]
        }
        driver = get_webdriver(args.url, options)
        wait(args.delay)
        while (run):
            LOGGER.info("capture screenshot")
            grab_screenshot(driver, args.output_path)
            wait(args.interval)
    except KeyboardInterrupt:
        LOGGER.info(f"captured keyboard interrupt")
    finally:
        LOGGER.info("stopping webdriver")
        stop_webdriver(driver)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture screenshots of a webpage. Screenshots are taken in regular intervals and saved in the output folder. The resulting file will be named screenshot.bmp.")
    parser.add_argument("url", type=str, nargs="?", default="http://localhost:8080", help="the URL of the webpage")
    parser.add_argument("-o", "--output-path", type=pathlib.Path, default=pathlib.Path("./out"), help="the path where screenshots should be saved to")
    parser.add_argument("-s", "--size", type=int, nargs=2, default=[800, 480], help="the size of the screenshot in pixels; width and height")
    parser.add_argument("-d", "--delay", type=int, default=5, help="delay in seconds between getting the webpage and first taking a screenshot")
    parser.add_argument("-i", "--interval", type=int, default=10, help="interval in seconds between screenshots")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="show more log output")
    parser.add_argument("-e", "--debug", action="store_true", default=False, help="show debug log messages")
    args = parser.parse_args()
    setup_logger(args)
    signal.signal(signal.SIGTERM, sigterm_handler)
    main(args)
