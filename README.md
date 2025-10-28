# 🐉 Tsuro - The Game of the Path

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Arcade](https://img.shields.io/badge/arcade-2.6.17-orange)
![License](https://img.shields.io/badge/license-Educational-green)

*An elegant digital adaptation of the classic board game Tsuro*

**Place tiles. Extend paths. Stay on the board. Be the last one standing.**

[Overview](#-overview) • [How to Play](#-how-to-play) • [Installation](#-installation) • [Controls](#-controls) • [Project Structure](#-project-structure)

</div>

---

## 📖 Overview

Tsuro (original design by Tom McMurchie) is a beautifully strategic tile-laying game where players guide their markers along an ever-changing path. This Python implementation brings the game to life with:

- 🎨 **Ancient scroll theme** with parchment panels and ink-style borders
- 👥 **2-8 player support** on a single computer
- 🎯 **Simple, intuitive controls** with mouse-based interaction
- 🏗️ **Modular architecture** for easy maintenance and extension
- 🎮 **Lightweight graphics** built on Python Arcade

## 🎮 How to Play

### 🎯 Game Rules

#### 1️⃣ Setup Phase
- **Choose players**: Select 2-8 players from the welcome screen
- **Position markers**: Each player cycles through border positions (left-click to move clockwise)
- **Confirm position**: Right-click to lock in your starting location
- **Initial hand**: Each player receives 3 tiles to begin

#### 2️⃣ Playing Your Turn
1. **Select a tile**: Left-click a tile in your hand (mint-green border `#9bc3ab` appears)
2. **Rotate (optional)**: Right-click the selected tile to rotate 90° clockwise
3. **Place the tile**: Left-click an empty board cell adjacent to your marker

#### 3️⃣ Automatic Movement
- All markers follow their connected paths automatically
- Movement continues until the path ends or leaves the board
- Markers that exit the board eliminate that player

#### 4️⃣ Tile Management
- Players automatically draw back up to 3 tiles each turn
- When the pile is empty, the **Dragon Tile** appears
- The dragon tile indicates who will receive the next available tile

#### 5️⃣ Victory Conditions
- ✨ **Win**: Be the last player remaining on the board
- 🤝 **Tie**: If all remaining players exit simultaneously

## 🎮 Controls

### Mouse Actions

| Action | Control | Description |
|--------|---------|-------------|
| **Select Tile** | Left-click on hand tile | Toggle selection (mint-green border appears) |
| **Rotate Tile** | Right-click on hand tile | Rotate 90° clockwise |
| **Place Tile** | Left-click on board cell | Place selected tile adjacent to your marker |

### Setup Phase Controls

| Action | Control | Description |
|--------|---------|-------------|
| **Move Marker** | Left-click on prompt banner | Cycle your marker clockwise around the border |
| **Confirm Position** | Right-click on prompt banner | Lock in your starting position |

> **💡 Trackpad Users**: Enable "secondary click" (two-finger tap or bottom-right click) for right-click functionality.

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Steps

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd tsuro-master
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv myenv
   ```

3. **Activate the virtual environment**:
   ```bash
   # Linux/macOS
   source myenv/bin/activate
   
   # Windows
   myenv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Launch the game**:
   ```bash
   python game.py
   ```

### Troubleshooting
- If the window size seems incorrect, adjust values in `constants.py`
- Ensure all images are present in the `images/` directory
- Use Python 3.11+ for best compatibility

---

## ⚙️ Configuration

Customize the game by editing `constants.py`:

```python
WIN_WIDTH = 1500      # Window width in pixels
WIN_HEIGHT = 800      # Window height in pixels
BOARD_LEN = 600       # Board size in pixels
IMG_DIR = 'images'    # Image assets directory
```

### Theme Colors
The ancient scroll theme uses:
- **Parchment panels**: `#efe2c2`
- **Ink borders**: `#5a4a3b`
- **Player markers**: `#9bc3ab`
- **Selection highlight**: `#9bc3ab`

To customize colors, edit the theme colors in `game_logic.py` (`Game.__init__`) or tile selection colors in `tiles.py` (`Tile.handle_mouse_press`).

---

## 📂 Project Structure

```
tsuro-master/
├── game.py              # Entry point - launches the game
├── game_logic.py        # Core game logic (Game class)
├── tiles.py             # Tile and Dragon classes
├── cells.py             # Board cell logic
├── players.py           # Player marker management
├── ui_components.py     # Popup dialogs and end-game messages
├── arcadegraphics.py    # Graphics helper functions using Arcade
├── constants.py         # Configuration constants
├── helpers.py           # Utility functions (tile path logic)
├── matches.txt          # Tile connection coordinate data
├── requirements.txt     # Python dependencies
└── images/              # Game assets (tiles, board, background)
    ├── 0.jpg ... 34.jpg # 35 unique tile images
    ├── dragon.jpg       # Dragon tile
    ├── board.jpg        # Game board
    └── bkg2.png         # Background image
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `game_logic.py` | Game state, turn management, player/tile coordination |
| `tiles.py` | Tile rendering, rotation, selection, path logic |
| `cells.py` | Board cell click handling and tile placement |
| `players.py` | Player markers, movement, elimination, prompts |
| `ui_components.py` | Popup dialogs, winner/tie announcements |
| `arcadegraphics.py` | Graphics API compatibility layer |

---

## 🎓 Technical Details

### Architecture Highlights
- **Event-driven design**: Mouse events dispatch to top-most clickable shapes
- **Depth-based z-ordering**: Lower depth values render on top
- **Dictionary-based pathfinding**: Efficient marker movement using coordinate lookups
- **Modular class structure**: Each component has a single, clear responsibility

### Path Algorithm
The game uses a dictionary-based path-following algorithm:
- Each board position can connect to up to 2 other positions
- Two dictionaries (`_loc_dict1`, `_loc_dict2`) store all possible connections
- Markers follow paths until reaching a dead end or board edge
- Movement is deterministic and visually smooth

---

## 🏆 Credits

- **Original Game Design**: Tom McMurchie
- **Implementation**: Educational project showcasing Python game development
- **Graphics Library**: [Python Arcade](https://api.arcade.academy/) 2.6.17

> ⚠️ **Disclaimer**: This software is for educational and demonstration purposes only and is not affiliated with or endorsed by the creators of Tsuro or its publishers.

---

## 👥 Development Team

<table>
  <tr>
    <td align="center">
      <strong>Thirumurugan RA</strong><br>
      <sub>Reg No: 3122235001149</sub>
    </td>
    <td align="center">
      <strong>Vishal Muralidharan</strong><br>
      <sub>Reg No: 3122235001162</sub>
    </td>
  </tr>
</table>

---

<div align="center">

**Enjoy the game! 🐉**

*May your path be long and your opponents' paths be short.*

</div>
