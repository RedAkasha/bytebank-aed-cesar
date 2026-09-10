"""
ByteBank
===================================
Disciplina: Algoritmo e Estrutura de Dados
Professor : Fernando Ferreira de Carvalho

Sprint 1 / Nível 1 - Produto Mínimo Viável (MVP)
------------------------------------------------
Escopo desta entrega:
    - Menu interativo rodando em loop contínuo.
    - Operações ativas: Consultar Saldo, Depositar e Sacar.

Regras de negócio críticas:
    - Saque bloqueado quando o saldo for insuficiente.
    - Bloqueio estrito de valores negativos (ou zerados) em depósitos e saques.
    - Entradas não numéricas e opções inexistentes são tratadas sem quebrar o programa.

"""

# ---------------------------------------------------------------------------
# Constantes de configuração do sistema
# ---------------------------------------------------------------------------
SALDO_INICIAL = 0.0
TITULAR = "Cliente ByteBank"
LARGURA = 42


# ---------------------------------------------------------------------------
# Camada de apresentação (interface com o usuário)
# ---------------------------------------------------------------------------
def exibir_cabecalho():
    """Imprime o cabeçalho de identificação do sistema."""
    print("=" * LARGURA)
    print("=== ByteBank MVP ===".center(LARGURA))
    print(f"Titular: {TITULAR}".center(LARGURA))
    print("=" * LARGURA)


def exibir_menu():
    """Imprime as opções disponíveis no menu principal."""
    print()
    print("-" * LARGURA)
    print("[1] Consultar Saldo")
    print("[2] Depositar")
    print("[3] Sacar")
    print("[4] Sair")
    print("-" * LARGURA)


def formatar_moeda(valor):
    """Devolve o valor formatado no padrão monetário brasileiro (R$)."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


# ---------------------------------------------------------------------------
# Camada de entrada e validação de dados
# ---------------------------------------------------------------------------
def ler_opcao():
    """Lê a opção digitada pelo usuário e devolve o texto já limpo."""
    return input("> Digite a operação desejada: ").strip()


def ler_valor(rotulo):
    """
    Lê um valor monetário informado pelo usuário.
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

    return valor


# ---------------------------------------------------------------------------
# Camada de operações financeiras (regras de negócio)
# ---------------------------------------------------------------------------
def consultar_saldo(saldo):
    """Exibe o saldo atual da conta. Não altera o saldo."""
    print()
    print(f"[SALDO] Saldo disponível: {formatar_moeda(saldo)}")


def depositar(saldo):
    """
    Realiza um depósito na conta.
    """
    print()
    print(">>> DEPÓSITO")
    valor = ler_valor("depósito")

    if valor is None:
        print("[AVISO] Depósito não realizado.")
        return saldo

    saldo = saldo + valor
    print(f"[OK] Depósito de {formatar_moeda(valor)} realizado com sucesso.")
    print(f"[SALDO] Novo saldo: {formatar_moeda(saldo)}")
    return saldo


def sacar(saldo):
    """
    Realiza um saque na conta.
    """
    print()
    print(">>> SAQUE")
    valor = ler_valor("saque")

    if valor is None:
        print("[AVISO] Saque não realizado.")
        return saldo

    if valor > saldo:
        print("[ERRO] Saldo insuficiente para realizar o saque.")
        print(f"       Saldo disponível: {formatar_moeda(saldo)}")
        print("[AVISO] Saque não realizado.")
        return saldo

    saldo = saldo - valor
    print(f"[OK] Saque de {formatar_moeda(valor)} realizado com sucesso.")
    print(f"[SALDO] Novo saldo: {formatar_moeda(saldo)}")
    return saldo


# ---------------------------------------------------------------------------
# Loop principal do sistema
# ---------------------------------------------------------------------------
def main():
    """Mantém o menu do ByteBank em execução até o usuário escolher sair."""
    saldo = SALDO_INICIAL
    executando = True

    exibir_cabecalho()

    while executando:
        exibir_menu()
        opcao = ler_opcao()

        if opcao == "1":
            consultar_saldo(saldo)
        elif opcao == "2":
            saldo = depositar(saldo)
        elif opcao == "3":
            saldo = sacar(saldo)
        elif opcao == "4":
            print()
            print(f"[SALDO] Saldo final: {formatar_moeda(saldo)}")
            print("Obrigado por usar o ByteBank. Até logo!")
            executando = False
        else:
            print()
            print("[ERRO] Opção inválida. Escolha uma opção entre 1 e 4.")


if __name__ == "__main__":
    main()
