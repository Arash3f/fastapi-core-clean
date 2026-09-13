from enum import Enum


class ErrorCode(int, Enum):
    UN_EXPECTED_ID = 1
    INVALID_PAGE_SIZE = 2
    INVALID_PAGE = 3

    # Auth
    INVALID_CREDENTIALS = 900
    INACTIVE_USER = 901
    INVALID_REFRESH_TOKEN = 902
    DEVICE_MISMATCH = 903
    USER_NOT_AUTHORIZED = 904
    INCORRECT_CURRENT_PASSWORD = 905

    # User
    USER_NOT_FOUND = 1400
    USERNAME_DUPLICATED = 1401
    FORBIDDEN = 1402


ERROR_MESSAGES = {
    "en": {
        ErrorCode.UN_EXPECTED_ID: "Unexpected ID provided",
        ErrorCode.INVALID_PAGE_SIZE: "Invalid page size",
        ErrorCode.INVALID_PAGE: "Invalid page",
        ErrorCode.INVALID_CREDENTIALS: "Incorrect username or password",
        ErrorCode.INACTIVE_USER: "User account is inactive",
        ErrorCode.INVALID_REFRESH_TOKEN: "Invalid refresh token",
        ErrorCode.DEVICE_MISMATCH: "Device fingerprint mismatch",
        ErrorCode.USER_NOT_AUTHORIZED: "User is not authorized",
        ErrorCode.INCORRECT_CURRENT_PASSWORD: "Current password is incorrect",
        ErrorCode.USER_NOT_FOUND: "User not found",
        ErrorCode.USERNAME_DUPLICATED: "Username is already taken",
        ErrorCode.FORBIDDEN: "You do not have permission to perform this action",
    },
    "fa": {
        ErrorCode.UN_EXPECTED_ID: "شناسه غیرمنتظره",
        ErrorCode.INVALID_PAGE_SIZE: "اندازه صفحه نامعتبر است",
        ErrorCode.INVALID_PAGE: "شماره صفحه اشتباه است",
        ErrorCode.INVALID_CREDENTIALS: "نام کاربری یا رمز عبور نادرست است",
        ErrorCode.INACTIVE_USER: "حساب کاربری غیرفعال است",
        ErrorCode.INVALID_REFRESH_TOKEN: "توکن تازه‌سازی نامعتبر است",
        ErrorCode.DEVICE_MISMATCH: "اثرانگشت دستگاه مطابقت ندارد",
        ErrorCode.USER_NOT_AUTHORIZED: "کاربر مجاز نیست",
        ErrorCode.INCORRECT_CURRENT_PASSWORD: "رمز عبور فعلی نادرست است",
        ErrorCode.USER_NOT_FOUND: "کاربر پیدا نشد",
        ErrorCode.USERNAME_DUPLICATED: "نام کاربری تکراری است",
        ErrorCode.FORBIDDEN: "مجوز انجام این عملیات را ندارید",
    },
}
