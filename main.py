import textwrap
from abc import ABC,abstractmethod
import datetime

class Cliente():
    def __init__(self, endereco) -> None:
        self.endereco:str = endereco
        self.contas = []
    
    def realizar_transacoes(self,conta,transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,cpf,nome,data_nascimento,endereco) -> None:
        super().__init__(endereco)
        self.cpf:str = cpf
        self.nome:str = nome
        self.data_nascimento:str = data_nascimento

class Conta():
    def __init__(self,cliente,numero) -> None:
        self._saldo:float = 0
        self._numero = numero
        self._agencia:str = "0001"
        self._cliente:Cliente = cliente
        self._historico:Historico = Historico()
    
    @classmethod    
    def nova_conta(cls,cliente,numero):
        return cls(cliente,numero)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor:float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("@@@ Operação falhou. Você não tem saldo suficiente @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Operação realizada com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou. Digite um valor de saque válida @@@")
            
        return False
        
    def depositar(self,valor:float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            print("\n@@@ Operação falhou. Digite um valor de depósito válida @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self,cliente,numero,limite=500,limite_saques=3) -> None:
        super().__init__(cliente,numero)
        self._limite:float  = limite
        self._limite_saques:int = limite_saques
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self,valor):
        saldo = self._saldo
        limite = self.limite
        limite_saques = self.limite_saques

        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if 
            transacoes["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > limite

        excedeu_tentativas = numero_saques >= limite_saques

        if excedeu_limite:
            print("@@@ Operação falhou. O valor do saque execedeu o limite @@@")
        elif excedeu_tentativas:
            print("@@@ Operação falhou. O número máximo de saques foi excedido @@@")
        else:
            super().sacar(valor)

        return False
    
    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}\n
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico():
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self) -> None:
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data" : datetime.now.strftime
                ("%d-%m-%Y %H:%M:%s")
            }
        )

class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self):
        pass

class Deposito(Transacao):
    def __init__(self,valor) -> None:
        self._valor:float = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar()

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self,valor) -> None:
        self._valor:float = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar()

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

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