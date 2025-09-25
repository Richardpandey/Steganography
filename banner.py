import pyfiglet
from termcolor import colored

def show_banner():
    banner = pyfiglet.figlet_format("SteganoTool", font="jazmine")
    print(colored(banner, "green"))

    print(colored(" Steganography Tool for Hiding Messages in Images/Videos"))
    print()
    print(colored("👤 Author: Richard | GitHub: Richardpandey", "green"))
    print()
    print(colored("Version: 1.0", "green"))
    print()
    print(colored("------------------------------------------------------------\n", "white"))
