import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
                Agência:\t{conta.agencia}
                Número:\t\t{conta.numero}
                Titular:\t{conta.cliente.nome}
                Saldo:\t\tR${conta.saldo}
            """

        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco: str = endereco
        self.contas = []

    def realizar_transacoes(self, conta, transacao):
        if len(conta.historico.transacoes_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco) -> None:
        super().__init__(endereco)
        self.cpf: str = cpf
        self.nome: str = nome
        self.data_nascimento: str = data_nascimento

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ({self.cpf})>"


class Conta:
    def __init__(self, cliente, numero) -> None:
        self._saldo: float = 0
        self._numero = numero
        self._agencia: str = "0001"
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

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

    def sacar(self, valor: float):
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

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            print("\n@@@ Operação falhou. Digite um valor de depósito válida @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3) -> None:
        super().__init__(cliente, numero)
        self._limite: float = limite
        self._limite_saques: int = limite_saques
        self._numero_saques: int = 0

    def sacar(self, valor):
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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.agencia}','{self.numero}','{self.cliente.nome}')>"

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t{self.saldo}
        """


class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self) -> None:
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_dia(self):
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self):
        pass


class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open("logs/log.txt", "a") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__.upper()}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n"
            )

        return resultado

    return wrapper


def mostrar_menu():
    menu = """
===========================MENU============================
    [0]\tDepositar
    [1]\tSacar
    [2]\tExtrato
    [3]\tCriar Usuário
    [4]\tCriar Conta
    [5]\tListar contas
    [6]\tSair

    =>
"""
    return textwrap.dedent(menu)


def mostrar_menu_extrato():
    menu = """
===========================MENU============================
    [0]\tApenas Depósitos
    [1]\tApenas Saques
    [2]\tExtrato Completo
    [3]\tVoltar ao menu principal
    =>
"""
    return textwrap.dedent(menu)


def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ O cliente não possui conta @@@")
        return
    # FIXME: Não permite o cliente escolher a conta
    return cliente.contas[0]


@log_transacao
def transacao(clientes, tipo_transacao, valor):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if tipo_transacao == "depósito":
        funcao_transacao = Deposito(valor)
    else:
        funcao_transacao = Saque(valor)

    transacao = funcao_transacao

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    cliente.realizar_transacoes(conta, transacao)


@log_transacao
def exibir_extrato(clientes, tipo_extrato=None) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    print("\n==========================EXTRATO==========================")
    extrato = ""
    transacoes = conta.historico.gerar_relatorio(tipo_extrato)
    tem_transacao = False

    for transacao in transacoes:
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("===========================================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("\n@@@ Cliente já existe com esse CPF! @@@")
        return

    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira sua data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe seu endereço (logadrouro, nro - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)
    print("\n=== Cliente cadastrado com sucesso! ===")
    return clientes


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print(
            "\n@@@ Cliente não encontrado, processo de criação de contas encerrado! @@@"
        )
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

    return contas


def listar_contas(contas) -> None:
    for conta in ContasIterador(contas):
        print("=" * 50)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:

        opcao = input(mostrar_menu())
        # Depósito
        if opcao == "0":
            valor = float(input(f"Digite o valor do Depósito: "))
            transacao(clientes, "depósito", valor)
        # Sacar
        elif opcao == "1":
            valor = float(input(f"Digite o valor do Saque: "))
            transacao(clientes, "saque", valor)
        # Extrato
        elif opcao == "2":
            tipo_extrato = input(mostrar_menu_extrato())
            if tipo_extrato == "0":
                exibir_extrato(clientes, "Deposito")
            elif tipo_extrato == "1":
                exibir_extrato(clientes, "Saque")
            elif tipo_extrato == "2":
                exibir_extrato(clientes)
            elif tipo_extrato == "3":
                main()
            else:
                print("Opção inválida, por favor selecione novamente a opção desejada")

        # Cadastrar cliente
        elif opcao == "3":
            clientes_novos = criar_cliente(clientes)
            if clientes_novos:
                clientes = clientes_novos
        # Cadastrar conta
        elif opcao == "4":
            numero_conta = len(contas) + 1
            contas_novas = criar_conta(numero_conta, clientes, contas)
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
