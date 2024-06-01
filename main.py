menu = '''
    [0] : Depositar
    [1] : Sacar
    [2] : Extrato
    [3] : Sair

    =>
'''

saldo = 0
limite = 500
extrato = ""
LIMITE_SAQUES = 3
numero_saques = 0

while True:

    opcao = input(menu) 
    saques_realizados = 0
    # Depósito
    if opcao == "0":
        deposito = float(input("Digite o valor do depósito: "))

        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
        else:
            print("Operação falhou. Digite um valor de depósito válida")

    # Sacar
    elif opcao == "1":
        saque = float(input("Digite o valor do saque: "))

        excedeu_saldo = saque > saldo

        excedeu_limite = saque > limite

        excedeu_tentativas = numero_saques >= LIMITE_SAQUES


        if excedeu_saldo:
            print("Operação falhou. Você não tem saldo suficiente")
        elif excedeu_limite:
            print("Operação falhou. O valor do saque execedeu o limite")
        elif excedeu_tentativas:
            print("Operação falhou. O número máximo de saques foi excedido")
        else:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saques += 1


    # Extrato
    elif opcao == "2":
        print("\n===============EXTRATO===============")
        print("Não foram realizadas operações") if not extrato else print(extrato)
        print(f"Saldo: {saldo:.2f}")
        print("======================================")
    # Sair
    elif opcao == "3":
        break
    else:
        print("Opção inválida, por favor selecione novamente a opção desejada")