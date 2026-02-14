from datetime import datetime, timezone
import uuid
import random

def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def new_account_id() -> str:
    return f"ACC_{uuid.uuid4()}" #Zasto ne 1 2 3 nego bas 4 i sto radi uuid4

def new_card_id() -> str:
    return f"CARD_{uuid.uuid4()}"

def iban_to_int_string(string: str) -> str:
    output = []
    for char in string:
        if char.isdigit():
            output.append(char)
        else:
            output.append(str(ord(char.upper()) - 55))
    return "".join(output) #Objasni mi sto je zasto neide nista u navodnike pa join

def mod97(num_str: str) -> int:
    remaider = 0

    for char in num_str:
        remaider = (remaider * 10 + int(char)) % 97
    return remaider

def generate_iban() -> str:
    bban = "".join(str(random.randint(0, 9)) for _ in range(17)) #sto oznacava _ u for petlji
    country = "HR"
    check = "00"
    rearranged = f"{bban}{country}{check}"
    numeric = iban_to_int_string(rearranged)
    mod = mod97(numeric)#koji je output moda
    check_digits = 98 - mod
    return f"HR{check_digits:02d}{bban}"

def luhn_checksum_digits(number: str) -> str:
    total = 0
    reverse_digits = list(map(int, reversed(number)))
    for i, digit_value in enumerate(reverse_digits):
        if i % 2 == 0:
            digit_value *= 2
            if digit_value > 9:
                digit_value -= 9
        total += digit_value
    check = (10 - (total % 10)) % 10
    return str(check)

def generate_pan(brand: str = "VISA") -> str:
    if brand.upper() == "VISA":
        prefix = "4"
    else:
        prefix = "5"
    
    body_len = 15 - len(prefix)
    body = "".join(str(random.randint(0, 9)) for _ in range(body_len))
    first15 = prefix + body
    return first15 + luhn_checksum_digits(first15)

def mask_pan(pan: str) -> str:
    last4 = pan[-4:]
    return f"**** **** **** {last4}", last4