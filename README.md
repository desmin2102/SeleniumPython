# SauceDemo Automation - Selenium + Python + Pytest

Automation test suite cho trang [SauceDemo](https://www.saucedemo.com) với 87 test cases bao phủ toàn bộ tính năng.

## Tech Stack
- **Ngôn ngữ:** Python 3.10+
- **Framework:** Pytest 8.x
- **Automation:** Selenium WebDriver 4.x
- **Browsers:** Chrome / Firefox / Edge (chuyển qua config hoặc CLI flag)
- **Driver:** webdriver-manager (tự download driver tương ứng)
- **Parallel:** pytest-xdist (`-n auto`)
- **Retry flaky:** pytest-rerunfailures
- **Report:** pytest-html
- **Lint/format:** ruff + pre-commit
- **Design pattern:** Page Object Model (POM)

## Cấu trúc project
```
selenium-python-demo/
├── config/config.ini              # Multi-env config (DEFAULT/dev/staging/prod)
├── pages/                         # Page Object (9 files)
│   ├── base_page.py               # Class cha - wait, click, send_keys, log
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   ├── checkout_step1_page.py
│   ├── checkout_step2_page.py
│   ├── checkout_complete_page.py
│   ├── menu_page.py
│   └── footer_page.py
├── tests/                         # Test cases (9 files, 87 tests)
│   ├── conftest.py                # Fixtures (driver, config, test_data) + hooks
│   ├── test_login.py              # 20 tests (đã parametrize)
│   ├── test_inventory.py          # 19 tests
│   ├── test_product_detail.py     # 4 tests
│   ├── test_cart.py               # 7 tests
│   ├── test_checkout.py           # 23 tests (3 step)
│   ├── test_menu.py               # 5 tests
│   ├── test_footer.py             # 4 tests
│   ├── test_url_security.py       # 3 tests (đã parametrize, dùng config)
│   └── test_e2e.py                # 2 tests
├── utils/
│   ├── helpers.py                 # Đọc config theo env, đọc test_data.json
│   ├── logger.py                  # Logger ghi ra console + logs/test_*.log
│   └── driver_factory.py          # Factory tạo WebDriver Chrome/Firefox/Edge
├── testcases/
│   ├── generate_testcases.py      # Sinh Excel test cases
│   └── SauceDemo_TestCases.xlsx
├── testdata/test_data.json        # Credentials 6 user types + checkout info
├── reports/                       # HTML report
├── screenshots/                   # PNG sau mỗi test
├── logs/                          # File log mỗi test run
├── .github/workflows/tests.yml    # CI/CD: lint + test parallel
├── pyproject.toml                 # Cấu hình ruff
├── .pre-commit-config.yaml        # Hook tự lint trước commit
├── requirements.txt
└── pytest.ini                     # Markers + log + reruns
```

## Setup

```bash
# Tạo virtual env
python -m venv venv

# Active venv
source venv/Scripts/activate    # Windows (Git Bash)
venv\Scripts\activate           # Windows (CMD)
source venv/bin/activate        # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# (Optional) Cài pre-commit hook để tự lint trước commit
pip install pre-commit && pre-commit install
```

## Chạy tests

### Cú pháp cơ bản
```bash
# Toàn bộ 87 tests (tuần tự)
pytest

# Chạy parallel theo số CPU - nhanh hơn nhiều
pytest -n auto

# 1 module
pytest tests/test_login.py

# Theo marker
pytest -m login          # 20 login tests
pytest -m e2e            # 2 E2E tests
pytest -m security       # 3 URL security tests
```

### Chuyển browser / môi trường

| Cách | Ví dụ |
|------|-------|
| CLI flag | `pytest --browser firefox --env staging` |
| Env var | `TEST_BROWSER=edge TEST_HEADLESS=false pytest` |
| Sửa file | `config/config.ini` -> đổi section `[dev]` / `[staging]` / `[prod]` |

Thứ tự ưu tiên: **CLI flag > env var > config.ini**.

Env var override theo pattern `TEST_<KEY>`: `TEST_BROWSER`, `TEST_HEADLESS`, `TEST_BASE_URL`, `TEST_ENV`.

### Chạy có giao diện (debug local)
```bash
TEST_HEADLESS=false pytest tests/test_login.py
# hoặc sửa [dev] trong config.ini
```

## Output sau khi chạy

| File/Folder | Nội dung |
|-------------|----------|
| `reports/report.html` | HTML report (pass/fail, thời gian, TC ID, screenshot embedded) |
| `screenshots/` | PNG mỗi test, tên = `{TC_ID}_{PASS/FAIL}[_{param}].png` |
| `logs/test_<timestamp>.log` | Full log DEBUG (click, send_keys, navigation) - rất hữu ích khi CI fail |

## Lint / format

```bash
ruff check .         # Check lỗi
ruff check . --fix   # Auto fix
ruff format .        # Format code
pre-commit run --all-files   # Chạy mọi hook lên toàn project
```

## Test cases theo module (87 tổng cộng)

| Module            | Số test | Marker       |
|-------------------|---------|--------------|
| Login             | 20      | `login`      |
| Inventory         | 19      | `inventory`  |
| Product Detail    | 4       | `product`    |
| Cart              | 7       | `cart`       |
| Checkout (3 step) | 23      | `checkout`   |
| Menu              | 5       | `menu`       |
| Footer            | 4       | `footer`     |
| URL Security      | 3       | `security`   |
| E2E               | 2       | `e2e`        |

## Findings / Bugs phát hiện được

1. **TC_CHK1_009 - Whitespace-only first name**: Site accept khoảng trắng làm first name (đáng lẽ phải reject).
2. **TC_INV_019 - Sort reset**: Vào product detail rồi back về inventory thì sort bị reset.
3. **Chrome password leak dialog**: Password `secret_sauce` nằm trong list breach của Chrome - đã fix bằng Chrome options trong [driver_factory.py](utils/driver_factory.py).

## CI/CD

[.github/workflows/tests.yml](.github/workflows/tests.yml) chạy:
- **Lint job:** `ruff check` + `ruff format --check` (block test nếu fail).
- **Test job:** install browser theo matrix, chạy `pytest -n auto`, retry 1 lần với flaky test.
- Trigger: push/PR vào main, manual dispatch (chọn browser), cron 9h sáng VN.
- Artifact: report + screenshots + logs (giữ 14 ngày).
