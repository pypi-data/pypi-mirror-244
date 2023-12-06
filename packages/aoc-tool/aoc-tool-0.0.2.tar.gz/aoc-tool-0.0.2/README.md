# 🎄aoc-tool 🎁

Python functions to automate getting inputs and submitting results to Advent of Code. 

Inputs are cached locally in `$HOME/.cache/aoc`. 

Please throttle your submissions to Advent of Code's servers.

## Dependencies

None.

## Installation

```bash
python3 -m pip install git+https://github.com/wesbarnett/aoc-tool
```

## Usage

Log in to [Advent of Code](https://adventofcode.com). Get your session cookie from the browser and save it to an environment variable named `AOC_COOKIE`.

```python
from aoc import get_input, submit

if __name__ == "__main__":
    year, day, level = 2022, 10, 1
    aoc_input = get_input(year, day)

    # Do some calculations
    # ans = <calculations>

    submit(ans, year, day, level)
```
