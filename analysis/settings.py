import os
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent

DEFAULT_FASTTEXT_ID_BIN_FILE = str(ROOT_PATH / "data" / "cc.id.300.bin")

def get_default(key, default):
  if key in os.environ:
    return os.environ[key]
  return default

FASTTEXT_ID_BIN_FILE = get_default('FASTTEXT_ID_BIN_FILE', DEFAULT_FASTTEXT_ID_BIN_FILE)
