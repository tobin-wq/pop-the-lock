#!/usr/bin/env python3
"""Pop the Lock - terminal edition."""
import curses
import math
import os
import random
import sys
import time

HIGH_SCORE_FILE = os.path.expanduser("~/.pop_the_lock_high_score")

LOCK = r"""
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
------------------------------------------==+**#####**+==-------------------------------------------
-----------------------------------=*#########################*=------------------------------------
-------------------------------=*#################################*=--------------------------------
-----------------------------*#######################################*------------------------------
---------------------------+###########################################*----------------------------
--------------------------###############################################---------------------------
-------------------------#################################################--------------------------
------------------------*################*=--------------*#################-------------------------
------------------------###############+-------------------+###############-------------------------
------------------------##############+---------------------=##############+------------------------
------------------------##############-----------------------*#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------#############*-----------------------+#############+------------------------
------------------------############%#*#%@@@@@@@@@@@@@@@@@@%**%############+------------------------
------------------------#######%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#######+-------------------------
------------------------##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%##+-------------------------
-----------------------+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*-------------------------
--------------------=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*----------------------
------------------#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=------------------
----------------%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=----------------
--------------%@@@@@@@@@@@@@@@@@@@@@@@%*=------------------+#@@@@@@@@@@@@@@@@@@@@@@@@=--------------
------------+@@@@@@@@@@@@@@@@@@@@@#-----------------------------*@@@@@@@@@@@@@@@@@@@@@#-------------
-----------%@@@@@@@@@@@@@@@@@@@*-----------------------------------=@@@@@@@@@@@@@@@@@@@@=-----------
---------=@@@@@@@@@@@@@@@@@@%-----------------------------------------#@@@@@@@@@@@@@@@@@@+----------
--------=@@@@@@@@@@@@@@@@@@---------------------------------------------#@@@@@@@@@@@@@@@@@+---------
-------=@@@@@@@@@@@@@@@@@=------------------------------------------------@@@@@@@@@@@@@@@@@+--------
-------%@@@@@@@@@@@@@@@@---------------------------------------------------#@@@@@@@@@@@@@@@@=-------
------*@@@@@@@@@@@@@@@@-----------------------------------------------------#@@@@@@@@@@@@@@@%-------
------@@@@@@@@@@@@@@@@-------------------------------------------------------%@@@@@@@@@@@@@@@+------
-----*@@@@@@@@@@@@@@@+-------------------------------------------------------=@@@@@@@@@@@@@@@#------
-----#@@@@@@@@@@@@@@@---------------------------------------------------------@@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@@---------------------------------------------------------*@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@%---------------------------------------------------------*@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@@---------------------------------------------------------#@@@@@@@@@@@@@@@------
-----#@@@@@@@@@@@@@@@---------------------------------------------------------@@@@@@@@@@@@@@%-------
-----+@@@@@@@@@@@@@@@%-------------------------------------------------------*@@@@@@@@@@@@@@@*------
------%@@@@@@@@@@@@@@@*-----------------------------------------------------=@@@@@@@@@@@@@@@@-------
------=@@@@@@@@@@@@@@@@+---------------------------------------------------=@@@@@@@@@@@@@@@@*-------
-------*@@@@@@@@@@@@@@@@*-------------------------------------------------=@@@@@@@@@@@@@@@@%--------
--------#@@@@@@@@@@@@@@@@@=----------------------------------------------%@@@@@@@@@@@@@@@@%---------
---------#@@@@@@@@@@@@@@@@@%-------------------------------------------#@@@@@@@@@@@@@@@@@%----------
----------*@@@@@@@@@@@@@@@@@@@=--------------------------------------%@@@@@@@@@@@@@@@@@@%-----------
-----------=@@@@@@@@@@@@@@@@@@@@%=-------------------------------=#@@@@@@@@@@@@@@@@@@@@+------------
-------------*@@@@@@@@@@@@@@@@@@@@@@#=------------------------*@@@@@@@@@@@@@@@@@@@@@@%--------------
---------------%@@@@@@@@@@@@@@@@@@@@@@@@@@#*+=-------==*#%@@@@@@@@@@@@@@@@@@@@@@@@@@=---------------
-----------------%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=-----------------
-------------------*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--------------------
----------------------#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=----------------------
-------------------------*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--------------------------
-----------------------------*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#=-----------------------------
---------------------------------=+#@@@@@@@@@@@@@@@@@@@@@@@@@@@%*=----------------------------------
------------------------------------------==+*#%@@@%%**+=-------------------------------------------
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
"""


