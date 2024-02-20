import pygame
import os
import math
import sys
import random

def check_dependency(module_name):
    try:
        __import__(module_name)
        print(f"{module_name} is installed.")
    except ImportError:
        print(f"{module_name} is not installed.")

def main():
    check_dependency("pygame")
    check_dependency("os")
    check_dependency("math")
    check_dependency("sys")
    check_dependency("random")

if __name__ == "__main__":
    main()
