import argparse
import logging
import logging.config

logging.config.fileConfig("src/logging.conf")
LOGGER = logging.getLogger()


def main(args: dict) -> None:
    LOGGER.debug(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture screenshots of an angular application.")
    parser.add_argument("-a", "--angular-project-path", nargs=1, default=".")
    parser.add_argument("-p", "--port", nargs=1)
    parser.add_argument("-o", "--output-path", nargs=1)
    parser.add_argument("-s", "--size", nargs=2)
    parser.add_argument("-t", "--timeout", nargs="?", default=0)
    parser.add_argument("-i", "--interval", nargs=1, default=10)
    main(parser.parse_args())
