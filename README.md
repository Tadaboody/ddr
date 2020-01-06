# Camera Dance Mat
Desperately want to play Dance Dance Revolution (DDR) But don't have a mat?

This project attempts to use a camera to detect your movments and translate it to the arrow keys, creating an **invisible dance mat**

## Outline
The camera will be mounted directly above the player.
1. Detect a quadrilateral object on the floor (like an A4 page), this will be the up arrow.
1. Duplicate the square to all directions to create the invisible mat.
1. Start rolling, detect any movment.
1. If the movement is colliding with a square, register a tap and press the matching direction in the arrow keys.
## Running

This project uses [poetry](https://python-poetry.org/) for packaging.
Run
```py
pip install poetry
poetry install
poetry run python src/ddr.py
```