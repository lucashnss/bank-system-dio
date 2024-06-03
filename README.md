## Desafio de Sistema Bancário na DIO
O Desafio tem como objetivo a aplicação de conhecimentos sobre estruturas mais básicas de Python, funções e orientação a objetos na trilha de Python AI Backend Developer da DIO.
Foi implementado um sistema bancário simples com a linguagem Python.
Nele é possível tomar as seguintes ações:
- Depósitos
- Saques
- Conferência de extratos
- Criação de usuários
- Criação de contas
- Listar contas

##

## Detalhes do Desafio
Fomos contratados por um grande banco para desenvolver o
seu novo sistema. Esse banco deseja modernizar suas
operações e para isso escolheu a linguagem Python. Para a
primeira versão do sistema devemos implementar apenas 3
operações: depósito, saque e extrato.

## Operação de depósito
Deve ser possível depositar valores positivos para a minha
conta bancária. Todos os depósitos devem ser armazenados e exibidos na
operação de extrato.

## Operação de saque
O sistema deve permitir realizar 3 saques diários com limite
máximo de R$ 500,00 por saque. Caso o usuário não tenha
saldo em conta, o sistema deve exibir uma mensagem
informando que não será possível sacar o dinheiro por falta de
saldo. Todos os saques devem ser armazenados e exibidos na operação de extrato.

## Operação de extrato
Essa operação deve listar todos os depósitos e saques
realizados na conta. No fim da listagem deve ser exibido o
saldo atual da conta. Se o extrato estiver em branco, exibir a
mensagem: Não foram realizadas movimentações.
Os valores devem ser exibidos utilizando o formato R$ xxx.xx,
exemplo:
1500.45 = R$ 1500.45

## Criar Cliente
O programa deve armazenar os usuários em uma lista, os quais são compostos 
por: nome, data de nascimento, cpf e endereço. O endereço é uma string
no formato logradouro, nro - bairro - cidade/Estado. Deve ser armazenado somente
os números do CPF. Não podemos cadastrar 
 usuários com o mesmo CPF.

## Criar conta corrente
O programa deve armazenar contas em uma lista, conta é composta por: agência,
número da conta e usuário. O número da conta é sequencial, e inicia-se por 1.
A agência é fixa: "0001". O usuário pode ter mais de uma conta, mas uma conta 
pertence somente a um usuário.

## Remodelação com conceitos de funções e POO
O projeto evolui de conceitos básicos, para uso de funções e posteriormente noções
de POO, o que ajuda na organização, mantenabilidade, legibilidade e permite
uma evolução maior do sistema. O projeto na versão POO segue o padrão do seguinte
diagrama UML:

![Diagrama UML - Desafio](Trilha-Python-desafio.png)


## Desafio com POO 
Fazer a modelagem das funções referentes a saques, depósitos, extrato, criação de 
contas e clientes para classes e também modelar as funções referentes ao menu
para funcionarem normalmente utilizando POO com as classes modeladas.