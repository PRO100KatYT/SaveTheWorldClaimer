import os
import subprocess


def set_and_display_title() -> None:
    if os.name == "nt":
        os.system("title Save the World Claimer")
    else:
        print("\033]0;Save the World Claimer\007", end="", flush=True)
    print("Save the World Claimer v2.0.0 by PRO100KatYT\n")
