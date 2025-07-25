from mpmath import mp

def base_selection():
    ALPH = {
        1: "01",
        2: "01234567",
        3: "0123456789",
        4: "0123456789ABCDEF",
        5: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        6: "ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        7: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        8: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        9: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        10: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
    }

    print("\nBienvenido, en esta aplicación podrá expresar cualquier número en la base deseada.")
    while True:
        print("\nIntroduzca el número de la base:\n")
        print("1. Binario (base 2)")
        print("2. Octal (base 8)")
        print("3. Decimal (base 10)")
        print("4. Hexadecimal (base 16)")
        print("5. Base 26 (A-Z)")
        print("6. Base 27 (A-Z, espacio)")
        print("7. Base 36 (0-9, A-Z)")
        print("8. Base 37 (0-9, A-Z, espacio)")
        print("9. Base 62 (0-9, A-Z, a-z)")
        print("10. Base 63 (0-9, A-Z, a-z, espacio)")
        print("11. Personalizada (introduzca el alfabeto deseado)")
        print("12. Salir")

        selected_alph = input("\nOpción: ")
        try:
            selected_alph = int(selected_alph)
            if selected_alph == 12:
                break
            if selected_alph == 11:
                alph = input("Alfabeto: ")
            else:
                alph = ALPH[selected_alph]
            menu(alph)
        except ValueError:
            print("Opción no válida. Por favor, elija un número entre 1 y 12.")

def menu(alph):    
    menu_options = {
        "1": lambda: input_number(alph),
        "2": lambda: irrational("pi", alph),
        "3": lambda: irrational("e", alph),
        "4": lambda: irrational("sqrt(2)", alph),
        "5": lambda: irrational("phi", alph)
    }

    while True:
        print("\nIntroduzca el número de la opción deseada:\n")
        print("1. Introducir un número manualmente (formato: XX.XX)")
        print("2. Transformar Pi")
        print("3. Transformar e")
        print("4. Transformar raíz de 2")
        print("5. Transformar proporción áurea (1+sqrt(5))/2")
        print("6. Volver a la selección de base")
        selected = input("\nOpción: ")
        if selected == "6":
            break
        try:
            menu_options[selected]()
        except KeyError as e:
            print("Opción no válida.")
            print(e)

def input_number(alph):
    number = input("Introduzca el número a transformar: ")
    if "." in number:
        precision = int(input("Introduzca la precisión máxima deseada (número de dígitos decimales): "))
        if precision:
            result = decimal_to_alph(alph, number, precision)
    else:
        result = decimal_to_alph(alph, number)
    print(result)

def irrational(number, alph):
    with open(f"irrational_numbers/{number}.txt", "r") as f:
        decimal = f.read()
    result = decimal_to_alph(alph, decimal, precision=len(decimal.split(".")[1]) if "." in decimal else 10)
    print(result)

def decimal_to_alph(alph, decimal, precision=10):
    base = len(alph)
    try:
        int_part, frac_part = decimal.split(".")
    except:
        int_part, frac_part = decimal, None
    int_part = int(int_part)

    int_result = integer_conversion(alph, int_part, base)

    if frac_part:
        frac_result = frac_conversion(alph, frac_part, base, precision)
        return int_result + frac_result
    else:
        return int_result

def integer_conversion(alph, int_part, base):
    int_result = ""
    while int_part > base - 1:
        remainder = int_part % base
        int_result += alph[remainder]
        int_part //= base
    int_result += alph[int_part]
    return int_result[::-1]

def frac_conversion(alph, frac_part, base, precision):
    frac_result = "."
    mp.dps = len(frac_part) + 5
    frac_value = mp.mpf("0." + frac_part)
    for _ in range(precision):
        frac_value *= base
        digit = int(frac_value)
        frac_result += alph[digit]
        frac_value -= digit
    return frac_result

def alph_to_decimal(alph, number):
    base = len(alph)
    try:
        int_part, frac_part = number.split(".")
    except ValueError:
        int_part, frac_part = number, None

    int_value = 0
    for i, digit in enumerate(reversed(int_part)):
        int_value += alph.index(digit) * (base ** i)
    
    if frac_part:
        mp.dps = len(frac_part) + 10
        frac_value = mp.mpf(0)
        mp_base = mp.mpf(base)
        for i, digit in enumerate(frac_part):
            frac_value += mp.mpf(alph.index(digit)) * (mp_base ** -(i + 1))
        return mp.mpf(int_value) + frac_value
    else:
        return mp.mpf(int_value)


if __name__ == "__main__":
    base_selection()