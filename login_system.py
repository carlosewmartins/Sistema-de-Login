#Aluno: Carlos Eduardo Wille Martins

import csv, os

banco_csv = "banco_de_dados.csv"


def create_db():
    if not os.path.exists(banco_csv) or os.stat(banco_csv).st_size == 0:
        with open(banco_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Usuario", "Senha", "Bloqueado"])


def register(username, password):
    with open(banco_csv, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row and row[0] == username:
                print("Usuário já cadastrado!")
                return

    with open(banco_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password, "False"])
        print(f"Usuário {username} cadastrado com sucesso!")


def update_user_status(username, blocked):
    rows = []
    with open(banco_csv, mode="r", newline="") as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    for row in rows:
        if row and row[0] == username:
            row[2] = "True" if blocked else "False"

    with open(banco_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def login():
    username = input("Digite o seu nome de usuário: ").lower()
    users = {}
    with open(banco_csv, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row:
                users[row[0]] = {"password": row[1], "blocked": row[2] == "True"}

    if username not in users:
        print("Usuário não encontrado!")
        return

    if users[username]["blocked"]:
        print("Conta bloqueada! Entre em contato com o suporte.")
        return

    attempts = 5
    while attempts > 0:
        password = input("Digite sua senha: ")
        if users[username]["password"] == password:
            print(f"Seja bem-vindo, {username}!")
            return

        attempts -= 1
        if attempts > 0:
            print(f"Senha incorreta! Você tem {attempts} tentativas restantes.")
        else:
            print("Tentativas esgotadas. Sua conta foi bloqueada.")
            update_user_status(username, True)
            return


def main():
    create_db()
    while True:
        print("\n[1] Login")
        print("[2] Registrar")
        print("[3] Sair")
        try:
            user_choice = int(input("Escolha uma opção: "))
            if user_choice == 1:
                login()
            elif user_choice == 2:
                username = input("Digite o seu nome de usuário: ")
                password = input("Digite sua senha: ")
                register(username.lower(), password)
            elif user_choice == 3:
                print("Saindo...")
                break
            else:
                print("Opção inválida, tente novamente!")
        except ValueError:
            print("Entrada inválida! Digite um número.")


if __name__ == "__main__":
    main()