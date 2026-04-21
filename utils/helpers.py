"""Helper utilities cho framework."""

import os
import configparser


def read_config(file_path=None):
    # Đọc config từ config/config.ini, trả về section DEFAULT
    if file_path is None:
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "config.ini"
        )
    config = configparser.ConfigParser()
    config.read(file_path)
    return config["DEFAULT"]
