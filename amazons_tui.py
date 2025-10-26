#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fancy TUI version of Amazons game with colors and interactive gameplay
"""

import sys
import os
from typing import Optional, Tuple, List
from amazons import Amazons

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.text import Text
    from rich.live import Live
    from rich.align import Align
    from rich import box
    import readchar
except ImportError:
    print("Please install required dependencies:")
    print("pip install rich readchar")
    sys.exit(1)


class AmazonsTUI:
    """Interactive TUI for Amazons game"""

    # Color schemes
    COLORS = {
        'white_amazon': 'bold bright_white on blue',
        'black_amazon': 'bold black on red',
        'block': 'white on bright_black',
        'empty': 'dim white',
        'cursor': 'bold yellow on green',
        'selected': 'bold yellow on magenta',
        'possible_move': 'bold green on bright_black',
        'board_border': 'bright_cyan',
    }

    def __init__(self, boardsize: int = 10):
        self.game = Amazons(boardsize)
        self.console = Console()
        self.cursor_x = 1
        self.cursor_y = 1
        self.selected_piece: Optional[Tuple[int, int]] = None
        self.move_to: Optional[Tuple[int, int]] = None
        self.possible_moves: List[str] = []
        self.status_message = "White's turn - Select an amazon to move"
        self.game_over = False
        self.winner = None
        self.move_count = 0

    def setup_standard_game(self):
        """Setup standard 10x10 game with 4 amazons each"""
        self.game.set_amazon(1, 4, "b")
        self.game.set_amazon(1, 7, "b")
        self.game.set_amazon(4, 1, "b")
        self.game.set_amazon(4, 10, "b")
        self.game.set_amazon(10, 4, "w")
        self.game.set_amazon(10, 7, "w")
        self.game.set_amazon(7, 1, "w")
        self.game.set_amazon(7, 10, "w")

    def setup_small_game(self):
        """Setup small 6x6 game for quick play"""
        self.game = Amazons(6)
        self.game.set_amazon(1, 1, "b")
        self.game.set_amazon(1, 6, "b")
        self.game.set_amazon(6, 6, "w")
        self.game.set_amazon(6, 1, "w")

    def get_cell_display(self, x: int, y: int, cell: str) -> Text:
        """Get formatted display for a cell with colors"""
        is_cursor = (x == self.cursor_x and y == self.cursor_y)
        is_selected = (self.selected_piece and
                      x == self.selected_piece[0] and
                      y == self.selected_piece[1])
        is_move_target = (self.move_to and
                         x == self.move_to[0] and
                         y == self.move_to[1])

        # Check if this is a possible move location
        is_possible = False
        if self.selected_piece and not self.move_to:
            # First phase: showing where amazon can move
            for move in self.possible_moves:
                coords = move.split(',')
                if len(coords) >= 4 and int(coords[2]) == x and int(coords[3]) == y:
                    is_possible = True
                    break
        elif self.move_to:
            # Second phase: showing where arrow can be placed
            for move in self.possible_moves:
                coords = move.split(',')
                if (int(coords[0]) == self.selected_piece[0] and
                    int(coords[1]) == self.selected_piece[1] and
                    int(coords[2]) == self.move_to[0] and
                    int(coords[3]) == self.move_to[1] and
                    int(coords[4]) == x and
                    int(coords[5]) == y):
                    is_possible = True
                    break

        # Determine display character and style
        if cell == Amazons.w_amazon_sq:
            char = "♛"
            style = self.COLORS['white_amazon']
        elif cell == Amazons.b_amazon_sq:
            char = "♛"
            style = self.COLORS['black_amazon']
        elif cell == Amazons.block_sq:
            char = "█"
            style = self.COLORS['block']
        else:
            char = "·"
            style = self.COLORS['empty']

        # Override style based on state
        if is_selected:
            style = self.COLORS['selected']
        elif is_cursor:
            style = self.COLORS['cursor']
        elif is_move_target:
            style = self.COLORS['selected']
        elif is_possible:
            style = self.COLORS['possible_move']
            char = "◉" if cell == Amazons.empty_sq else char

        return Text(f" {char} ", style=style)

    def render_board(self) -> Table:
        """Render the game board as a Rich table"""
        table = Table(
            show_header=True,
            header_style=self.COLORS['board_border'],
            box=box.DOUBLE_EDGE,
            padding=(0, 0),
            collapse_padding=True,
            border_style=self.COLORS['board_border']
        )

        # Add column headers
        table.add_column("", justify="right", style=self.COLORS['board_border'])
        for i in range(1, self.game.boardsize + 1):
            table.add_column(str(i), justify="center", width=3)

        # Add rows (reversed to show board from top to bottom)
        for x in range(self.game.boardsize, 0, -1):
            row_data = [Text(str(x), style=self.COLORS['board_border'])]
            for y in range(1, self.game.boardsize + 1):
                cell = self.game.board[x][y]
                row_data.append(self.get_cell_display(x, y, cell))
            table.add_row(*row_data)

        return table

    def render_info_panel(self) -> Panel:
        """Render information panel with game status"""
        current_player = "White ♛" if self.game.active == Amazons.w_amazon_sq else "Black ♛"
        player_style = "bold bright_white" if self.game.active == Amazons.w_amazon_sq else "bold bright_red"

        info = Text()
        info.append(f"Current Player: ", style="bold")
        info.append(f"{current_player}\n", style=player_style)
        info.append(f"Move: {self.move_count}\n\n", style="dim")
        info.append(f"Status: {self.status_message}\n\n", style="italic")

        if not self.game_over:
            info.append("Controls:\n", style="bold underline")
            info.append("Arrow Keys - Move cursor\n", style="dim")
            info.append("Space/Enter - Select\n", style="dim")
            info.append("Esc - Cancel selection\n", style="dim")
            info.append("Q - Quit game\n", style="dim")
            info.append("R - Restart game\n", style="dim")
        else:
            winner_name = "White" if self.winner == Amazons.w_amazon_sq else "Black"
            info.append(f"\n{winner_name} wins!\n", style="bold green")
            info.append("Press R to restart or Q to quit", style="italic")

        return Panel(
            Align.center(info),
            title="Game Info",
            border_style=self.COLORS['board_border'],
            padding=(1, 2)
        )

    def render_legend(self) -> Panel:
        """Render legend explaining the symbols"""
        legend = Text()
        legend.append("♛ ", style=self.COLORS['white_amazon'])
        legend.append("White Amazon  ")
        legend.append("♛ ", style=self.COLORS['black_amazon'])
        legend.append("Black Amazon\n")
        legend.append("█ ", style=self.COLORS['block'])
        legend.append("Arrow Block   ")
        legend.append("◉ ", style=self.COLORS['possible_move'])
        legend.append("Possible Move\n")
        legend.append("  ", style=self.COLORS['cursor'])
        legend.append("Cursor        ")
        legend.append("  ", style=self.COLORS['selected'])
        legend.append("Selected")

        return Panel(
            legend,
            title="Legend",
            border_style=self.COLORS['board_border'],
            padding=(0, 1)
        )

    def render(self) -> Layout:
        """Render the complete UI"""
        layout = Layout()
        layout.split_column(
            Layout(name="title", size=3),
            Layout(name="main"),
            Layout(name="legend", size=5)
        )

        layout["main"].split_row(
            Layout(name="board", ratio=2),
            Layout(name="info", ratio=1)
        )

        # Title
        title = Text("AMAZONS", style="bold bright_cyan", justify="center")
        layout["title"].update(Panel(title, border_style="bright_cyan"))

        # Game components
        layout["board"].update(Align.center(self.render_board()))
        layout["info"].update(self.render_info_panel())
        layout["legend"].update(self.render_legend())

        return layout

    def check_game_over(self) -> bool:
        """Check if current player has any moves left"""
        active_moves = []
        for amazon in self.game.pieces[self.game.active]:
            x_from = int(amazon.split(",")[0])
            y_from = int(amazon.split(",")[1])
            active_moves.extend(self.game.get_moves(x_from, y_from))

        if len(active_moves) == 0:
            self.game_over = True
            self.winner = Amazons.b_amazon_sq if self.game.active == Amazons.w_amazon_sq else Amazons.w_amazon_sq
            return True
        return False

    def handle_select(self):
        """Handle selection/action at current cursor position"""
        if self.game_over:
            return

        cell = self.game.board[self.cursor_x][self.cursor_y]

        # Phase 1: Select an amazon to move
        if not self.selected_piece:
            if cell == self.game.active:
                self.selected_piece = (self.cursor_x, self.cursor_y)
                self.possible_moves = self.game.get_moves(self.cursor_x, self.cursor_y)
                if self.possible_moves:
                    player = "White" if self.game.active == Amazons.w_amazon_sq else "Black"
                    self.status_message = f"{player}: Select where to move the amazon"
                else:
                    self.selected_piece = None
                    self.status_message = "This amazon has no valid moves!"
            else:
                self.status_message = "Select one of your amazons to move!"

        # Phase 2: Select where to move the amazon
        elif not self.move_to:
            # Check if cursor is on a valid move destination
            valid_move = False
            for move in self.possible_moves:
                coords = move.split(',')
                if int(coords[2]) == self.cursor_x and int(coords[3]) == self.cursor_y:
                    valid_move = True
                    break

            if valid_move:
                self.move_to = (self.cursor_x, self.cursor_y)
                player = "White" if self.game.active == Amazons.w_amazon_sq else "Black"
                self.status_message = f"{player}: Select where to place the arrow"
            else:
                self.status_message = "Invalid move! Select a highlighted square or press Esc to cancel"

        # Phase 3: Select where to place the arrow
        else:
            # Check if this completes a valid move
            valid_arrow = False
            complete_move = f"{self.selected_piece[0]},{self.selected_piece[1]},{self.move_to[0]},{self.move_to[1]},{self.cursor_x},{self.cursor_y}"

            if complete_move in self.possible_moves:
                valid_arrow = True

            if valid_arrow:
                # Execute the move
                self.game.move(
                    self.selected_piece[0], self.selected_piece[1],
                    self.move_to[0], self.move_to[1],
                    self.cursor_x, self.cursor_y
                )
                self.move_count += 1

                # Reset selection state
                self.selected_piece = None
                self.move_to = None
                self.possible_moves = []

                # Check if game is over
                if not self.check_game_over():
                    player = "White" if self.game.active == Amazons.w_amazon_sq else "Black"
                    self.status_message = f"{player}'s turn - Select an amazon to move"
                else:
                    winner_name = "White" if self.winner == Amazons.w_amazon_sq else "Black"
                    self.status_message = f"Game Over! {winner_name} wins!"
            else:
                self.status_message = "Invalid arrow placement! Select a highlighted square or press Esc to cancel"

    def handle_cancel(self):
        """Cancel current selection"""
        if self.move_to:
            self.move_to = None
            player = "White" if self.game.active == Amazons.w_amazon_sq else "Black"
            self.status_message = f"{player}: Select where to move the amazon"
        elif self.selected_piece:
            self.selected_piece = None
            self.possible_moves = []
            player = "White" if self.game.active == Amazons.w_amazon_sq else "Black"
            self.status_message = f"{player}'s turn - Select an amazon to move"

    def reset_game(self):
        """Reset the game to initial state"""
        self.game = Amazons(self.game.boardsize)
        if self.game.boardsize == 10:
            self.setup_standard_game()
        else:
            self.setup_small_game()
        self.cursor_x = 1
        self.cursor_y = 1
        self.selected_piece = None
        self.move_to = None
        self.possible_moves = []
        self.status_message = "White's turn - Select an amazon to move"
        self.game_over = False
        self.winner = None
        self.move_count = 0

    def play(self):
        """Main game loop"""
        with Live(self.render(), console=self.console, refresh_per_second=10, screen=True) as live:
            while True:
                live.update(self.render())

                # Get input
                key = readchar.readkey()

                # Handle input
                if key == 'q' or key == 'Q':
                    break
                elif key == 'r' or key == 'R':
                    self.reset_game()
                elif key == readchar.key.UP:
                    if self.cursor_x < self.game.boardsize:
                        self.cursor_x += 1
                elif key == readchar.key.DOWN:
                    if self.cursor_x > 1:
                        self.cursor_x -= 1
                elif key == readchar.key.RIGHT:
                    if self.cursor_y < self.game.boardsize:
                        self.cursor_y += 1
                elif key == readchar.key.LEFT:
                    if self.cursor_y > 1:
                        self.cursor_y -= 1
                elif key == ' ' or key == readchar.key.ENTER or key == '\r' or key == '\n':
                    self.handle_select()
                elif key == readchar.key.ESC or key == '\x1b':
                    self.handle_cancel()


def show_menu():
    """Show main menu and return user choice"""
    console = Console()

    console.clear()
    console.print(Panel(
        Text("AMAZONS", style="bold bright_cyan", justify="center"),
        border_style="bright_cyan"
    ))

    menu = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    menu.add_column(justify="center")

    menu.add_row(Text("1. Standard Game (10x10, 4 amazons each)", style="bold white"))
    menu.add_row(Text("2. Quick Game (6x6, 2 amazons each)", style="bold white"))
    menu.add_row(Text("3. Watch AI vs AI (Random moves)", style="bold white"))
    menu.add_row(Text("Q. Quit", style="bold red"))

    console.print(Align.center(menu))
    console.print()
    console.print("[bold]Select an option:[/bold] ", end="")

    choice = readchar.readkey()
    return choice


def watch_ai_game(boardsize: int = 10):
    """Watch AI play against itself"""
    console = Console()
    game = Amazons(boardsize)

    if boardsize == 10:
        game.set_amazon(1, 4, "b")
        game.set_amazon(1, 7, "b")
        game.set_amazon(4, 1, "b")
        game.set_amazon(4, 10, "b")
        game.set_amazon(10, 4, "w")
        game.set_amazon(10, 7, "w")
        game.set_amazon(7, 1, "w")
        game.set_amazon(7, 10, "w")
    else:
        game.set_amazon(1, 1, "b")
        game.set_amazon(1, boardsize, "b")
        game.set_amazon(boardsize, boardsize, "w")
        game.set_amazon(boardsize, 1, "w")

    winner, moves = game.play(display=True, delay=0.3)

    winner_name = "White" if winner == Amazons.w_amazon_sq else "Black"
    console.print(f"\n[bold green]{winner_name} wins after {moves} moves![/bold green]")
    console.print("\nPress any key to return to menu...")
    readchar.readkey()


def main():
    """Main entry point"""
    while True:
        choice = show_menu()

        if choice == '1':
            tui = AmazonsTUI(10)
            tui.setup_standard_game()
            tui.play()
        elif choice == '2':
            tui = AmazonsTUI(6)
            tui.setup_small_game()
            tui.play()
        elif choice == '3':
            watch_ai_game(10)
        elif choice.lower() == 'q':
            break


if __name__ == "__main__":
    main()
