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


def play_level(stdscr, level, direction, ring, high_score, start_ball_idx):
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
    # Tolerance reflects the visual width of the sprites: ball is ~8 wide, peg
    # ~3 wide, ring has ~1.7 chars per stop, so a 2-stop window roughly matches
    # "the ball is touching the peg".
    tol = 2

    def in_zone(b):
        diff = (b - peg_idx) % n
        return diff <= tol or diff >= n - tol

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

        # HUD
        hud_left = f" Level: {level}   High: {high_score} "
        hud_right = " SPACE=lock  Q=quit "
        try:
            stdscr.addnstr(0, 0, hud_left, w - 1, curses.A_BOLD)
            stdscr.addnstr(0, max(0, w - len(hud_right) - 1), hud_right, w - 1)
        except curses.error:
            pass

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
        ball_idx = 0  # ball starts on the right side; persists between pegs

        while True:
            hit, ball_idx = play_level(
                stdscr, level, direction, ring, high_score, ball_idx
            )
            if hit:
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
                game_over_screen(stdscr, reached, high_score, new_record)
                break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
