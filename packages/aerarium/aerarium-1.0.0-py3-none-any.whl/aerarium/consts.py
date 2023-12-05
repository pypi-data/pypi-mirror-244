import os
import sys

HOME = os.path.expanduser("~")
AERARIUM_PATH = os.path.join(HOME, ".config", "aerarium")

CONFIG_FILE_PATH = os.path.join(AERARIUM_PATH, "config.yaml")
DATA_FILE_PATH = os.path.join(AERARIUM_PATH, "transactions.json")
