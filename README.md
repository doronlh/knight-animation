# Knight Animation

A library for animating the movement of a knight on a chessboard. Outputs a GIF animation of the knight's movement and
presents it in a browser.

## Installation

```shell script
$ pip install git+ssh://git@github.com/doronlh/knight-animation@v0.1
```

## Usage

The `animate_knight()` function takes a sequence of (x, y) coordinates of the chessboard, where top-left is (0, 0)

```python
from knight_animation import animate_knight
moves = [(0,1), (1,3), (3, 4), (5, 3), (4, 1)]
animate_knight(moves)
```

will result in the following animated GIF being opened in a browser

![animated knight](resources/example.gif?raw=true "animated knight")
