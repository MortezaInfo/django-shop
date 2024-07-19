from . import jalali
from django.utils import timezone



def send_otp_code(phone, code):
    ...


def conver_number(str):
    number = {"0": "0"}
    for e,p in number.items():
        str = str.replace(e,p)


def jalali(time):
    jmonth = ["فرودین", "اردیبهشت", "خرداد", ...]
    time_to_str = f"{time.year}, {time.month}, {time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(time_to_list):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    output = f"{time_to_list[2]} {time_to_list[1]} {time_to_list[0]} ساعت {time.hour}:{time.minute}"
    return conver_number(output)


# برای مبدل عدد میتونی ی تابع تعریف کنی و عدد های انگلیسی و فارسی رو گی ولیو ذخیره کنی
