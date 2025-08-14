import argparse
import logging
import logging.config
import pathlib
import signal
import subprocess
import time

logging.config.fileConfig("src/logging.conf")
LOGGER = logging.getLogger()


def run_angular_project(path: pathlib.Path, port: int) -> subprocess.Popen:
    LOGGER.debug(f"starting angular project at {path.absolute()} at port {port}")
    return subprocess.Popen(["ng", "serve", "--port", str(port)], shell=True, cwd=path.absolute())


def stop_angular_project(p: subprocess.Popen) -> None:
    if p is not None:
        LOGGER.debug(f"terminating angular project")
        p.terminate()


def wait(seconds: int) -> None:
    time.sleep(seconds)


def main(args: dict) -> None:
    LOGGER.debug(args)
    try:
        ng = run_angular_project(pathlib.Path(args.angular_project_path), int(args.port))
        wait(args.delay)
        while (True):
            LOGGER.info("capture screenshot")
            wait(args.interval)
    except KeyboardInterrupt:
        LOGGER.debug(f"captured keyboard interrupt")
        stop_angular_project(ng)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture screenshots of an angular application.")
    parser.add_argument("-a", "--angular-project-path", required=True)
    parser.add_argument("-p", "--port", type=int, default=4200)
    parser.add_argument("-o", "--output-path", default="./out")
    parser.add_argument("-s", "--size", type=int, nargs=2)
    parser.add_argument("-d", "--delay", type=int, default=0)
    parser.add_argument("-i", "--interval", type=int, default=10)
    main(parser.parse_args())