def lock_lines():
    return LOCK.strip("\n").split("\n")


OPEN_LOCK = r"""
-----------------------------------------------------------+++*******************++++---------------
-------------------------------------------------------+********************************+-----------
----------------------------------------------------+**************************************+--------
--------------------------------------------------+******************************************+------
--------------------------------------------------********************************************+-----
------------------------------------------------+****************-------------*****************+----
-----------------------------------------------=**************+------------------**************+----
-----------------------------------------------+************+----------------------*************+---
-----------------------------------------------+************+----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
-----------------------------------------------+***********+-----------------------+************+---
---------------------------------------#%@@@@@@@@@@@@@@@@@@%----------------------------------------
--------------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%---------------------------------
---------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%----------------------------
-----------------------+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*-------------------------
--------------------=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*----------------------
------------------#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=------------------
----------------%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=----------------
--------------%@@@@@@@@@@@@@@@@@@@@@@@%*=------------------+#@@@@@@@@@@@@@@@@@@@@@@@@=--------------
------------+@@@@@@@@@@@@@@@@@@@@@#-----------------------------*@@@@@@@@@@@@@@@@@@@@@#-------------
-----------%@@@@@@@@@@@@@@@@@@@*-----------------------------------=@@@@@@@@@@@@@@@@@@@@=-----------
---------=@@@@@@@@@@@@@@@@@@%-----------------------------------------#@@@@@@@@@@@@@@@@@@+----------
--------=@@@@@@@@@@@@@@@@@@---------------------------------------------#@@@@@@@@@@@@@@@@@+---------
-------=@@@@@@@@@@@@@@@@@=------------------------------------------------@@@@@@@@@@@@@@@@@+--------
-------%@@@@@@@@@@@@@@@@---------------------------------------------------#@@@@@@@@@@@@@@@@=-------
------*@@@@@@@@@@@@@@@@-----------------------------------------------------#@@@@@@@@@@@@@@@%-------
------@@@@@@@@@@@@@@@@-------------------------------------------------------%@@@@@@@@@@@@@@@+------
-----*@@@@@@@@@@@@@@@+-------------------------------------------------------=@@@@@@@@@@@@@@@#------
-----#@@@@@@@@@@@@@@@---------------------------------------------------------@@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@@---------------------------------------------------------*@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@%---------------------------------------------------------*@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@@---------------------------------------------------------#@@@@@@@@@@@@@@@------
-----#@@@@@@@@@@@@@@@---------------------------------------------------------@@@@@@@@@@@@@@%-------
-----+@@@@@@@@@@@@@@@%-------------------------------------------------------*@@@@@@@@@@@@@@@*------
------%@@@@@@@@@@@@@@@*-----------------------------------------------------=@@@@@@@@@@@@@@@@-------
------=@@@@@@@@@@@@@@@@+---------------------------------------------------=@@@@@@@@@@@@@@@@*-------
-------*@@@@@@@@@@@@@@@@*-------------------------------------------------=@@@@@@@@@@@@@@@@%--------
--------#@@@@@@@@@@@@@@@@@=----------------------------------------------%@@@@@@@@@@@@@@@@%---------
---------#@@@@@@@@@@@@@@@@@%-------------------------------------------#@@@@@@@@@@@@@@@@@%----------
----------*@@@@@@@@@@@@@@@@@@@=--------------------------------------%@@@@@@@@@@@@@@@@@@%-----------
-----------=@@@@@@@@@@@@@@@@@@@@%=-------------------------------=#@@@@@@@@@@@@@@@@@@@@+------------
-------------*@@@@@@@@@@@@@@@@@@@@@@#=------------------------*@@@@@@@@@@@@@@@@@@@@@@%--------------
---------------%@@@@@@@@@@@@@@@@@@@@@@@@@@#*+=-------==*#%@@@@@@@@@@@@@@@@@@@@@@@@@@=---------------
-----------------%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=-----------------
-------------------*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--------------------
----------------------#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=----------------------
-------------------------*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--------------------------
-----------------------------*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#=-----------------------------
---------------------------------=+#@@@@@@@@@@@@@@@@@@@@@@@@@@@%*=----------------------------------
------------------------------------------==+*#%@@@%%**+=-------------------------------------------
"""


def open_lock_lines():
    return OPEN_LOCK.strip("\n").split("\n")


# Center & radii of the round body of the lock (in character cells).
# Body roughly: rows 22..58, cols 16..86 -> center (40, 51), rx ~ 35, ry ~ 17.
RING_CENTER_Y = 40
RING_CENTER_X = 51
RING_RX = 35
RING_RY = 17
RING_POINTS = 90  # number of stops the ball can sit on

