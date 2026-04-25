"""Logger dùng chung cho toàn framework.

Mục tiêu:
- Log ra console (theo dõi khi chạy local)
- Log ra file logs/test_<timestamp>.log (xem lại sau, upload lên CI artifact)
- Mỗi module gọi get_logger(__name__) để có namespace riêng
- Cùng 1 file log cho cả test run (1 lần pytest = 1 file log)
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOGS_DIR = "logs"
_LOG_FILE = None  # Cache đường dẫn file log của session hiện tại
_INITIALIZED = False


def _get_log_file():
    """Tạo path file log cho session hiện tại. Cache lại để mọi logger
    cùng ghi vào 1 file."""
    global _LOG_FILE
    if _LOG_FILE is None:
        os.makedirs(LOGS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        _LOG_FILE = os.path.join(LOGS_DIR, f"test_{timestamp}.log")
    return _LOG_FILE


def _init_root_logger():
    """Cấu hình root logger 1 lần duy nhất cho cả session."""
    global _INITIALIZED
    if _INITIALIZED:
        return

    fmt = "%(asctime)s | %(levelname)-7s | %(name)-25s | %(message)s"
    formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")

    root = logging.getLogger("automation")
    root.setLevel(logging.DEBUG)
    root.propagate = False

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    root.addHandler(console)

    # File handler: rotate khi file > 5MB, giữ tối đa 3 file backup
    file_handler = RotatingFileHandler(
        _get_log_file(), maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    _INITIALIZED = True


def get_logger(name):
    """Lấy logger cho module. Convention: get_logger(__name__).

    Tất cả logger đều là child của 'automation' nên config 1 lần ở root là đủ.
    """
    _init_root_logger()
    return logging.getLogger(f"automation.{name}")
