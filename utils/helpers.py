"""Các hàm tiện ích dùng chung trong project."""

import configparser
import json
import os


def _project_root():
    """Trả về đường dẫn thư mục gốc của project."""
    return os.path.dirname(os.path.dirname(__file__))


def read_config():
    """Đọc file config.ini và trả về dict các giá trị cấu hình."""
    file_path = os.path.join(_project_root(), "config", "config.ini")
    parser = configparser.ConfigParser()
    parser.read(file_path, encoding="utf-8")
    return dict(parser["DEFAULT"])


def read_test_data():
    """Đọc file test_data.json và trả về dict dữ liệu test."""
    file_path = os.path.join(_project_root(), "testdata", "test_data.json")
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
