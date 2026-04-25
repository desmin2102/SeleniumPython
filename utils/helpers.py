"""Helper utilities cho framework.

Đọc config theo môi trường (dev/staging/prod) - chọn qua biến môi trường TEST_ENV
hoặc CLI flag --env. Mỗi giá trị trong config có thể bị override bằng biến môi trường
viết HOA, ví dụ TEST_HEADLESS=false sẽ ghi đè headless trong file.
"""

import configparser
import json
import os

DEFAULT_ENV = "dev"
ENV_VAR_PREFIX = "TEST_"  # Tiền tố cho env var override (TEST_HEADLESS, TEST_BROWSER...)


def _project_root():
    return os.path.dirname(os.path.dirname(__file__))


def read_config(env=None):
    """Đọc config theo môi trường.

    Thứ tự ưu tiên:
    1. Env var TEST_<KEY> (vd TEST_BROWSER=firefox)
    2. Section [<env>] trong config.ini
    3. Section [DEFAULT]

    `env` lấy từ:
    - tham số truyền vào (cao nhất)
    - env var TEST_ENV
    - DEFAULT_ENV ('dev')
    """
    env = env or os.environ.get("TEST_ENV", DEFAULT_ENV)
    file_path = os.path.join(_project_root(), "config", "config.ini")

    parser = configparser.ConfigParser()
    parser.read(file_path, encoding="utf-8")

    section = env if env in parser else "DEFAULT"
    cfg = dict(parser[section])

    # Override bằng env var TEST_<KEY>
    for key in cfg:
        env_key = f"{ENV_VAR_PREFIX}{key.upper()}"
        if env_key in os.environ:
            cfg[key] = os.environ[env_key]

    cfg["_env"] = env
    return cfg


def read_test_data():
    """Đọc testdata/test_data.json - dùng làm fixture."""
    file_path = os.path.join(_project_root(), "testdata", "test_data.json")
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
