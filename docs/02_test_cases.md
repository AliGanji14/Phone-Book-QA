# تست‌کیس‌ها و تقسیم‌بندی Manual / Automated


## ۱. تست‌کیس‌های سمت کلاینت

| شناسه | سناریو | عنوان | نتیجه مورد انتظار | نوع | تست اتومات | نتیجه اجرای آخر |
|---|---|---|---|---|---|---|
| TC-C-01 | CS-01 | ارسال فایل معتبر samples/commands.json | پاسخ سرور چاپ شود و سرور پایدار بماند | Automate | `test_client_sends_valid_file_and_prints_response` | Pass |
| TC-C-02 | CS-02 | فایل JSON ناموجود | پیام «Json file does not exist» بدون کرش | Automate | `test_client_file_not_found` | Pass |
| TC-C-03 | CS-03 | فایل JSON نامعتبر | پیام «Invalid json file» بدون کرش | Automate | `test_client_invalid_json` | Pass |
| TC-C-04 | CS-04 | سرور در دسترس نیست | کلاینت باید با timeout خطا بدهد (باگ ثبت‌شده: BUG-08) | Automate | `test_client_hangs_when_server_unreachable` | Pass (باگ مستند شد) |
| TC-C-05 | CS-05 | اعتبارسنجی قالب ایمیل | ایمیل نامعتبر رد شود | Manual | — | یافته: اعتبارسنجی وجود ندارد (BUG-10) |
| TC-C-06 | CS-06 | هش شدن رمز و salt یکتا در دیتابیس | رمز plaintext ذخیره نشود | Manual | — | تأیید شد (bcrypt + salt) |

## ۲. تست‌کیس‌های سمت سرور

