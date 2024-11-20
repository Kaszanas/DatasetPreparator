import os
from pathlib import Path


LOGGING_FORMAT = "[%(asctime)s][%(process)d/%(thread)d][%(levelname)s][%(filename)s:%(lineno)s] - %(message)s"

PATH_TO_SC2INFOEXTRACTORGO = Path(os.getcwd(), "SC2InfoExtractorGo").resolve()
