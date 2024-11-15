from datetime import datetime

def get_first_to_letter_upper(str):
    letter = str[0:2]
    upper_letter = letter.upper()
    return upper_letter

def generate_signup_coupon(first_name, last_name):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    coupon_code = f'{get_first_to_letter_upper(first_name)}{get_first_to_letter_upper(last_name)}{hour}{minute}'
    return coupon_code