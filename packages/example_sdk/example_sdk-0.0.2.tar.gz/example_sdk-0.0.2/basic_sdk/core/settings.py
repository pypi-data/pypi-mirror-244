import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, DirectoryPath

BASEPATH = Path(os.path.dirname(os.path.realpath(__file__))).parent


class GeneralSettings(BaseSettings):
    ...
