# SauceDemo Automation - Selenium + Python + Pytest

Automation test suite cho trang [SauceDemo](https://www.saucedemo.com) với 87 test cases bao phủ toàn bộ tính năng.

## Tech Stack
- **Ngôn ngữ:** Python 3.10+
- **Framework:** Pytest 8.x
- **Automation:** Selenium WebDriver 4.x
- **Driver:** webdriver-manager (tự download ChromeDriver)
- **Report:** pytest-html (HTML report), Allure (tuỳ chọn)
- **Design pattern:** Page Object Model (POM)

## Cấu trúc project
```
selenium-python-demo/
├── config/config.ini              # URL, browser, headless setting
├── pages/                         # Page Object (9 files)
│   ├── base_page.py               # Class cha - wait, click, send_keys
│   ├── login_page.py              # Trang login
│   ├── inventory_page.py          # Danh sách sản phẩm
│   ├── product_detail_page.py     # Chi tiết sản phẩm
│   ├── cart_page.py               # Giỏ hàng
│   ├── checkout_step1_page.py     # Nhập thông tin giao hàng
│   ├── checkout_step2_page.py     # Overview đơn hàng
│   ├── checkout_complete_page.py  # Xác nhận đặt hàng thành công
│   ├── menu_page.py               # Menu hamburger
│   └── footer_page.py             # Footer (social links)
├── tests/                         # Test cases (9 files, 87 tests)
│   ├── conftest.py                # Fixtures + hooks (screenshot, HTML)
│   ├── test_login.py              # 20 tests - Login
│   ├── test_inventory.py          # 19 tests - Inventory
│   ├── test_product_detail.py     # 4 tests - Product detail
│   ├── test_cart.py               # 7 tests - Cart
│   ├── test_checkout.py           # 23 tests - Checkout 3 steps
│   ├── test_menu.py               # 5 tests - Menu
│   ├── test_footer.py             # 4 tests - Footer
│   ├── test_url_security.py       # 3 tests - URL security
│   └── test_e2e.py                # 2 tests - End-to-End
├── testcases/
│   ├── generate_testcases.py      # Script sinh Excel test cases
│   └── SauceDemo_TestCases.xlsx   # File Excel 87 test cases
├── testdata/test_data.json        # Test data (credentials, checkout info)
├── utils/helpers.py               # Đọc config.ini
├── reports/                       # HTML report sau khi chạy
├── screenshots/                   # Auto-capture sau mỗi test
├── .github/workflows/tests.yml    # CI/CD GitHub Actions
├── requirements.txt               # Python dependencies
└── pytest.ini                     # Pytest config + markers
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
```

## Chạy tests

```bash
# Chạy toàn bộ 87 tests
pytest

# Chạy 1 module
pytest tests/test_login.py

# Chạy 1 test cụ thể
pytest tests/test_login.py::TestLogin::test_TC_LOGIN_001_valid_standard_user

# Chạy theo marker
pytest -m login          # 20 login tests
pytest -m e2e            # 2 E2E tests
pytest -m security       # 3 URL security tests

# Chạy với Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

## Chạy có giao diện (không headless)

Sửa `config/config.ini`:
```ini
headless = false
```

## Test cases theo module (87 tổng cộng)

| Module            | Số test | Marker       | Bao gồm |
|-------------------|---------|--------------|---------|
| Login             | 20      | `login`      | 6 loại user, sai credential, empty field, case sensitive, whitespace, SQL injection, XSS, long input, special chars |
| Inventory         | 19      | `inventory`  | 6 sản phẩm, sort 4 kiểu, add/remove cart, detail nav, max cart, sort reset bug |
| Product Detail    | 4       | `product`    | Info display, add/remove, back button |
| Cart              | 7       | `cart`       | Điều hướng, items, remove, checkout, price match |
| Checkout Step 1   | 12      | `checkout`   | Validate 3 field, field robustness (long, special, Unicode emoji, whitespace) |
| Checkout Step 2   | 7       | `checkout`   | Overview, payment/shipping info, tính subtotal + tax = total, finish/cancel |
| Checkout Complete | 4       | `checkout`   | Success msg, Pony image, back home, cart empty |
| Menu              | 5       | `menu`       | Open/close, all items, logout, reset app state |
| Footer            | 4       | `footer`     | Twitter, Facebook, LinkedIn, copyright |
| URL Security      | 3       | `security`   | Truy cập trực tiếp URL khi chưa login |
| E2E               | 2       | `e2e`        | Full purchase 1 sản phẩm + multi-item (3 sản phẩm) |

## Output sau khi chạy

| File/Folder | Nội dung |
|-------------|----------|
| `reports/report.html` | HTML report (pass/fail, thời gian, TC ID, screenshot embedded). Mỗi lần chạy sẽ ghi đè file này. |
| `screenshots/` | Screenshot PNG, tên = `{TC_ID}_{PASS/FAIL}.png`. Xóa và tạo lại mỗi lần chạy full suite. |
| `allure-results/` | Raw data cho Allure report (chỉ có nếu chạy với `--alluredir`) |

## Test case Excel

Toàn bộ 87 test case được export ra file Excel ở [testcases/SauceDemo_TestCases.xlsx](testcases/SauceDemo_TestCases.xlsx):
- **Sheet 1:** Chi tiết từng case (ID, Module, Priority, Type, Title, Precondition, Steps, Test Data, Expected Result, Automatable)
- **Sheet 2:** Summary đếm số case theo module

Nếu muốn sinh lại file Excel (sau khi thêm case mới):
```bash
python testcases/generate_testcases.py
```

## Findings / Bugs phát hiện được

1. **TC_CHK1_009 - Whitespace-only first name**: Site accept khoảng trắng làm first name (đáng lẽ phải reject vì tên không thể chỉ là space).
2. **TC_INV_019 - Sort reset**: Khi vào product detail rồi back về inventory, sort bị reset về default thay vì persist.
3. **Chrome password leak dialog**: Password `secret_sauce` nằm trong list breach của Chrome - modal dialog block automation. Đã fix bằng Chrome options trong conftest.py.

## CI/CD

Mỗi lần push code lên nhánh main, GitHub Actions sẽ tự chạy toàn bộ test headless. File workflow: [.github/workflows/tests.yml](.github/workflows/tests.yml).
