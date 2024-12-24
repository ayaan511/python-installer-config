#!/usr/bin/env python3

import sys
import os
import subprocess

# Global variables dictionary
variables = {}

def interpret_ayaan(file_path):
    try:
        print(f"Running file: {file_path}")
        with open(file_path, 'r') as file:
            lines = file.readlines()

            i = 0
            while i < len(lines):
                line = lines[i].strip()

                if line.startswith("::"):
                    i += 1
                    continue  # Ignore comments

                if line.startswith("repeat"):
                    repeat_count = int(line.split()[1])
                    block = []
                    i += 1
                    while not lines[i].strip().startswith("end repeat"):
                        block.append(lines[i].strip())
                        i += 1
                    for _ in range(repeat_count):
                        for repeat_line in block:
                            interpret_line(repeat_line)
                else:
                    interpret_line(line)
                i += 1

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")

def interpret_line(line):
    global variables

    # Print command
    if line.startswith("psyska -/"):
        text = line[9:].strip('"')
        for var, value in variables.items():
            text = text.replace(f"{{{var}}}", str(value))
        print(text)

    # Set a variable
    elif line.startswith("set "):
        parts = line[4:].split(" = ")
        variables[parts[0]] = int(parts[1])

    # Add to a variable
    elif line.startswith("add "):
        parts = line[4:].split(",")
        var_name = parts[0].strip()
        value = parts[1].strip()

        # Check if the second part is a variable or a number
        if value in variables:  # It's a variable
            value = variables[value]
        else:  # It's a raw number
            value = int(value)

        # Add the value to the variable
        if var_name in variables:
            variables[var_name] += value
        else:
            print(f"Error: Variable '{var_name}' not found.")

    # Ask number command
    elif line.startswith("asknum "):
        var_name = line.split()[1].strip()
        try:
            user_input = int(input(f"Enter a number for {var_name}: "))
            variables[var_name] = user_input
        except ValueError:
            print(f"Error: Invalid number entered for {var_name}.")

    # Pause command
    elif line == "pause":
        input("Press Enter to continue...")

    # Reverse text
    elif line.startswith("reverse text -/"):
        text = line[15:].strip('"')
        print(text[::-1])

    # Uppercase text
    elif line.startswith("uppercase text -/"):
        text = line[17:].strip('"')
        print(text.upper())

    # Exit command
    elif line == "exit":
        print("Program ended.")
        sys.exit(0)

    # Play file command
    elif line.startswith("plaayaan"):
        file_path = input("Enter the file path to play: ").strip()
        if os.path.exists(file_path):
            try:
                print(f"Opening file: {file_path}")
                if os.name == "nt":  # Windows
                    os.startfile(file_path)
                elif os.name == "posix":  # macOS/Linux
                    subprocess.call(("open", file_path))
            except Exception as e:
                print(f"Error opening file: {e}")
        else:
            print(f"Error: File '{file_path}' does not exist.")

    else:
        print(f"Unknown command: {line}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ayaan <script.ayaan>")
    else:
        interpret_ayaan(sys.argv[1])
