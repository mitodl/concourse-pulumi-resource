import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)
fileHandler = logging.FileHandler("/var/log/pulumi.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
