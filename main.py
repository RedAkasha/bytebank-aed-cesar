"""
ByteBank
===================================================
Disciplina: Algoritmo e Estrutura de Dados
Professor : Fernando Ferreira de Carvalho

Escopo implementado
---------------------------------------------------
Nível 1 - Operações básicas e interface
    - Menu interativo em loop contínuo com encerramento amigável.
    - Depósito: solicita o valor, valida entradas negativas/nulas e
      incrementa o saldo.
    - Saque: valida saldo insuficiente, limite por operação e valores
      negativos.
    - Tratamento de exceções (try/except) contra entradas inválidas.
    - Formatação financeira com f-strings (ex.: R$ 1.250,50).

Nível 2 - Múltiplas contas e transferências PIX
    - Contas armazenadas em memória como lista de dicionários.
    - Cadastro de clientes (nome, CPF e número de conta único).
    - Busca de conta: varre a coleção e localiza pelo número ou CPF.
    - Transferência PIX atômica, com verificação da conta de destino
      e do saldo disponível.

Execução: python main.py   (Python 3.10+, apenas biblioteca padrão)
"""

# ---------------------------------------------------------------------------
# Constantes de configuração do sistema
# ---------------------------------------------------------------------------
SALDO_INICIAL = 0.0
TITULAR = "Cliente ByteBank"
LARGURA = 56

NUMERO_CONTA_INICIAL = 1001
LIMITE_SAQUE = 5000.00


