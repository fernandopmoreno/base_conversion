from mpmath import mp

def digits_generator(number, n_digits):
    mp.dps = n_digits + 5

    if number == "pi":
        frac = mp.pi - 3
    elif number == "e":
        frac = mp.e - 2
    elif number == "phi":
        frac = mp.phi - 1
    elif number == "sqrt2":
        frac = mp.sqrt(2) - 1
    else:
        print("Número no permitido")
        return

    for _ in range(n_digits):
        frac *= 10
        digit = mp.floor(frac)
        yield str(int(digit))
        frac -= digit

def save_digits(number, filename, n_digits):
    print(f"Generando {n_digits} dígitos de {number} y guardándolos en {filename}...")

    with open(filename, "w") as f:
        if number == "pi":
            f.write("3.")
        elif number == "e":
            f.write("2.")
        elif number in ["phi", "sqrt2"]:
            f.write("1.")
        else:
            print("Número no permitido")
            return

        for digit in digits_generator(number, n_digits):
            f.write(digit)
    print("¡Proceso completado!")

if __name__ == "__main__":
    save_digits("pi", "irrational_numbers/pi.txt", 1000000)
    save_digits("e", "irrational_numbers/e.txt", 1000000)
    save_digits("phi", "irrational_numbers/phi.txt", 1000000)
    save_digits("sqrt2", "irrational_numbers/sqrt(2).txt", 1000000)
