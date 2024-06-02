import textwrap

def mostrar_menu():
    menu = '''
===============MENU===============
    [0]\tDepositar
    [1]\tSacar
    [2]\tExtrato
    [3]\tCriar Usuário
    [4]\tCriar Conta
    [5]\tListar contas
    [6]\tSair

    =>
'''
    return textwrap.dedent(menu)

def deposito(saldo,valor_deposito,extrato,/):
    if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito:\tR$ {valor_deposito:.2f}\n"
            print("\n=== Operação realizada com sucesso! ===")
    else:
        print("\n@@@ Operação falhou. Digite um valor de depósito válida @@@")

    return saldo,extrato

def saque(*,saldo,valor_saque,extrato,limite,numero_saques,limite_saques):
    excedeu_saldo = valor_saque > saldo

    excedeu_limite = valor_saque > limite

    excedeu_tentativas = numero_saques >= limite_saques


    if excedeu_saldo:
        print("@@@ Operação falhou. Você não tem saldo suficiente @@@")
    elif excedeu_limite:
        print("@@@ Operação falhou. O valor do saque execedeu o limite @@@")
    elif excedeu_tentativas:
        print("@@@ Operação falhou. O número máximo de saques foi excedido @@@")
    elif valor_saque > 0:
        saldo -= valor_saque
        extrato += f"Saque:\t\tR$ {valor_saque:.2f}\n"
        numero_saques += 1
        print("\n=== Operação realizada com sucesso! ===")
    else:
        print("\n@@@ Operação falhou. Digite um valor de saque válida @@@")

    return saldo, extrato, numero_saques

def mostrar_extrato(saldo,/,*,extrato) -> None:
    print("\n===============EXTRATO===============")
    print("Não foram realizadas operações") if not extrato else print(extrato)
    print(f"Saldo:\t\tR$ {saldo:.2f}")
    print("======================================")

def criar_user(*,users):
    cpf = input("Insira seu CPF(somente números): ")
    user= filtrar_user(cpf=cpf,users=users)

    if user:
        print("\n@@@ Usuário já cadastrado com esse CPF! @@@")

    nome = input("Insira o seu nome completo: ")
    data_nascimento = input("Insira sua data de nascimento no formato dd/mm/aa: ")
    endereco = input("Insira seu endereço no formato logradouro, nro - bairro - cidade/Estado(sigla): ")

    users.append({"nome":nome,"data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

    return users

def filtrar_user(*,cpf,users):
    users_filtrado = [user for user in users if user["cpf"] == cpf]
    return users_filtrado[0] if users_filtrado else None

def criar_conta(*,agencia,numero_conta,contas,users):
    cpf = input("Insira seu CPF(somente números): ")
    user = filtrar_user(cpf=cpf,users=users)

    if user:
        contas.append({'agencia':agencia,
                       "numero_conta":numero_conta,
                       "user": user})
        numero_conta += 1
        print("=== Conta criado com sucesso! ===")
    else:
        print("\n @@@ Usuário não encontrado, processo de criação de conta encerrado! @@@")
    
    return contas, numero_conta

def listar_contas(*,contas) -> None:
    for conta in contas:
        linha = f"""
            Agência:\t\t{conta['agencia']}
            Número da conta:\t{conta["numero_conta"]}
            Titular da conta:\t{conta["user"]["nome"]}
        """
        print("=" * 50)
        print(linha)
        
def main():
    numero_conta = 1
    NUMERO_AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ""
    LIMITE_SAQUES = 3
    numero_saques = 0
    users = []
    contas = []

    while True:

        opcao = input(mostrar_menu())
        # Depósito
        if opcao == "0":
            valor_deposito = float(input("Digite o valor do depósito: "))

            saldo, extrato = deposito(saldo, 
                                    valor_deposito,
                                    extrato)
        # Sacar
        elif opcao == "1": 
            valor_saque = float(input("Digite o valor do saque: "))

            saldo, extrato, numero_saques = saque(saldo=saldo,
                                    valor_saque=valor_saque,
                                    extrato=extrato, 
                                    limite=limite, 
                                    numero_saques=numero_saques, 
                                    limite_saques=LIMITE_SAQUES)
            
        # Extrato
        elif opcao == "2":
            mostrar_extrato(saldo, 
                    extrato=extrato)

        # Cadastrar user
        elif opcao == "3":
            users = criar_user(users=users)

        # Cadastrar conta
        elif opcao == "4":
            contas, numero_conta = criar_conta(agencia=NUMERO_AGENCIA,
                                 numero_conta=numero_conta,
                                 users=users,
                                 contas=contas)
            
        # Listar contas
        elif opcao == "5":
            listar_contas(contas=contas)
        # Sair
        elif opcao == "6":
            break
        else:
            print("Opção inválida, por favor selecione novamente a opção desejada")

main()