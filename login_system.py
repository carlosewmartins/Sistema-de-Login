# Aluno: Carlos Eduardo Wille Martins

import csv
import os

banco_csv = "banco_de_dados.csv"
permission_csv = "permissoes.csv"


def create_db():
    """Cria o banco de usuários se não existir."""
    if not os.path.exists(banco_csv) or os.stat(banco_csv).st_size == 0:
        with open(banco_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Usuario", "Senha", "Bloqueado"])


def create_permission():
    """Cria o arquivo de permissões se não existir."""
    if not os.path.exists(permission_csv) or os.stat(permission_csv).st_size == 0:
        with open(permission_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Usuario", "Permissoes"])


def register(username, password):
    """Registra um novo usuário no banco de dados."""
    with open(banco_csv, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)  # Pula o cabeçalho
        for row in reader:
            if row and row[0] == username:
                print("Usuário já cadastrado!")
                return

    with open(banco_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password, "False"])

    with open(permission_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, ""])  # Sem permissões inicialmente

    print(f"Usuário {username} cadastrado com sucesso!")


def update_user_status(username, blocked):
    """Atualiza o status de bloqueio de um usuário."""
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
    """Autentica um usuário."""
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
        return None

    if users[username]["blocked"]:
        print("Conta bloqueada! Entre em contato com o suporte.")
        return None

    attempts = 5
    while attempts > 0:
        password = input("Digite sua senha: ")
        if users[username]["password"] == password:
            print(f"Seja bem-vindo, {username}!")
            return username  # Retorna o nome do usuário autenticado

        attempts -= 1
        if attempts > 0:
            print(f"Senha incorreta! Você tem {attempts} tentativas restantes.")
        else:
            print("Tentativas esgotadas. Sua conta foi bloqueada.")
            update_user_status(username, True)
            return None


def add_permission(username, new_permissions):
    """Adiciona permissões ao usuário no arquivo de permissões."""
    rows = []
    found = False

    # Lendo o arquivo de permissões
    with open(permission_csv, mode="r", newline="") as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    # Atualizando permissões do usuário
    for row in rows:
        if row and row[0] == username:
            existing_permissions = set(row[1].split(";")) if row[1] else set()
            new_permissions = set(new_permissions)
            updated_permissions = existing_permissions.union(new_permissions)  # Une permissões antigas e novas
            row[1] = ";".join(updated_permissions)  # Salva em formato "ler;escrever;apagar"
            found = True
            break

    # Caso o usuário não esteja na lista, adiciona ele
    if not found:
        rows.append([username, ";".join(new_permissions)])

    # Escrevendo de volta no arquivo
    with open(permission_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Permissões {new_permissions} adicionadas ao usuário {username}.")


def check_permission(username):
    """Verifica as permissões de um usuário."""
    with open(permission_csv, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row and row[0] == username:
                return row[1].split(";") if row[1] else []
    return []


def access_resource(username):
    """Simula o acesso a um recurso fictício baseado nas permissões do usuário."""
    permissions = check_permission(username)

    if not permissions:
        print("Você não tem permissão para acessar nenhum recurso.")
        return

    print(f"Suas permissões: {permissions}")
    action = input("Digite a ação desejada (ler, escrever, apagar): ").lower()

    if action in permissions:
        print("Acesso permitido.")
    else:
        print("Acesso negado.")


def main():
    create_db()
    create_permission()

    while True:
        print("\n[1] Login")
        print("[2] Registrar")
        print("[3] Sair")
        try:
            user_choice = int(input("Escolha uma opção: "))
            if user_choice == 1:
                user = login()
                if user:
                    while True:
                        print("\n[1] Acessar recurso")
                        print("[2] Conceder permissões (apenas admin)")
                        print("[3] Logout")

                        option = int(input("Escolha uma opção: "))

                        if option == 1:
                            access_resource(user)
                        elif option == 2 and user == "admin":
                            target_user = input("Digite o nome do usuário para conceder permissões: ")
                            new_perms = input(
                                "Digite as permissões (separadas por ponto e vírgula - ex: ler;escrever): ").split(";")
                            add_permission(target_user, new_perms)
                        elif option == 3:
                            print("Deslogando...")
                            break
                        else:
                            print("Opção inválida.")
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