# Multi-character sprites taken from the lock art itself.
# Spaces in a sprite line are treated as "transparent" (lock shows through).
BALL_SPRITE = [
    " ...... ",
    "........",
    " ....... ",
]

PEG_SPRITE = [
    "###",
    "###",
    "###",
]

# How many pegs the player must lock to win the game.
GOAL = 50

# Big-digit sprites for the goal counter shown in the middle of the lock.
# Every digit is normalized to 6 wide x 5 tall so they line up nicely.
DIGITS = {
    "0": [
        "000000",
        "00  00",
        "00  00",
        "00  00",
        "000000",
    ],
    "1": [
        "1111  ",
        "  11  ",
        "  11  ",
        "  11  ",
        "111111",
    ],
    "2": [
        "222222",
        "     2",
        "222222",
        "2     ",
        "222222",
    ],
    "3": [
        "333333",
        "    33",
        "333333",
        "    33",
        "333333",
    ],
    "4": [
        "44  44",
        "44  44",
        "444444",
        "    44",
        "    44",
    ],
    "5": [
        "555555",
        "55    ",
        "555555",
        "    55",
        "555555",
    ],
    "6": [
        "666666",
        "66    ",
        "666666",
        "66  66",
        "666666",
    ],
    "7": [
        "777777",
        "    77",
        "    77",
        "    77",
        "    77",
    ],
    "8": [
        "888888",
        "88  88",
        "888888",
        "88  88",
        "888888",
    ],
    "9": [
        "999999",
        "99  99",
        "999999",
        "    99",
        "999999",
    ],
}


def build_ring():
    """Compute (y, x) points around the lock body, deduplicated, in clockwise order."""
    pts = []
    seen = set()
    # Start at angle 0 = right side; clockwise = increasing angle with sin flipped.
    for i in range(RING_POINTS * 4):  # oversample, then dedupe
        t = (i / (RING_POINTS * 4)) * 2 * math.pi
        # In screen coords, y grows downward, so for clockwise from "right":
        # x = cx + rx*cos(t), y = cy + ry*sin(t)
        x = int(round(RING_CENTER_X + RING_RX * math.cos(t)))
        y = int(round(RING_CENTER_Y + RING_RY * math.sin(t)))
        key = (y, x)
        if key not in seen:
            seen.add(key)
            pts.append(key)
    return pts


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE) as f:
            return int(f.read().strip())
    except Exception:
        return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass


def draw_lock(stdscr, max_y, max_x, lines=None):
    if lines is None:
        lines = lock_lines()
    for i, line in enumerate(lines):
        if i >= max_y:
            break
        try:
            stdscr.addnstr(i, 0, line, max_x - 1)
        except curses.error:
            pass


def safe_addch(stdscr, y, x, ch, attr=0):
    try:
        stdscr.addstr(y, x, ch, attr)
    except curses.error:
        pass


def draw_sprite(stdscr, cy, cx, sprite, attr=0):
    """Draw a multi-line sprite centered at (cy, cx). Spaces are transparent."""
    h, w = stdscr.getmaxyx()
    sh = len(sprite)
    sw = max(len(line) for line in sprite)
    start_y = cy - sh // 2
    start_x = cx - sw // 2
    for i, line in enumerate(sprite):
        y = start_y + i
        if y < 0 or y >= h:
            continue
        for j, ch in enumerate(line):
            if ch == " ":
                continue
            x = start_x + j
            if x < 0 or x >= w:
                continue
            try:
                stdscr.addstr(y, x, ch, attr)
            except curses.error:
                pass


def sprite_cells(cy, cx, sprite):
    """Return the set of (y, x) screen cells covered by a sprite's non-space chars."""
    cells = set()
    sh = len(sprite)
    sw = max(len(line) for line in sprite)
    start_y = cy - sh // 2
    start_x = cx - sw // 2
    for i, line in enumerate(sprite):
        for j, ch in enumerate(line):
            if ch != " ":
                cells.add((start_y + i, start_x + j))
    return cells


def draw_number(stdscr, cy, cx, number, attr=0):
    """Draw a non-negative integer centered at (cy, cx) using big digits."""
    s = str(number)
    digit_w = 6
    digit_h = 5
    spacing = 1
    total_w = len(s) * digit_w + (len(s) - 1) * spacing
    start_y = cy - digit_h // 2
    start_x = cx - total_w // 2
    h, w = stdscr.getmaxyx()
    for i, ch in enumerate(s):
        sprite = DIGITS.get(ch)
        if sprite is None:
            continue
        x_offset = start_x + i * (digit_w + spacing)
        for row, line in enumerate(sprite):
            y = start_y + row
            if y < 0 or y >= h:
                continue
            for col, c in enumerate(line):
                if c == " ":
                    continue
                x = x_offset + col
                if x < 0 or x >= w:
                    continue
                try:
                    stdscr.addstr(y, x, c, attr)
                except curses.error:
                    pass


def center_text(stdscr, row, text, attr=0):
    h, w = stdscr.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    try:
        stdscr.addnstr(row, x, text, w - 1, attr)
    except curses.error:
        pass


DIFFICULTIES = [
    ("Easy", 15),
    ("Normal", 30),
    ("Hard", 50),
]


def difficulty_menu(stdscr, high_score):
    """Show the title + difficulty menu. Returns the chosen goal (peg count)."""
    selected = 1  # default to Normal
    stdscr.nodelay(False)

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w)
        center_text(stdscr, 1, "*** POP THE LOCK ***", curses.A_BOLD)
        center_text(stdscr, 3, "Choose a difficulty", curses.A_BOLD)

        # Lay out the three options vertically, centered.
        base_row = h // 2 - 2
        for i, (name, goal) in enumerate(DIFFICULTIES):
            row = base_row + i * 2
            if i == selected:
                # Selected option is "bigger": spaced uppercase + arrows +
                # bold/reverse, which makes it visibly wider.
                spaced = " ".join(name.upper())
                text = f">>  {spaced}   ({goal} LEVELS)  <<"
                attr = curses.A_BOLD | curses.A_REVERSE
            else:
                text = f"   {name}  ({goal} levels)   "
                attr = curses.A_BOLD
            x = max(0, (w - len(text)) // 2)
            try:
                stdscr.addnstr(row, x, text, w - 1, attr)
            except curses.error:
                pass

        center_text(stdscr, h - 4, f"High Score: {high_score}")
        center_text(stdscr, h - 3, "UP/DOWN arrows to choose")
        center_text(
            stdscr,
            h - 2,
            "ENTER or SPACE = start   ESC = quit",
            curses.A_BOLD,
        )
        stdscr.refresh()

        ch = stdscr.getch()
        if ch == curses.KEY_UP:
            selected = (selected - 1) % len(DIFFICULTIES)
        elif ch == curses.KEY_DOWN:
            selected = (selected + 1) % len(DIFFICULTIES)
        elif ch in (10, 13, curses.KEY_ENTER, ord(" ")):
            # Resize the terminal window to fit the lock art (xterm escape).
            sys.stdout.write("\033[8;66;101t")
            sys.stdout.flush()
            curses.napms(120)
            curses.resize_term(66, 101)
            return DIFFICULTIES[selected][1]
        elif ch == 27:  # ESC
            raise SystemExit(0)


def win_screen(stdscr, goal, high_score):
    stdscr.nodelay(False)
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w, open_lock_lines())
        center_text(stdscr, h - 3, f"High Score: {high_score}")
        center_text(stdscr, h - 2, "SPACE = play again   ESC = quit", curses.A_BOLD)
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord(" "):
            return
        if ch == 27:  # ESC
            raise SystemExit(0)


def game_over_screen(stdscr, level_reached, pegs_remaining, high_score, new_record):
    stdscr.nodelay(False)
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w)
        # Keep the goal counter visible so the player can see what they died on.
        draw_number(
            stdscr, RING_CENTER_Y, RING_CENTER_X, pegs_remaining, curses.A_BOLD
        )
        center_text(stdscr, 1, "!!! GAME OVER !!!", curses.A_BOLD)
        center_text(stdscr, 2, f"You reached level {level_reached}")
        if new_record:
            center_text(stdscr, 3, "*** NEW HIGH SCORE! ***", curses.A_BOLD)
        center_text(stdscr, h - 3, f"High Score: {high_score}")
        center_text(stdscr, h - 2, "SPACE = play again   ESC = quit", curses.A_BOLD)
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord(" "):
            return
        if ch == 27:  # ESC
            raise SystemExit(0)


def play_level(stdscr, level, pegs_remaining, direction, ring, high_score, start_ball_idx):
    """Plays one peg. Returns (hit, ball_idx_at_end)."""
    # Speed: starts slow, gets a tiny bit faster each level.
    delay = max(0.012, 0.055 - (level - 1) * 0.0025)

    n = len(ring)
    min_gap = max(8, n // 8)

    # Place the peg far enough ahead of the ball in the direction of travel
    # that the player has time to react.
    offset = random.randint(min_gap, n - min_gap)
    peg_idx = (start_ball_idx + direction * offset) % n

    ball_idx = start_ball_idx

    # Hit zone = any visual overlap between the ball's "." cells and the peg's
    # "#" cells. Even one touching counts; auto-out only fires once nothing is
    # touching anymore.
    peg_cells = sprite_cells(*ring[peg_idx], PEG_SPRITE)

    def in_zone(b):
        by, bx = ring[b]
        return bool(sprite_cells(by, bx, BALL_SPRITE) & peg_cells)

    was_in_zone = in_zone(ball_idx)
    last_step = time.time()
    stdscr.nodelay(True)

    while True:
        now = time.time()
        if now - last_step >= delay:
            ball_idx = (ball_idx + direction) % n
            last_step = now
            currently_in_zone = in_zone(ball_idx)
            # Auto-out: if the ball was in the hit zone last frame and is now
            # past the peg without the player pressing SPACE, that's a miss.
            if was_in_zone and not currently_in_zone:
                return False, ball_idx
            was_in_zone = currently_in_zone

        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w)

        # HUD: high score on the left, controls hint on the right.
        hud_left = f" High: {high_score} "
        hud_right = " SPACE=lock  P=pause  ESC=quit "
        try:
            stdscr.addnstr(0, 0, hud_left, w - 1, curses.A_BOLD)
            stdscr.addnstr(0, max(0, w - len(hud_right) - 1), hud_right, w - 1)
        except curses.error:
            pass

        # Big goal counter in the middle of the lock.
        draw_number(
            stdscr, RING_CENTER_Y, RING_CENTER_X, pegs_remaining, curses.A_BOLD
        )

        # Peg (drawn first so the ball appears on top of it during overlap)
        py, px = ring[peg_idx]
        draw_sprite(stdscr, py, px, PEG_SPRITE, curses.A_BOLD | curses.A_REVERSE)

        # Ball
        by, bx = ring[ball_idx]
        draw_sprite(stdscr, by, bx, BALL_SPRITE, curses.A_BOLD | curses.A_REVERSE)

        stdscr.refresh()

        ch = stdscr.getch()
        if ch == ord(" "):
            return in_zone(ball_idx), ball_idx
        if ch == 27:  # ESC
            raise SystemExit(0)
        if ch in (ord("p"), ord("P")):
            # Pause: freeze the ball and wait for P to resume.
            center_text(stdscr, 1, ">>> PAUSED <<<   (P to resume)", curses.A_BOLD)
            stdscr.refresh()
            stdscr.nodelay(False)
            while True:
                pch = stdscr.getch()
                if pch in (ord("p"), ord("P")):
                    break
                if pch == 27:
                    raise SystemExit(0)
            stdscr.nodelay(True)
            # Reset the step timer so the ball doesn't jump after unpausing.
            last_step = time.time()

        time.sleep(0.005)


def main(stdscr):
    curses.curs_set(0)
    try:
        curses.start_color()
        curses.use_default_colors()
    except curses.error:
        pass
    # Make ESC respond instantly instead of waiting ~1s for an escape sequence.
    try:
        curses.set_escdelay(25)
    except (AttributeError, curses.error):
        pass
    stdscr.keypad(True)

    ring = build_ring()
    high_score = load_high_score()

    while True:
        goal = difficulty_menu(stdscr, high_score)

        level = 1
        pegs_remaining = goal  # countdown shown in the middle of the lock
        direction = 1  # start going right (clockwise)
        ball_idx = 0  # ball starts on the right side; persists between pegs

        while True:
            hit, ball_idx = play_level(
                stdscr, level, pegs_remaining, direction, ring, high_score, ball_idx
            )
            if hit:
                pegs_remaining -= 1
                if pegs_remaining == 0:
                    # All pegs locked — you win!
                    if level > high_score:
                        high_score = level
                        save_high_score(high_score)
                    win_screen(stdscr, goal, high_score)
                    break
                level += 1
                # Ball stays where it locked the peg; reverse direction and
                # spawn the next peg further along the new direction.
                direction = -direction
            else:
                reached = level - 1
                new_record = reached > high_score
                if new_record:
                    high_score = reached
                    save_high_score(high_score)
                game_over_screen(stdscr, reached, pegs_remaining, high_score, new_record)
                break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
