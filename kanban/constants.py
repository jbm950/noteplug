import os
import pathlib

# Probably need a check that Notes Dir exists as an environment variable
NOTES_DIR = pathlib.Path(os.environ["NOTES_DIR"])
PROD_DIR = NOTES_DIR.joinpath("Productivity")

