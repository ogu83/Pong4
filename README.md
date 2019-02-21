# Pong4

## Description
This is 4 Player Pong Game

## Installation

Python 3.6 Required
```python
pip install pygame
```
## Pong4.py
This is 2 or 4 player Pong game with single local computer and keyboard

* if `FourPlayers = True` is set game will initiate four player game play 
* if `FourPlayers = False` is set game will initiate two player game play 

### 2 Player Game
A **RED** and a **GREEN** player will initiated across the screen. 

* **RED** player will be on the **LEFT**
* **GREEN** player will stand on the **RIGHT**

Ball will be thrown to the RED player first, if reflected by **RED** player the game will start, if not ball will be thrown to **GREEN** player.
To start scoring at least one player should reflect first to be fair in 2 Player and also in 4 Player game.

![2 Player Pong Local](https://github.com/ogu83/Pong4/blob/master/Images/2PlayerPongLocal.jpg)

### 4 Player Game
A **RED**, **GREEN**, **BLUE** and **YELLOW** player will initiated across the screen. 

* **RED** player will be on the **LEFT** and playes with **W** and **S** keys
* **GREEN** player will stand on the **RIGHT** and playes with **UP** and **DOWN** keys
* **BLUE** player will stand on the **TOP** and playes with **A** and **D** keys
* **YELLOW** player will stand on the **BOTTOM** and playes with **LEFT** and **RIGHT** keys

Ball will be thrown to the RED player first, if reflected by **RED** player the game will start, if not ball will be thrown to **GREEN** player.
To start scoring at least one player should reflect first to be fair.
The last ball thrower gets the score, whereever side of the screen the ball fall of, and has the right to first throw the ball in the next cycle.

![4 Player Pong Local](https://github.com/ogu83/Pong4/blob/master/Images/4PlayerPongLocal.jpg)

Scoring is on the top of the screen. All scores is in the color of the player.

## Pong4Server.py
Multiplayer Pong4 on Network

First Start The Pong4 Server
```python
python Pong4Server.py
```

* if `FourPlayers = True` is set game will initiate four player game play 
* if `FourPlayers = False` is set game will initiate two player game play 

Default Host and Port are localhost and 9009, to customize set the values **HOST** and **PORT**

Then Start the clients via command
1. Player1 `python Pong4Client.py 1`
1. Player2 `python Pong4Client.py 2`
1. Player3 `python Pong4Client.py 3`
1. Player4 `python Pong4Client.py 4`

All Players playes with **LEFT** and **RIGHT** keys and server will move their paddle accordingly.

Also in the clients **ip** and **port** values should be set if the server is customized.

The defaults are
```python
ip, port = socket.gethostname(), 9009
```

### ENJOY THE GAME.
