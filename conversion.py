from mpmath import mp
from decimal import Decimal, getcontext
from alphs import ALPH

ALPH_DICT = {name: alph for name, alph in (item.split(":", 1) for item in ALPH)}


def base_convert(alph_from, alph_to, number):
    base_from = len(alph_from)
    base_to = len(alph_to)
    int_part, frac_part = number_split(number)
    
    if alph_from != ALPH_DICT["Decimal (0-9)"]:
        int_value = integer_conversion_to_decimal(alph_from, int_part, base_from)
        if frac_part:
            frac_value = frac_conversion_to_decimal(alph_from, frac_part, base_from)
            decimal_value = mp.mpf(int_value) + frac_value
        else:
            decimal_value = mp.mpf(int_value)
    else:
        decimal_value = number
    
    if alph_to == ALPH_DICT["Decimal (0-9)"]:
        return str(decimal_value)

    int_part, frac_part = number_split(str(decimal_value))

    int_result = integer_conversion_from_decimal(alph_to, int_part, base_to)
    if frac_part:
        precision = len(frac_part)
        frac_result = frac_conversion_from_decimal(alph_to, frac_part, base_to, precision)
        return int_result + frac_result
    else:
        return int_result

def number_split(number):
    if "." in number:
        return number.split(".", 1)
    return number, None

def integer_conversion_from_decimal(alph, int_part, base):
    int_result = ""
    int_part = int(int_part)
    while int_part > base - 1:
        remainder = int_part % base
        int_result += alph[remainder]
        int_part //= base
    int_result += alph[int_part]
    return int_result[::-1]  

def frac_conversion_from_decimal(alph, frac_part, base, precision):
    frac_result = "."
    getcontext().prec = precision + 2 if precision else 15
    frac_value = Decimal("0." + frac_part)
    for _ in range(precision):
        frac_value *= base
        digit = int(frac_value)
        frac_result += alph[digit]
        frac_value -= digit
        if frac_value == 0:
            break
    return frac_result

def integer_conversion_to_decimal(alph, int_part, base):
    int_value = 0
    for i, digit in enumerate(reversed(int_part)):
        int_value += alph.index(digit) * (base ** i)
    return int_value

def frac_conversion_to_decimal(alph, frac_part, base):
    mp.dps = len(frac_part) + 10
    frac_value = mp.mpf(0)
    mp_base = mp.mpf(base)
    for i, digit in enumerate(frac_part):
        frac_value += mp.mpf(alph.index(digit)) * (mp_base ** -(i + 1))
    return frac_value

def irrational(number, alph):
    with open(f"irrational_numbers/{number}.txt", "r") as f:
        decimal = f.read()
    print(f"Converting {number} in {alph} alphabet:")
    result = base_convert("0123456789", alph, decimal)
    with open("irrational_conversion_result.txt", "w") as f:
        f.write(result)
    return result
