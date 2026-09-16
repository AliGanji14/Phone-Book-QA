# گزارش اجرای تست (آخرین اجرا) — Test Execution Report

**مستند:** گزارش اجرای تست و گزارش باگ 
**تاریخ اجرا:** 2026-09-16
**نتیجه کلی:** ۳۵ تست اجرا شد — **۱۹ Pass / ۱۶ Fail** — مدت اجرا: 27.46s

## ۱. محیط اجرا

| مورد | مقدار |
|---|---|
| سیستم‌عامل | Windows 10 (build 26200) |
| Python | 3.14.5 (venv پروژه) |
| pytest | 9.1.1 |
| pyzmq | 27.2.0 |
| peewee / bcrypt | طبق requirements.txt |
| نحوه اجرا | `venv\Scripts\python.exe -m pytest tests -v` |

## ۲. خلاصه نتایج

| حوزه | تعداد | Pass | Fail |
|---|---|---|---|
| کلاینت (`tests/test_client.py`) | ۴ | ۴ | ۰ |
| غیرعملکردی (`tests/test_nonfunctional.py`) | ۲ | ۲ | ۰ |
| عملکردی سرور (`tests/test_server_functional.py`) | ۱۶ | ۱۲ | ۴ |
| منفی سرور (`tests/test_server_negative.py`) | ۱۳ | ۱ | ۱۲ |
| **جمع** | **۳۵** | **۱۹** | **۱۶** |

نکته: تمام ۱۶ خطا به ۷ ریشه باگ برمی‌گردد که در `docs/04_bug_report.md` شرح داده شده است (برخی باگ‌ها چند تست را خراب می‌کنند).

## ۳. نتایج تفصیلی

| تست | نتیجه | باگ مرتبط |
|---|---|---|
| test_client_file_not_found | Pass | — |
| test_client_invalid_json | Pass | — |
| test_client_sends_valid_file_and_prints_response | Pass | — |
| test_client_hangs_when_server_unreachable | Pass (رفتار معیوب مستند شد) | BUG-08 |
| test_response_time_simple_query | Pass | — |
| test_bulk_add_30_contacts | Pass | — |
| test_sign_up_success | Pass | — |
| test_sign_up_result_structure | Pass | — |
| test_sign_in_correct_password | Pass | — |
| test_logout_after_sign_in | Pass | — |
| test_logout_without_sign_in | Pass | BUG-07 (جزئی) |
| test_add_phone_user_with_explanation | Pass | — |
| test_add_phone_user_without_explanation | Pass | — |
| test_add_phone_number_to_existing_user | Pass | — |
| test_get_all_phone_users | Pass | — |
| test_get_phone_user_by_name_returns_explanation | **Fail** | BUG-03 |
| test_get_phone_user_by_number | **Fail** | BUG-03 |
| test_edit_phone_user_username_only | Pass | — |
| test_edit_phone_user_number_only | Pass | — |
| test_remove_phone_user | Pass | — |
| test_remove_phone_user_nonexistent | **Fail** | BUG-02 |
| test_phone_commands_require_authentication | **Fail** | BUG-06 |
| test_sign_in_wrong_password | **Fail** | BUG-01 |
| test_sign_in_nonexistent_user | **Fail** | BUG-01, BUG-09 |
| test_sign_up_duplicate_username | **Fail** | BUG-01 |
| test_add_phone_user_duplicate_username | **Fail** | BUG-01 |
| test_add_phone_number_duplicate_number | **Fail** | BUG-01 |
| test_get_phone_user_by_name_nonexistent | **Fail** | BUG-01 |
| test_get_phone_user_by_number_nonexistent | **Fail** | BUG-01 |
| test_edit_phone_user_nonexistent | **Fail** | BUG-01 |
| test_edit_phone_user_partial_parameters | **Fail** | BUG-04 |
| test_add_phone_user_missing_parameter | **Fail** | BUG-01, BUG-05 |
| test_unknown_command_name | **Fail** | BUG-01, BUG-05 |
| test_malformed_payload_object_instead_of_list | **Fail** | BUG-01, BUG-05 |
| test_empty_command_list | Pass | — |

## ۴. شواهد کلیدی

- بعد از ارسال رمز نادرست، سرور متن خام `password is wrong` (خارج از قالب استاندارد پاسخ) برمی‌گرداند و سپس **فرآیند سرور کامل قطع می‌شود** (بررسی شد: `process alive = False` و درخواست بعدی حتی ارسال هم نمی‌شود). این رفتار در ۹ سناریوی خطا تکرار می‌شود → BUG-01.
- حذف مخاطب ناموجود پیام `phone user ghost_xxx removed successfully` برمی‌گرداند → BUG-02.
- جواب جستجو فقط `{'name': ..., 'phone_numbers': [...]}` است و `explanation` ندارد → BUG-03.

## ۵. نتیجه‌گیری

- جریان‌های اصلی (ثبت‌نام، ورود موفق، افزودن/ویرایش/حذف مخاطب، جستجو، لیست کامل) در مسیر خوش‌خواسته (happy path) درست کار می‌کنند و عملکرد (زمان پاسخ) مناسب است.
- ضعف اصلی سیستم، نبود مدیریت خطا و اعتبارسنجی ورودی در سرور است: هر استثنای پیش‌بینی‌نشده کل سرور را از کار می‌اندازد (نیاز فوری به اصلاح BUG-01).
- تست‌های غیرعملکردی اختیاری (زمان پاسخ و بارگذاری حجمی) طبق مجوز فایل ارزیابی اضافه و با موفقیت اجرا شدند.
