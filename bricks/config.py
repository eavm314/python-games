from pathlib import Path

TITLE = "Brick Game"  # Window title.
WIDTH = 640   # Screen width.
HEIGHT = 480  # Screen height.

LEVEL_CONFIG_PATH = Path(__file__).resolve().parent / "level_configs.json"

UNLOCKED_LEVELS = True