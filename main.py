import textwrap
from abc import ABC,abstractmethod
from datetime import datetime

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
    
    def sacar(self,valor:float):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("@@@ Operação falhou. Você não tem saldo suficiente @@@")
            return False
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
        self._numero_saques:int = 0
    
    
    def sacar(self,valor):
        excedeu_saldo = valor > self._saldo

        excedeu_limite = valor > self._limite

        excedeu_tentativas = self._numero_saques >= self._limite_saques

        if excedeu_limite:
            print("@@@ Operação falhou. O valor do saque execedeu o limite @@@")
            return False
        elif excedeu_saldo:
            print("@@@ Operação falhou. Você não tem saldo suficiente @@@")
            return False
        elif excedeu_tentativas:
            print("@@@ Operação falhou. O número máximo de saques foi excedido @@@")
            return False
        elif valor > 0:
            self._saldo -= valor
            self._numero_saques += 1
            print("\n=== Operação realizada com sucesso! ===")
            return True
        else:
            super().sacar(valor)
    
    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
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
                "data" : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
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
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self,valor) -> None:
        self._valor:float = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def mostrar_menu():
    menu = '''
===========================MENU============================
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

def filtrar_clientes(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ O cliente não possui conta @@@")
        return
    # FIXME: Não permite o cliente escolher a conta
    return cliente.contas[0]

def transacao(clientes, tipo_transacao):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input(f"Digite o valor do {tipo_transacao}: "))

    if tipo_transacao == "depósito":
        funcao_transacao = Deposito(valor)
    else:
        funcao_transacao = Saque(valor)

    transacao = funcao_transacao

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    cliente.realizar_transacoes(conta,transacao)

def exibir_extrato(clientes) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    extrato = ""
    print("\n==========================EXTRATO==========================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            if transacao["tipo"] == "Deposito":
                extrato += f"\n{transacao['tipo']}:\tR${transacao['valor']:.2f}\t Data:\t{transacao['data']}"
            else:
                extrato += f"\n{transacao['tipo']}:\t\tR${transacao['valor']:.2f}\t Data:\t{transacao['data']}"
        
        print(extrato)
        print(f"\nSaldo:\tR${conta.saldo:.2f}")
        print("===========================================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if cliente:
        print("\n@@@ Cliente já existe com esse CPF! @@@")
        return
    
    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logadrouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf,nome,data_nascimento,endereco)
    clientes.append(cliente
                    )
    print("\n=== Cliente cadastrado com sucesso! ===")
    return clientes

def criar_conta(numero_conta,clientes,contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, processo de criação de contas encerrado! @@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente,numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

    return contas

def listar_contas(contas) -> None:
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))
        
def main():
    clientes = []
    contas = []

    while True:

        opcao = input(mostrar_menu())
        # Depósito
        if opcao == "0":
            transacao(clientes,"depósito")
        # Sacar
        elif opcao == "1": 
            transacao(clientes,"saque")
        # Extrato
        elif opcao == "2":
            exibir_extrato(clientes)
        # Cadastrar cliente
        elif opcao == "3":
            clientes_novos = criar_cliente(clientes)
            if clientes_novos:
                clientes = clientes_novos
        # Cadastrar conta
        elif opcao == "4":
            numero_conta = len(contas) + 1
            contas_novas = criar_conta(numero_conta,clientes,contas) 
            if contas_novas:
                contas = contas_novas
        # Listar contas
        elif opcao == "5":
            listar_contas(contas)
        # Sair
        elif opcao == "6":
            break
        else:
            print("Opção inválida, por favor selecione novamente a opção desejada")

main()