# Tsuro (Python/Arcade)

An interactive adaptation of the board game Tsuro (original design by Tom McMurchie). Place tiles to extend your path and keep your marker on the board—while nudging others off the edge.

This project uses Python with a lightweight graphics shim over Arcade for a CS110-style API. It supports 2–8 players on a single computer.

## Table of Contents

- Overview
- How to Play (Rules)
- Controls (This Implementation)
- Run Locally
- Configuration
- Project Structure
- Credits

## Overview

In Tsuro, each player has a marker on the board’s edge. On your turn, you place one tile adjacent to your own marker. The tile’s paths connect and extend your marker’s route; your marker (and possibly others) then travels along the connected path until it cannot move further. If a marker exits the board’s boundary, that player is eliminated. The last player remaining wins (or the game may end in a tie).

## How to Play (Rules)

1) Setup
- Choose number of players (2–8).
- Each player sets a starting position by moving clockwise around the border and right-clicking to confirm.
- Each player draws a hand of three tiles.

2) Your Turn
- Select a tile from your hand (left-click to toggle selection; a light-blue border #90D5FF indicates selection).
- Right-click the selected tile to rotate it 90° (repeat as needed).
- Left-click a board cell adjacent to your marker to place the tile.

3) Movement
- After a tile is placed, all markers that can move follow the connected path automatically until no further movement is possible.
- If a marker’s path leaves the board, that player is eliminated.

4) Drawing Tiles and the Dragon Tile
- Players draw back up to three tiles if possible. When the tile pile is empty, the dragon tile indicates who will draw next as tiles become available again.

5) End of Game
- The last remaining player wins.
- If all remaining players exit the board simultaneously, the game ends in a tie.

## Controls (This Implementation)

- Mouse left-click on your hand tile: select/unselect the tile (border turns light blue #90D5FF).
- Mouse right-click on your hand tile: rotate it 90° clockwise.
- Mouse left-click on a board cell next to your marker: place the selected tile there (if the placement is legal); otherwise, a warning will appear.
- During setup (before the first round):
	- Left-click the colored banner near the top to cycle your marker clockwise along border positions.
	- Right-click the same banner to confirm your starting position.

Notes
- On some trackpads, you may need to enable “secondary click” (two-finger tap or bottom-right click) to send a right-click.

## Run Locally

This repository does not include a virtual environment. Create one and install dependencies with the provided requirements file:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Then launch the game:

```bash
python game.py
```

If the window size or assets don’t look right, see Configuration below.

## Configuration

Edit `constants.py` to tweak:
- `WIN_WIDTH`, `WIN_HEIGHT` — window size
- `BOARD_LEN` — board graphic size
- `IMG_DIR` — images folder

Visual & UI notes:
- Selected tile border color is light blue `#90D5FF`.
- If you prefer a different selection color or border thickness, change it in `classes.py` (`Tile.handle_mouse_press`).

## Project Structure

- `game.py` — entry point
- `game_core.py` — wire-up to `Game` and window creation
- `classes.py` — main game logic (Game, Player, Tile, Cell, Dragon, Popup)
- `arcadegraphics.py` — shim providing a cs110graphics-like API on top of Arcade
- `constants.py` — sizes and assets
- `images/` — sprites and textures
- `matches.txt` — tile connection logic
- `requirements.txt` — Python dependencies

## Credits

- Board game Tsuro designed by Tom McMurchie.
- This software is for educational/demonstration purposes and is not an official product of the Tsuro IP holders.

## Team
- Thirumurugan RA - 3122235001149
- Vishal Muralidharan - 3122235001162