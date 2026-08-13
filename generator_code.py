import random
import string

def generate_password(length, chars):
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
def choise_complexity():
    print("Выбирете сложность:")
    print("1. Лёкгий")
    print("2. Средний")
    print("3. Сложный")
    a = input(">")
    if a == "1":
        chars = string.ascii_letters
        return chars
    elif a == "2":
        chars = string.ascii_letters + string.digits
        return chars
    elif a == "3":
        chars = string.ascii_letters + string.digits + string.punctuation
        return chars
    else:
        print("Вы ввели неверную команду!")
        return None
    
def main_loop():
        while True:
            print("\nГенератор паролей")
            chars = choise_complexity()
            if chars is None:
                continue
            try:
                length = int(input("Выберите длину: "))
            except ValueError:
                print("Введите число!")
                continue
            password = generate_password(length, chars)
            print(f"Ваш пароль: {password}")
            break
main_loop()
