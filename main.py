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

Nível 3 - Estruturas de dados avançadas
    - TAD PILHA: cada transação é empilhada com append(); o estorno da
      última transação usa pop() e reverte o movimento.
    - TAD FILA: boletos agendados são processados na ordem de chegada
      (FIFO) com pop(0).

Execução: python main.py   (Python 3.10+, apenas biblioteca padrão)
"""

from datetime import datetime

# ---------------------------------------------------------------------------
# Constantes de configuração do sistema
# ---------------------------------------------------------------------------
SALDO_INICIAL = 0.0
TITULAR = "Cliente ByteBank"
LARGURA = 56

NUMERO_CONTA_INICIAL = 1001
LIMITE_SAQUE = 5000.00

# Transações que só podem ser estornadas pela conta de origem.
TIPOS_NAO_ESTORNAVEIS = ("PIX RECEBIDO", "ESTORNO RECEBIDO")


# ---------------------------------------------------------------------------
# Camada de apresentação (interface com o usuário)
# ---------------------------------------------------------------------------
def formatar_moeda(valor):
    """Devolve o valor formatado no padrão monetário brasileiro (R$)."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def agora():
    """Devolve a data e a hora corrente formatadas para o extrato."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


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
    print("[7]  Exibir Extrato (Pilha)")
    print("[8]  Estornar Última Transação")
    print("[9]  Agendar Boleto (Fila)")
    print("[10] Pagar Próximo Boleto")
    print("[11] Consultar Fila de Boletos")
    print("[12] Sair")
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
    """
    Monta o dicionário que representa uma conta do ByteBank.

    Cada conta carrega suas próprias estruturas de dados:
        historico    -> PILHA (LIFO) de transações
        fila_boletos -> FILA  (FIFO) de pagamentos agendados
    """
    return {
        "numero": numero,
        "nome": nome,
        "cpf": cpf,
        "saldo": saldo,
        "historico": [],
        "fila_boletos": [],
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
# Nível 3 - TAD Pilha: histórico de transações e estorno
# ---------------------------------------------------------------------------
def registrar_transacao(conta, tipo, valor, delta, descricao, extra=None):
    """
    Empilha (append) uma transação no histórico da conta.

    O campo delta guarda o efeito no saldo corrente e permite que o
    estorno desfaça a operação.
    """
    transacao = {
        "tipo": tipo,
        "valor": valor,
        "delta": delta,
        "descricao": descricao,
        "data": agora(),
    }

    if extra:
        transacao.update(extra)

    conta["historico"].append(transacao)
    return transacao


def exibir_extrato(conta):
    """Percorre a pilha do topo para a base, exibindo o extrato."""
    titulo("EXTRATO")

    if not conta["historico"]:
        print("[AVISO] Nenhuma transação registrada até o momento.")
        return

    print("Leitura da pilha: do topo (mais recente) para a base.")
    linha("-")

    posicao = len(conta["historico"])
    for transacao in reversed(conta["historico"]):
        sinal = "+" if transacao["delta"] > 0 else "-"
        print(
            f"{posicao:>3}. "
            f"{transacao['data']:<17}"
            f"{transacao['tipo']:<20}"
            f"{sinal + formatar_moeda(transacao['valor']):>14}"
        )
        print(f"     {transacao['descricao']}")
        posicao = posicao - 1

    linha("-")
    print(f"Transações empilhadas: {len(conta['historico'])}")
    print(f"Saldo atual          : {formatar_moeda(conta['saldo'])}")


def validar_estorno(conta, contas, transacao):
    """
    Verifica se a transação do topo da pilha pode ser desfeita.

    Devolve (True, "") quando o estorno é possível ou (False, motivo).
    """
    tipo = transacao["tipo"]

    if tipo in TIPOS_NAO_ESTORNAVEIS:
        return False, "Esta transação só pode ser estornada pela conta de origem."

    if transacao["delta"] > 0 and conta["saldo"] < transacao["delta"]:
        return False, "Saldo insuficiente para devolver o valor creditado."

    if tipo == "PIX ENVIADO":
        destino = buscar_conta(contas, transacao["destino"])
        if destino is None:
            return False, "Conta de destino não localizada."
        if destino["saldo"] < transacao["valor"]:
            return False, "A conta de destino não possui saldo para devolver o PIX."

    return True, ""


def aplicar_reversao(conta, contas, transacao):
    """Desfaz o efeito no saldo e os efeitos colaterais da transação."""
    tipo = transacao["tipo"]

    conta["saldo"] = round(conta["saldo"] - transacao["delta"], 2)

    if tipo == "PIX ENVIADO":
        destino = buscar_conta(contas, transacao["destino"])
        destino["saldo"] = round(destino["saldo"] - transacao["valor"], 2)
        registrar_transacao(
            destino,
            "ESTORNO RECEBIDO",
            transacao["valor"],
            -transacao["valor"],
            f"Estorno de PIX da conta {conta['numero']}",
        )

    elif tipo == "BOLETO PAGO":
        conta["fila_boletos"].insert(0, transacao["boleto"])


def estornar_ultima_transacao(conta, contas):
    """
    Desempilha (pop) a transação do topo do histórico e reverte o movimento.

    Operação LIFO: a última transação registrada é a primeira a ser desfeita.
    """
    titulo("ESTORNO DA ÚLTIMA TRANSAÇÃO")

    if not conta["historico"]:
        print("[ERRO] Não há transações na pilha para estornar.")
        return

    topo = conta["historico"][-1]
    print(f"Topo da pilha: {topo['tipo']} de {formatar_moeda(topo['valor'])}")
    print(f"Registrada em: {topo['data']}")

    permitido, motivo = validar_estorno(conta, contas, topo)
    if not permitido:
        print(f"[ERRO] {motivo}")
        print("[AVISO] Estorno não realizado.")
        return

    transacao = conta["historico"].pop()
    aplicar_reversao(conta, contas, transacao)

    print(f"[OK] Transação '{transacao['tipo']}' estornada com sucesso.")
    informar_saldo(conta)


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
    registrar_transacao(conta, "DEPÓSITO", valor, valor, "Depósito em conta")

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
    registrar_transacao(conta, "SAQUE", valor, -valor, "Saque em conta")

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

    registrar_transacao(
        conta,
        "PIX ENVIADO",
        valor,
        -valor,
        f"PIX para {destino['nome']} (conta {destino['numero']})",
        {"destino": destino["numero"]},
    )
    registrar_transacao(
        destino,
        "PIX RECEBIDO",
        valor,
        valor,
        f"PIX de {conta['nome']} (conta {conta['numero']})",
    )

    print(f"[OK] PIX de {formatar_moeda(valor)} enviado com sucesso.")
    informar_saldo(conta)


# ---------------------------------------------------------------------------
# Nível 3 - TAD Fila: boletos agendados (FIFO)
# ---------------------------------------------------------------------------
def agendar_boleto(conta):
    """Enfileira (append) um novo boleto no fim da fila de pagamentos."""
    titulo("AGENDAR BOLETO")

    descricao = ler_texto("Descrição do boleto")
    if not descricao:
        print("[ERRO] A descrição do boleto não pode ficar vazia.")
        return

    valor = ler_valor("boleto")
    if valor is None:
        print("[AVISO] Boleto não agendado.")
        return

    conta["fila_boletos"].append({"descricao": descricao, "valor": valor})

    print(f"[OK] Boleto '{descricao}' de {formatar_moeda(valor)} agendado.")
    print(f"     Posição na fila: {len(conta['fila_boletos'])}")


def consultar_fila(conta):
    """Exibe a fila de boletos na ordem de processamento (FIFO)."""
    titulo("FILA DE BOLETOS AGENDADOS")

    if not conta["fila_boletos"]:
        print("[AVISO] Não há boletos agendados.")
        return

    print("Leitura da fila: do início (próximo a ser pago) para o fim.")
    linha("-")

    for posicao, boleto in enumerate(conta["fila_boletos"], start=1):
        print(
            f"{posicao:>3}. "
            f"{boleto['descricao']:<38}"
            f"{formatar_moeda(boleto['valor']):>14}"
        )

    linha("-")
    total = sum(boleto["valor"] for boleto in conta["fila_boletos"])
    print(f"Boletos na fila: {len(conta['fila_boletos'])}")
    print(f"Total agendado : {formatar_moeda(total)}")


def pagar_proximo_boleto(conta):
    """
    Desenfileira (pop(0)) o boleto mais antigo e realiza o pagamento.

    Sem saldo suficiente, o boleto permanece na primeira posição.
    """
    titulo("PAGAMENTO DO PRÓXIMO BOLETO")

    if not conta["fila_boletos"]:
        print("[ERRO] Não há boletos na fila para pagamento.")
        return

    proximo = conta["fila_boletos"][0]
    print(f"Próximo da fila: {proximo['descricao']}")
    print(f"Valor          : {formatar_moeda(proximo['valor'])}")

    if proximo["valor"] > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para pagar este boleto.")
        print(f"       Saldo disponível: {formatar_moeda(conta['saldo'])}")
        print("[AVISO] O boleto permanece na primeira posição da fila.")
        return

    boleto = conta["fila_boletos"].pop(0)
    conta["saldo"] = round(conta["saldo"] - boleto["valor"], 2)

    registrar_transacao(
        conta,
        "BOLETO PAGO",
        boleto["valor"],
        -boleto["valor"],
        f"Pagamento de boleto: {boleto['descricao']}",
        {"boleto": boleto},
    )

    print(f"[OK] Boleto '{boleto['descricao']}' pago com sucesso.")
    informar_saldo(conta)
    print(f"[FILA] Boletos restantes: {len(conta['fila_boletos'])}")


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
            exibir_extrato(conta)
        elif opcao == "8":
            estornar_ultima_transacao(conta, contas)
        elif opcao == "9":
            agendar_boleto(conta)
        elif opcao == "10":
            pagar_proximo_boleto(conta)
        elif opcao == "11":
            consultar_fila(conta)
        elif opcao == "12":
            print()
            print(f"[SALDO] Saldo final: {formatar_moeda(conta['saldo'])}")
            print("Obrigado por usar o ByteBank. Até logo!")
            executando = False
        else:
            print()
            print("[ERRO] Opção inválida. Escolha uma opção entre 1 e 12.")


if __name__ == "__main__":
    main()
