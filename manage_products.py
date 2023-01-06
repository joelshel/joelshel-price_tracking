#!/usr/bin/env python3

from os.path import isfile


FILE = "products_list.tab"


def create_file(file):
    """Creates the file in case it doesn't exist.

    Args:
        file (str): The file we want to check if exists and create it in case it doesn't exit.
    """

    if not (isfile(file)):
        with open(file, "w") as f:
            f.write("LINK\tPRODUCT\n")


def menu():
    """Creates the menu"""

    while True:
        print("What do you want to do?")
        print("Create entry [1]")
        print("Remove entry [2]")
        print("Change entry [3]")
        print("EXIT         [4]")
        
        try:
            option = int(input().strip())
        except ValueError:
            option = 5
        
        if option == 1:
            create_entry()
        elif option == 2:
            remove_entry()
        elif option == 3:
            change_entry()
        elif option == 4:
            print("\nEXITING PROGRAM")
            return
        else:
            print("\nINVALID OPTION\n")


def create_entry():
    """Creates a new entry in the file."""

    link = input("Insert link:\n").strip()
    
    if not link:
        print("You need to insert a link to continue")
        return
    
    with open(FILE, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        if link == line.split("\t")[0]:
            print("This link is already in use, if you want choose change entry option")
            return
    
    product = input("Insert product name:\n").strip()
    
    if not link:
        print("You need to insert a product name to continue")
        return


    with open(FILE, "a") as f:
        f.write(f"{link}\t{product}\n")


def remove_entry():
    """Removes an entry in the file."""

    to_remove = input("Insert link or product name:\n").strip()

    with open(FILE, "r") as f:
        lines = f.readlines()

    with open(FILE, "w") as f:
        for line in lines:
            if to_remove in line.split("\t"):
                entry = 1
                continue
            f.write(line)
        
        try:
            entry
        except UnboundLocalError:
            print("\nLink or product not found\n")


def change_entry():
    """Changes an entry in the file."""

    link = input("Insert link:\n").strip()
    product = input("Insert new product name:\n").strip()

    with open(FILE, "r") as f:
        lines = f.readlines()

    with open(FILE, "w") as f:
        for line in lines:
            if link in line.split("\t"):
                f"{link}\t{product}\n"
                entry = 1
            f.write(line)
        
    try:
        entry
    except UnboundLocalError:
        print("\nLink or product not found\n")


def main():
    create_file(FILE)
    menu()


if __name__ == '__main__':
    main()