| شناسه | سناریو | عنوان | نتیجه مورد انتظار | نوع | تست اتومات | نتیجه اجرای آخر |
|---|---|---|---|---|---|---|
| TC-S-01 | SS-01 | ثبت‌نام موفق | پیام success در قالب استاندارد | Automate | `test_sign_up_success` | Pass |
| TC-S-02 | SS-01 | ساختار پاسخ {"command_name","result"} | پاسخ دقیقاً دو کلید داشته باشد | Automate | `test_sign_up_result_structure` | Pass |
| TC-S-03 | SS-02 | ورود با رمز درست | پیام success | Automate | `test_sign_in_correct_password` | Pass |
| TC-S-04 | SS-02 | ورود با رمز نادرست | خطای ساختاریافته + پایداری سرور | Automate | `test_sign_in_wrong_password` | **Fail — BUG-01** |
| TC-S-05 | SS-02 | ورود کاربر ناموجود | خطای ساختاریافته + پایداری سرور | Automate | `test_sign_in_nonexistent_user` | **Fail — BUG-01/09** |
| TC-S-06 | SS-01 | ثبت‌نام با نام کاربری تکراری | خطای ساختاریافته + پایداری سرور | Automate | `test_sign_up_duplicate_username` | **Fail — BUG-01** |
| TC-S-07 | SS-03 | خروج پس از ورود | پیام success | Automate | `test_logout_after_sign_in` | Pass |
| TC-S-08 | SS-03 | خروج بدون ورود | عدم کرش (رفتار فعلی: success) | Automate | `test_logout_without_sign_in` | Pass (باگ جزئی BUG-07) |
| TC-S-09 | SS-04 | افزودن مخاطب با توضیحات | پیام success | Automate | `test_add_phone_user_with_explanation` | Pass |
| TC-S-10 | SS-04 | افزودن مخاطب بدون توضیحات | توضیحات اختیاری است؛ پیام success | Automate | `test_add_phone_user_without_explanation` | Pass |
| TC-S-11 | SS-04 | افزودن مخاطب با نام تکراری | خطای ساختاریافته + پایداری سرور | Automate | `test_add_phone_user_duplicate_username` | **Fail — BUG-01** |
| TC-S-12 | SS-05 | دستور دفترچه بدون احراز هویت | رد شدن به دلیل عدم sign_in | Automate | `test_phone_commands_require_authentication` | **Fail — BUG-06** |
| TC-S-13 | SS-04 | پارامتر phone_number ناموجود | خطای اعتبارسنجی ساختاریافته | Automate | `test_add_phone_user_missing_parameter` | **Fail — BUG-01/05** |
| TC-S-14 | SS-06 | افزودن شماره دوم به مخاطب | مخاطب دو شماره داشته باشد | Automate | `test_add_phone_number_to_existing_user` | Pass |
| TC-S-15 | SS-06 | افزودن شماره تکراری | خطای ساختاریافته + پایداری سرور | Automate | `test_add_phone_number_duplicate_number` | **Fail — BUG-01** |
| TC-S-16 | SS-07 | ویرایش فقط نام کاربری | نام عوض شود، شماره ثابت بماند | Automate | `test_edit_phone_user_username_only` | Pass |
| TC-S-17 | SS-07 | ویرایش فقط شماره (null گذاشتن بقیه) | شماره عوض شود | Automate | `test_edit_phone_user_number_only` | Pass |
| TC-S-18 | SS-07 | حذف کلید new_username از payload | طبق صورت مسئله مجاز است؛ بدون کرش | Automate | `test_edit_phone_user_partial_parameters` | **Fail — BUG-04** |
| TC-S-19 | SS-07 | ویرایش مخاطب ناموجود | خطای ساختاریافته + پایداری سرور | Automate | `test_edit_phone_user_nonexistent` | **Fail — BUG-01** |
| TC-S-20 | SS-08 | حذف مخاطب موجود | success و حذف از لیست | Automate | `test_remove_phone_user` | Pass |
| TC-S-21 | SS-08 | حذف مخاطب ناموجود | پیام خطای مناسب، نه success | Automate | `test_remove_phone_user_nonexistent` | **Fail — BUG-02** |
| TC-S-22 | SS-09 | دریافت لیست کامل | هر دو مخاطب در لیست باشند | Automate | `test_get_all_phone_users` | Pass |
| TC-S-23 | SS-10 | جستجوی مخاطب موجود با نام | name + شماره‌ها + explanation | Automate | `test_get_phone_user_by_name_returns_explanation` | **Fail — BUG-03** |
| TC-S-24 | SS-10 | جستجوی نام ناموجود | خطای ساختاریافته + پایداری سرور | Automate | `test_get_phone_user_by_name_nonexistent` | **Fail — BUG-01** |
| TC-S-25 | SS-11 | جستجوی شماره موجود | name + شماره‌ها + explanation | Automate | `test_get_phone_user_by_number` | **Fail — BUG-03** |
| TC-S-26 | SS-11 | جستجوی شماره ناموجود | خطای ساختاریافته + پایداری سرور | Automate | `test_get_phone_user_by_number_nonexistent` | **Fail — BUG-01** |
| TC-S-27 | SS-12 | command_name ناشناخته | خطای ساختاریافته + پایداری سرور | Automate | `test_unknown_command_name` | **Fail — BUG-01/05** |
| TC-S-28 | SS-12 | payload خراب (شیء به‌جای لیست) | خطای ساختاریافته + پایداری سرور | Automate | `test_malformed_payload_object_instead_of_list` | **Fail — BUG-01/05** |
| TC-S-29 | SS-12 | لیست خالی دستورات | پاسخ [] و پایداری سرور | Automate | `test_empty_command_list` | Pass |
| TC-S-30 | SS-13 | پایداری سرور بعد از خطاها | سرور به کار ادامه دهد | Automate | داخل تمام تست‌های negative | **Fail — BUG-01** |
| TC-S-31 | NF-01 | زمان پاسخ کوئری ساده < ۲ ثانیه | موفق | Automate | `test_response_time_simple_query` | Pass |
| TC-S-32 | NF-02 | افزودن ۳۰ مخاطب < ۳ ثانیه | موفق | Automate | `test_bulk_add_30_contacts` | Pass |
| TC-M-01 | — | ماندگاری داده پس از ری‌استارت سرور | داده‌ها در sab.db باقی بمانند | Manual | — | طراحی شده |
| TC-M-02 | — | دو کلاینت همزمان | پاسخ‌ها بدون تداخل و به‌ترتیب | Manual | — | طراحی شده |
