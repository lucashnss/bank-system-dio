def deposito(saldo, valor_deposito, extrato,/):
    if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
    else:
        print("Operação falhou. Digite um valor de depósito válida")

    return saldo,extrato

def saque(*,saldo,valor_saque, extrato, limite, numero_saques,limite_saques):
    excedeu_saldo = valor_saque > saldo

    excedeu_limite = valor_saque > limite

    excedeu_tentativas = numero_saques >= limite_saques


    if excedeu_saldo:
        print("Operação falhou. Você não tem saldo suficiente")
    elif excedeu_limite:
        print("Operação falhou. O valor do saque execedeu o limite")
    elif excedeu_tentativas:
        print("Operação falhou. O número máximo de saques foi excedido")
    else:
        saldo -= valor_saque
        extrato += f"Saque: R$ {valor_saque:.2f}\n"
        numero_saques += 1

    return saldo, extrato, numero_saques

def mostrar_extrato(saldo,/,*,extrato) -> None:
    print("\n===============EXTRATO===============")
    print("Não foram realizadas operações") if not extrato else print(extrato)
    print(f"Saldo: {saldo:.2f}")
    print("======================================")
    
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
    # Sair
    elif opcao == "3":
        break
    else:
        print("Opção inválida, por favor selecione novamente a opção desejada")