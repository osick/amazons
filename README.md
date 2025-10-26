# The Game of Amazons

A Python implementation of the Amazons board game - a chess-like strategy game where players move amazons and shoot arrows to block their opponent.

For more about the game rules, see: https://www.youtube.com/watch?v=kjSOSeRZVNg

## Features

### Interactive TUI (Text User Interface)
- Beautiful colored interface with rich graphics
- Player vs Player mode with keyboard controls
- Visual highlighting of valid moves
- Multiple game modes (standard 10x10, quick 6x6)
- Watch AI vs AI matches

### Classic Mode
- Automated game simulation
- Win rate analysis across different board sizes
- Random move generation for testing

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Play the Interactive TUI Version (Recommended)

```bash
python amazons_tui.py
```

**Controls:**
- Arrow Keys: Move cursor
- Space/Enter: Select piece or confirm move
- Esc: Cancel current selection
- R: Restart game
- Q: Quit

**How to play:**
1. Select one of your amazons (White ♛ or Black ♛)
2. Choose where to move it (highlighted squares show valid moves)
3. Choose where to shoot an arrow (creates a permanent block 🔥)
4. The game ends when a player has no valid moves left

### Run Classic Tests

```bash
python amazons.py
```

This runs automated tests and win-rate analysis.

## Game Rules

- Two players: White and Black, each controls 4 (or 2) amazons
- On each turn:
  1. Move one of your amazons (like a chess queen - any direction, any distance)
  2. Shoot an arrow from the new position (also moves like a queen)
  3. The arrow creates a permanent block on the board
- Amazons and arrows cannot jump over blocks or other amazons
- First player with no valid moves loses

## File Structure

- `amazons.py` - Core game logic and automated testing
- `amazons_tui.py` - Interactive TUI version with colors and keyboard controls
- `requirements.txt` - Python dependencies
