import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = Path(os.environ["ROOT_DIR"])

# Application style variables
LOGO_PATH = Path(os.path.join(ROOT_DIR, "images/logo-littlebigcode.png"))
STYLE_CSS_PATH = Path(os.path.join(ROOT_DIR, "styling/style.css"))
DESCRIPTION_APP = "Projet de reconnaissance faciale."
