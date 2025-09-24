# ripoff

This project is used to capture screenshots of a website in periodic intervals.

## Usage

```bash
python ripoff.py [-h] [-o OUTPUT_PATH] [-s SIZE SIZE] [-d DELAY] [-i INTERVAL] [-v] [-e] [url]
```

### Arguments

- `url` positional argument: the URL of the webpage
- `-h`, `--help`: show this help message and exit
- `-o`, `--output-path OUTPUT_PATH`: the path where screenshots should be saved to
- `-s`, `--size SIZE SIZE`: the size of the screenshot in pixels; width and height
- `-d`, `--delay DELAY`: delay in seconds between getting the webpage and first taking a screenshot
- `-i`, `--interval INTERVAL`: interval in seconds between screenshots
- `-v`, `--verbose`: show more log output
- `-e`, `--debug`: show debug log messages

The screenshots are saved to the output directory with the filename: `screenshot.bmp`.

## Requirements

This relies on [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) being installed at the default location.

## Raspberry Pi

[Here](https://gist.github.com/Smonman/06d7121be082fc81029bc56003b665a4) is an example of how this can be used with a Raspberry Pi and a Waveshare eInk display:
