#!/usr/bin/env python3
"""Pop the Lock - terminal edition."""
import curses
import math
import os
import random
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
------------------------############%#*#%@@@@@@@%%%@@@@@@@@%**%############+------------------------
------------------------#######%@@@@@@@@@@@@@@@%###%@@@@@@@@@@@@@@@%#######+------------------------
------------------------##%@@@@@@@@@@@@@@@@@@@@%###%@@@@@@@@@@@@@@@@@@@@%##+------------------------
-----------------------+@@@@@@@@@@@@@@@@@@@@@@@%###%@@@@@@@@@@@@@@@@@@@@@@@*------------------------
--------------------=@@@@@@@@@@@@@@@@@@@@@@@@@@%###%@@@@@@@@@@@@@@@@@@@@@@@@@@*---------------------
------------------#@@@@@@@@@@@@@@@@@@@@@@@@@@@@%###%@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=------------------
----------------%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=----------------
--------------%@@@@@@@@@@@@@@@@@@@@@@@%*=------------------+#@@@@@@@@@@@@@@@@@@@@@@@@=--------------
------------+@@@#......-@@@@@@@@@@#-----------------------------*@@@@@@@@@@@@@@@@@@@@@#-------------
-----------%@@@%........+@@@@@@*-----------------------------------=@@@@@@@@@@@@@@@@@@@@=-----------
---------=@@@@@@-.......@@@@%-----------------------------------------#@@@@@@@@@@@@@@@@@@+----------
--------=@@@@@@@@@#=-*@@@@@---------------------------------------------#@@@@@@@@@@@@@@@@@+---------
-------=@@@@@@@@@@@@@@@@@=------------------------------------------------@@@@@@@@@@@@@@@@@+--------
-------%@@@@@@@@@@@@@@@@--------------------::::::::::---------------------#@@@@@@@@@@@@@@@@=-------
------*@@@@@@@@@@@@@@@@---------------------::::::::::----------------------#@@@@@@@@@@@@@@@%-------
------@@@@@@@@@@@@@@@@---------------------------:::::-----------------------%@@@@@@@@@@@@@@@+------
-----*@@@@@@@@@@@@@@@+---------------------------:::::-----------------------=@@@@@@@@@@@@@@@#------
-----#@@@@@@@@@@@@@@@----------------------------:::::------------------------@@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@@----------------------------:::::------------------------*@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@%----------------------------:::::------------------------*@@@@@@@@@@@@@@@------
-----%@@@@@@@@@@@@@@@----------------------------:::::------------------------#@@@@@@@@@@@@@@@------
-----#@@@@@@@@@@@@@@@----------------------------:::::------------------------@@@@@@@@@@@@@@%-------
-----+@@@@@@@@@@@@@@@%---------------------------:::::-----------------------*@@@@@@@@@@@@@@@*------
------%@@@@@@@@@@@@@@@*--------------------------:::::----------------------=@@@@@@@@@@@@@@@@-------
------=@@@@@@@@@@@@@@@@+--------------------------:::----------------------=@@@@@@@@@@@@@@@@*-------
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


# Center & radii of the round body of the lock (in character cells).
# Body roughly: rows 22..58, cols 16..86 -> center (40, 51), rx ~ 35, ry ~ 17.
RING_CENTER_Y = 40
RING_CENTER_X = 51
RING_RX = 35
RING_RY = 17
RING_POINTS = 90  # number of stops the ball can sit on


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


def draw_lock(stdscr, max_y, max_x):
    for i, line in enumerate(lock_lines()):
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


def center_text(stdscr, row, text, attr=0):
    h, w = stdscr.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    try:
        stdscr.addnstr(row, x, text, w - 1, attr)
    except curses.error:
        pass


def title_screen(stdscr, high_score):
    stdscr.nodelay(False)
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w)
        center_text(stdscr, 1, "*** POP THE LOCK ***", curses.A_BOLD)
        center_text(stdscr, h - 3, f"High Score: {high_score}")
        center_text(stdscr, h - 2, "Press SPACE to start   (Q to quit)", curses.A_BOLD)
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord(" "):
            return
        if ch in (ord("q"), ord("Q")):
            raise SystemExit(0)


def game_over_screen(stdscr, level_reached, high_score, new_record):
    stdscr.nodelay(False)
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w)
        center_text(stdscr, 1, "!!! GAME OVER !!!", curses.A_BOLD)
        center_text(stdscr, 2, f"You reached level {level_reached}")
        if new_record:
            center_text(stdscr, 3, "*** NEW HIGH SCORE! ***", curses.A_BOLD)
        center_text(stdscr, h - 3, f"High Score: {high_score}")
        center_text(stdscr, h - 2, "SPACE = play again   Q = quit", curses.A_BOLD)
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord(" "):
            return
        if ch in (ord("q"), ord("Q")):
            raise SystemExit(0)


def play_level(stdscr, level, direction, ring, high_score):
    """Returns True if the player hit the peg, False if they missed."""
    # Speed: starts slow, gets a tiny bit faster each level.
    delay = max(0.012, 0.055 - (level - 1) * 0.0025)

    # Pick a peg position that's not too close to the start so the player has
    # time to react. Start point is index 0 (rightmost).
    n = len(ring)
    min_gap = max(8, n // 8)
    peg_idx = random.randint(min_gap, n - min_gap)

    ball_idx = 0
    last_step = time.time()
    stdscr.nodelay(True)

    while True:
        now = time.time()
        if now - last_step >= delay:
            ball_idx = (ball_idx + direction) % n
            last_step = now

        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_lock(stdscr, h, w)

        # HUD
        hud_left = f" Level: {level}   High: {high_score} "
        hud_right = " SPACE=lock  Q=quit "
        try:
            stdscr.addnstr(0, 0, hud_left, w - 1, curses.A_BOLD)
            stdscr.addnstr(0, max(0, w - len(hud_right) - 1), hud_right, w - 1)
        except curses.error:
            pass

        # Peg
        py, px = ring[peg_idx]
        if 0 <= py < h and 0 <= px < w:
            safe_addch(stdscr, py, px, "#", curses.A_BOLD | curses.A_REVERSE)

        # Ball
        by, bx = ring[ball_idx]
        if 0 <= by < h and 0 <= bx < w:
            safe_addch(stdscr, by, bx, ".", curses.A_BOLD | curses.A_REVERSE)

        stdscr.refresh()

        ch = stdscr.getch()
        if ch == ord(" "):
            # Allow a tiny tolerance so it doesn't feel super strict.
            tol = 0
            diff = (ball_idx - peg_idx) % n
            diff = min(diff, n - diff)
            return diff <= tol
        if ch in (ord("q"), ord("Q")):
            raise SystemExit(0)

        time.sleep(0.005)


def main(stdscr):
    curses.curs_set(0)
    try:
        curses.start_color()
        curses.use_default_colors()
    except curses.error:
        pass
    stdscr.keypad(True)

    ring = build_ring()
    high_score = load_high_score()

    while True:
        title_screen(stdscr, high_score)

        level = 1
        direction = 1  # start going right (clockwise)

        while True:
            hit = play_level(stdscr, level, direction, ring, high_score)
            if hit:
                level += 1
                direction = -direction  # reverse direction on each successful hit
            else:
                reached = level - 1
                new_record = reached > high_score
                if new_record:
                    high_score = reached
                    save_high_score(high_score)
                game_over_screen(stdscr, reached, high_score, new_record)
                break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
