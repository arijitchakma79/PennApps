import os
import sys
import time

class Console:
    @staticmethod
    def clear_screen():
        if os.name == 'nt':  # for Windows
            _ = os.system('cls')
        else:  # for Unix/Linux/macOS
            _ = os.system('clear')

    @staticmethod
    def get_terminal_size():
        return os.get_terminal_size().columns, os.get_terminal_size().lines

    @staticmethod
    def create_clean_area(num_lines):
        width, height = Console.get_terminal_size()
        for _ in range(num_lines):
            sys.stdout.write("\n")
        sys.stdout.write("\033[{}A".format(num_lines))  # Move cursor up
        sys.stdout.flush()

        for t in range(num_lines):
            Console.update_value(t, "")

    @staticmethod
    def update_value(row, text):
        sys.stdout.write(f'\033[{row};0H\033[K{text}')  # Move cursor, clear line, write text
        sys.stdout.flush()