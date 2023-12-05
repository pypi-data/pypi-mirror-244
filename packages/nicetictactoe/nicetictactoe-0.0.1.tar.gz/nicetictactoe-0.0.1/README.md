

Tic Tac Toe
===============
This is simple nice game which you can choose on your preferences to play in various dimensions with your friends both in console for code lovers and visually displayed. Enjoy! 

<p align="center">
  <img src="/nicetictactoe.png">
</p>

Getting Started
====
Install the package using pip:
```bash
pip install nicetictactoe
```
Or download the source code using this command:

    git clone https://github.com/iamkhosrojerdi/nicetictactoe.git

Usage
====
### GUI:

```python
from nicetictactoe.src.gui import Game
from nicetictactoe.src.logic import Grid

grid = Grid()
game = Game(grid)

with game:
    game.run()
```

### Console:
```python
from nicetictactoe.src.logic import Grid

while not grid.winner:
    pos = input()
    x, y = int(pos[0]), int(pos[1])
    grid.insert((x, y))

    for row in grid.tiles:
        print(row)

print(grid.winner)
```