# ---------------------------------------------------------------------------
# Camada de apresentação (interface com o usuário)
# ---------------------------------------------------------------------------
def formatar_moeda(valor):
    """Devolve o valor formatado no padrão monetário brasileiro (R$)."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def linha(caractere="-"):
    """Imprime uma linha divisória com a largura padrão do sistema."""
    print(caractere * LARGURA)


def titulo(texto):
    """Imprime o título da operação em execução."""
    print()
    print(f">>> {texto}")


def exibir_cabecalho(conta):
    """Imprime o cabeçalho de identificação do sistema."""
    print()
    linha("=")
    print("=== ByteBank ===".center(LARGURA))
    print(f"Conta {conta['numero']} - Titular: {conta['nome']}".center(LARGURA))
    linha("=")


def exibir_menu():
    """Imprime as opções disponíveis no menu principal."""
    print()
    linha("-")
    print("[1]  Consultar Saldo")
    print("[2]  Depositar")
    print("[3]  Sacar")
    print("[4]  Cadastrar Conta")
    print("[5]  Buscar Conta")
    print("[6]  Transferir via PIX")
    print("[7]  Sair")
    linha("-")


def informar_saldo(conta):
    """Imprime o saldo atualizado da conta."""
    print(f"[SALDO] Novo saldo: {formatar_moeda(conta['saldo'])}")


# ---------------------------------------------------------------------------
# Camada de entrada e validação de dados
# ---------------------------------------------------------------------------
def ler_opcao():
    """Lê a opção digitada pelo usuário e devolve o texto já limpo."""
    return input("> Digite a operação desejada: ").strip()


def ler_texto(rotulo):
    """Lê um texto simples já sem espaços nas pontas."""
    return input(f"{rotulo}: ").strip()


def ler_valor(rotulo):
    """
    Lê um valor monetário informado pelo usuário.

    Devolve None quando a entrada não é numérica ou quando o valor é
    negativo ou zerado.
    """
    entrada = input(f"Informe o valor do {rotulo}: R$ ").strip().replace(",", ".")

    try:
        valor = float(entrada)
    except ValueError:
        print("[ERRO] Valor inválido. Digite apenas números (ex.: 150.00).")
        return None

    if valor <= 0:
        print(f"[ERRO] Não é permitido {rotulo} de valor negativo ou zerado.")
        return None

    return round(valor, 2)


# ---------------------------------------------------------------------------
# Nível 2 - Coleção de contas em memória (lista de dicionários)
# ---------------------------------------------------------------------------
def criar_conta(numero, nome, cpf, saldo=SALDO_INICIAL):
    """Monta o dicionário que representa uma conta do ByteBank."""
    return {
        "numero": numero,
        "nome": nome,
        "cpf": cpf,
        "saldo": saldo,
    }


def gerar_numero_conta(contas):
    """Gera um número de conta sequencial garantidamente único."""
    maior = NUMERO_CONTA_INICIAL - 1

    for conta in contas:
        numero = int(conta["numero"])
        if numero > maior:
            maior = numero

    return str(maior + 1)


def buscar_conta(contas, chave):
    """
    Varre a coleção em memória e localiza a conta cujo número OU CPF
    corresponda à chave informada.

    Devolve o dicionário da conta ou None quando não encontrada.
    """
    procurado = "".join(caractere for caractere in chave if caractere.isdigit())

    if not procurado:
        return None

    for conta in contas:
        if conta["numero"] == procurado:
            return conta
        if conta["cpf"] and conta["cpf"] == procurado:
            return conta

    return None


def cadastrar_conta(contas):
    """Cadastra um novo cliente na coleção de contas."""
    titulo("CADASTRO DE CONTA")

    nome = ler_texto("Nome do titular")
    if not nome:
        print("[ERRO] O nome do titular não pode ficar vazio.")
        return

    entrada = ler_texto("CPF (somente números)")
    cpf = "".join(caractere for caractere in entrada if caractere.isdigit())
    if not cpf:
        print("[ERRO] CPF inválido. Informe apenas números.")
        return

    if buscar_conta(contas, cpf) is not None:
        print("[ERRO] Já existe uma conta cadastrada para este CPF.")
        return

    numero = gerar_numero_conta(contas)
    contas.append(criar_conta(numero, nome, cpf))

    print(f"[OK] Conta {numero} cadastrada para {nome}.")


def consultar_conta(contas):
    """Localiza e exibe os dados de uma conta a partir do número ou do CPF."""
    titulo("BUSCA DE CONTA")

    chave = ler_texto("Informe o número da conta ou o CPF")
    conta = buscar_conta(contas, chave)

    if conta is None:
        print("[ERRO] Conta não encontrada.")
        return

    print(f"[OK] Conta {conta['numero']}")
    print(f"     Titular: {conta['nome']}")
    print(f"     CPF    : {conta['cpf'] if conta['cpf'] else 'não informado'}")
    print(f"     Saldo  : {formatar_moeda(conta['saldo'])}")


# ---------------------------------------------------------------------------
# Nível 1 - Operações financeiras básicas
# ---------------------------------------------------------------------------
def consultar_saldo(conta):
    """Exibe o saldo atual da conta. Não altera o saldo."""
    print()
    print(f"[SALDO] Saldo disponível: {formatar_moeda(conta['saldo'])}")


def depositar(conta):
    """Credita um valor na conta após validar a entrada."""
    titulo("DEPÓSITO")

    valor = ler_valor("depósito")
    if valor is None:
        print("[AVISO] Depósito não realizado.")
        return

    conta["saldo"] = round(conta["saldo"] + valor, 2)

    print(f"[OK] Depósito de {formatar_moeda(valor)} realizado com sucesso.")
    informar_saldo(conta)


def sacar(conta):
    """Debita um valor da conta após validar saldo e limite por operação."""
    titulo("SAQUE")
    print(f"Limite por operação: {formatar_moeda(LIMITE_SAQUE)}")

    valor = ler_valor("saque")
    if valor is None:
        print("[AVISO] Saque não realizado.")
        return

    if valor > LIMITE_SAQUE:
        print(f"[ERRO] Valor acima do limite por operação "
              f"({formatar_moeda(LIMITE_SAQUE)}).")
        print("[AVISO] Saque não realizado.")
        return

    if valor > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para realizar o saque.")
        print(f"       Saldo disponível: {formatar_moeda(conta['saldo'])}")
        print("[AVISO] Saque não realizado.")
        return

    conta["saldo"] = round(conta["saldo"] - valor, 2)

    print(f"[OK] Saque de {formatar_moeda(valor)} realizado com sucesso.")
    informar_saldo(conta)


# ---------------------------------------------------------------------------
# Nível 2 - Transferência PIX
# ---------------------------------------------------------------------------
def transferir_pix(conta, contas):
    """
    Transferência PIX atômica.

    O débito na origem e o crédito no destino só acontecem depois que
    todas as validações passam.
    """
    titulo("TRANSFERÊNCIA PIX")

    chave = ler_texto("Chave de destino (número da conta ou CPF)")
    destino = buscar_conta(contas, chave)

    if destino is None:
        print("[ERRO] Chave PIX não encontrada.")
        print("[AVISO] Transferência não realizada.")
        return

    if destino["numero"] == conta["numero"]:
        print("[ERRO] Não é possível transferir para a própria conta.")
        print("[AVISO] Transferência não realizada.")
        return

    print(f"Destinatário: {destino['nome']} (conta {destino['numero']})")

    valor = ler_valor("PIX")
    if valor is None:
        print("[AVISO] Transferência não realizada.")
        return

    if valor > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para realizar a transferência.")
        print(f"       Saldo disponível: {formatar_moeda(conta['saldo'])}")
        print("[AVISO] Transferência não realizada.")
        return

    conta["saldo"] = round(conta["saldo"] - valor, 2)
    destino["saldo"] = round(destino["saldo"] + valor, 2)

    print(f"[OK] PIX de {formatar_moeda(valor)} enviado com sucesso.")
    informar_saldo(conta)


# ---------------------------------------------------------------------------
# Loop principal do sistema
# ---------------------------------------------------------------------------
def main():
    """Mantém o menu do ByteBank em execução até o usuário escolher sair."""
    contas = [criar_conta(str(NUMERO_CONTA_INICIAL), TITULAR, "", SALDO_INICIAL)]
    conta = contas[0]
    executando = True

    exibir_cabecalho(conta)

    while executando:
        exibir_menu()
        opcao = ler_opcao()

        if opcao == "1":
            consultar_saldo(conta)
        elif opcao == "2":
            depositar(conta)
        elif opcao == "3":
            sacar(conta)
        elif opcao == "4":
            cadastrar_conta(contas)
        elif opcao == "5":
            consultar_conta(contas)
        elif opcao == "6":
            transferir_pix(conta, contas)
        elif opcao == "7":
            print()
            print(f"[SALDO] Saldo final: {formatar_moeda(conta['saldo'])}")
            print("Obrigado por usar o ByteBank. Até logo!")
            executando = False
        else:
            print()
            print("[ERRO] Opção inválida. Escolha uma opção entre 1 e 7.")


if __name__ == "__main__":
    main()
