"""Cấu hình logging cho toàn bộ project - log ra console và file."""

import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
_log_file = os.path.join(LOGS_DIR, f"test_{_timestamp}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_file, encoding="utf-8"),
    ],
)


def get_logger(name):
    """Lấy logger theo tên module."""
    return logging.getLogger(name)
