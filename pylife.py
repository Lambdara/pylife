import curses

from random import randint
import time

interval = 0.1

def main(screen):
    global interval, old_time

    screen.clear()

    height, width = screen.getmaxyx()
    height, width = height - 1, width - 1

    grid = [[randint(0,1) for _ in range(height)] for _ in range (width)]

    # Draw grid
    for x in range(width):
        for y in range(height):
            screen.addstr(y, x, 'X' if grid[x][y] else ' ')

    while True:
        old_time = time.time()
        # Update grid
        updates = []
        for x in range(width):
            for y in range(height):
                n_neighbours = 0
                # Calculate amount of neighbours
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if not (dx == 0 and dy == 0) and grid[(x+dx)%width][(y+dy)%height]:
                            n_neighbours += 1
                if not grid[x][y] and n_neighbours == 3:
                    updates.append((x,y,1))
                elif grid[x][y] and n_neighbours not in [2,3]:
                    updates.append((x,y,0))

        for x,y,value in updates:
            if value == 0:
                grid[x][y] = 0
                screen.addstr(y, x, ' ')
            else:
                grid[x][y] = 1
                screen.addstr(y, x, 'X')

        # Update screen and wait to get desired refresh rate
        screen.refresh()
        new_time = time.time()
        time.sleep(max(0, interval - new_time + old_time))
    screen.getkey()

curses.wrapper(main)
