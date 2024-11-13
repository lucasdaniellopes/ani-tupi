import curses


def __menu(stdscr, menu, result) -> str:
    menu.append("EXIT")
    # Clear the screen
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor
    
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Black text on yellow background

    # Define menu 
    current_option = 0

    while True:
        stdscr.clear()
        
        # Display menu
        for idx, row in enumerate(menu):
            if idx == current_option:
                stdscr.attron(curses.color_pair(1))  # Highlight current option
                stdscr.addstr(idx + 1, 2, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 1, 2, row)

        # Get user input
        key = stdscr.getch()

        # Arrow key navigation
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(menu)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(menu)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(len(menu) + 3, 2, f"You selected '{menu[current_option]}'")
            stdscr.refresh()
            #stdscr.getch()  # Wait for another key press
            result.append(menu[current_option])
            break

def menu(opts: list[str]) -> str:
    selected= [] 
    curses.wrapper(lambda stdscr: __menu(stdscr, opts, result=selected))
    return selected[0]

if __name__ == "__main__":
   main() 

