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

Funcionalidades extras (item 4 - pontuação bônus)
    - Cofrinhos / Caixinhas com rendimento simulado (juros simples).
    - Categorização de gastos e relatório com somatórios por categoria.
    - Cartão de crédito: limite, compras no crédito e pagamento da fatura.
    - Carteira multimoedas com tabela de taxas de câmbio.
    - Programa de fidelidade BytePoints com resgate em cashback.
    - Empréstimos pré-aprovados com parcelamento passivo.

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

# Categorização de gastos
CATEGORIAS = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Lazer",
    "Saúde",
    "Educação",
    "Transferências",
    "Outros",
]
CATEGORIA_ENTRADA = "Entradas"

# Cofrinhos - rendimento simulado por juros simples
TAXA_COFRINHO = 0.005

# Cartão de crédito
LIMITE_CARTAO = 1500.00

# Carteira multimoedas
TAXAS_CAMBIO = {"USD": 5.42, "EUR": 5.88, "BTC": 352000.00}
CASAS_DECIMAIS = {"USD": 2, "EUR": 2, "BTC": 8}

# Programa de fidelidade BytePoints
PONTOS_POR_REAL = 0.1
VALOR_DO_PONTO = 0.01

# Empréstimos pré-aprovados
MULTIPLICADOR_EMPRESTIMO = 3
TAXA_JUROS_EMPRESTIMO = 0.025
PARCELAS_DISPONIVEIS = [6, 12, 24]

# Transações que entram no relatório de gastos por categoria.
# O pagamento da fatura fica de fora porque as compras já foram
# contabilizadas no momento do lançamento.
TIPOS_DE_GASTO = (
    "SAQUE",
    "PIX ENVIADO",
    "BOLETO PAGO",
    "COMPRA CRÉDITO",
    "PARCELA EMPRÉSTIMO",
)

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


def formatar_moeda_estrangeira(valor, moeda):
    """Formata um saldo em moeda estrangeira com suas casas decimais."""
    casas = CASAS_DECIMAIS[moeda]
    texto = f"{valor:,.{casas}f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{moeda} {texto}"


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
    print("[12] Criar Cofrinho")
    print("[13] Guardar no Cofrinho")
    print("[14] Resgatar do Cofrinho")
    print("[15] Simular Rendimento do Cofrinho")
    print("[16] Consultar Cofrinhos")
    print("[17] Relatório de Gastos por Categoria")
    print("[18] Comprar no Crédito")
    print("[19] Pagar Fatura do Cartão")
    print("[20] Consultar Cartão de Crédito")
    print("[21] Comprar Moeda Estrangeira")
    print("[22] Vender Moeda Estrangeira")
    print("[23] Consultar Carteira Multimoedas")
    print("[24] Consultar BytePoints")
    print("[25] Resgatar BytePoints")
    print("[26] Simular Empréstimo")
    print("[27] Contratar Empréstimo")
    print("[28] Pagar Parcela do Empréstimo")
    print("[29] Consultar Empréstimos")
    print("[30] Sair")
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


def ler_quantidade(moeda):
    """Lê uma quantidade de moeda estrangeira. Devolve None se inválida."""
    entrada = input(f"Informe a quantidade de {moeda}: ").strip().replace(",", ".")

    try:
        quantidade = float(entrada)
    except ValueError:
        print("[ERRO] Quantidade inválida. Digite apenas números.")
        return None

    if quantidade <= 0:
        print("[ERRO] A quantidade deve ser maior que zero.")
        return None

    return round(quantidade, CASAS_DECIMAIS[moeda])


def ler_inteiro(rotulo):
    """Lê um número inteiro positivo. Devolve None se a entrada for inválida."""
    entrada = input(f"{rotulo}: ").strip()

    try:
        numero = int(entrada)
    except ValueError:
        print("[ERRO] Valor inválido. Digite um número inteiro.")
        return None

    if numero <= 0:
        print("[ERRO] O número deve ser maior que zero.")
        return None

    return numero


def escolher_da_lista(rotulo, itens):
    """
    Exibe uma lista numerada e devolve o item escolhido.

    Devolve None quando o usuário digita uma opção inexistente.
    """
    print()
    print(f"{rotulo}:")
    for indice, item in enumerate(itens, start=1):
        print(f"  [{indice}] {item}")

    entrada = input("> Escolha uma opção: ").strip()

    try:
        escolhido = int(entrada)
    except ValueError:
        print("[ERRO] Opção inválida. Digite o número correspondente.")
        return None

    if escolhido < 1 or escolhido > len(itens):
        print(f"[ERRO] Opção inválida. Escolha um número entre 1 e {len(itens)}.")
        return None

    return itens[escolhido - 1]


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
        "cofrinhos": {},
        "cartao": {"limite": LIMITE_CARTAO, "fatura": 0.0, "compras": []},
        "moedas": {moeda: 0.0 for moeda in TAXAS_CAMBIO},
        "pontos": 0,
        "emprestimos": [],
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
def registrar_transacao(conta, tipo, valor, delta, categoria, descricao, extra=None):
    """
    Empilha (append) uma transação no histórico da conta.

    O campo delta guarda o efeito no saldo corrente e permite que o
    estorno desfaça a operação.
    """
    transacao = {
        "tipo": tipo,
        "valor": valor,
        "delta": delta,
        "categoria": categoria,
        "descricao": descricao,
        "pontos": 0,
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

    if transacao["pontos"] > conta["pontos"]:
        return False, "Os BytePoints desta transação já foram resgatados."

    if tipo == "PIX ENVIADO":
        destino = buscar_conta(contas, transacao["destino"])
        if destino is None:
            return False, "Conta de destino não localizada."
        if destino["saldo"] < transacao["valor"]:
            return False, "A conta de destino não possui saldo para devolver o PIX."

    if tipo == "COFRINHO GUARDAR":
        cofrinho = conta["cofrinhos"].get(transacao["cofrinho"])
        if cofrinho is None or cofrinho["saldo"] < transacao["valor"]:
            return False, "O cofrinho não possui saldo suficiente para o estorno."

    if tipo == "CÂMBIO COMPRA":
        moeda = transacao["moeda"]
        if conta["moedas"][moeda] < transacao["quantidade"]:
            return False, f"Saldo em {moeda} insuficiente para desfazer a compra."

    if tipo == "EMPRÉSTIMO" and transacao["emprestimo"]["parcelas_pagas"] > 0:
        return False, "Empréstimo com parcelas pagas não pode ser estornado."

    return True, ""


def aplicar_reversao(conta, contas, transacao):
    """Desfaz o efeito no saldo e os efeitos colaterais da transação."""
    tipo = transacao["tipo"]

    conta["saldo"] = round(conta["saldo"] - transacao["delta"], 2)
    conta["pontos"] = conta["pontos"] - transacao["pontos"]

    if tipo == "PIX ENVIADO":
        destino = buscar_conta(contas, transacao["destino"])
        destino["saldo"] = round(destino["saldo"] - transacao["valor"], 2)
        registrar_transacao(
            destino,
            "ESTORNO RECEBIDO",
            transacao["valor"],
            -transacao["valor"],
            "Transferências",
            f"Estorno de PIX da conta {conta['numero']}",
        )

    elif tipo == "COFRINHO GUARDAR":
        cofrinho = conta["cofrinhos"][transacao["cofrinho"]]
        cofrinho["saldo"] = round(cofrinho["saldo"] - transacao["valor"], 2)

    elif tipo == "COFRINHO RESGATE":
        cofrinho = conta["cofrinhos"][transacao["cofrinho"]]
        cofrinho["saldo"] = round(cofrinho["saldo"] + transacao["valor"], 2)

    elif tipo == "COMPRA CRÉDITO":
        conta["cartao"]["fatura"] = round(
            conta["cartao"]["fatura"] - transacao["valor"], 2
        )
        conta["cartao"]["compras"].pop()

    elif tipo == "PAGAMENTO FATURA":
        conta["cartao"]["fatura"] = round(
            conta["cartao"]["fatura"] + transacao["valor"], 2
        )
        conta["cartao"]["compras"].extend(transacao["compras_liquidadas"])

    elif tipo == "CÂMBIO COMPRA":
        moeda = transacao["moeda"]
        conta["moedas"][moeda] = round(
            conta["moedas"][moeda] - transacao["quantidade"], 8
        )

    elif tipo == "CÂMBIO VENDA":
        moeda = transacao["moeda"]
        conta["moedas"][moeda] = round(
            conta["moedas"][moeda] + transacao["quantidade"], 8
        )

    elif tipo == "RESGATE BYTEPOINTS":
        conta["pontos"] = conta["pontos"] + transacao["pontos_resgatados"]

    elif tipo == "BOLETO PAGO":
        conta["fila_boletos"].insert(0, transacao["boleto"])

    elif tipo == "EMPRÉSTIMO":
        conta["emprestimos"].remove(transacao["emprestimo"])

    elif tipo == "PARCELA EMPRÉSTIMO":
        emprestimo = transacao["emprestimo"]
        emprestimo["parcelas_pagas"] = emprestimo["parcelas_pagas"] - 1
        emprestimo["quitado"] = False


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
    registrar_transacao(
        conta, "DEPÓSITO", valor, valor, CATEGORIA_ENTRADA, "Depósito em conta"
    )

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

    categoria = escolher_da_lista("Categoria do gasto", CATEGORIAS)
    if categoria is None:
        categoria = "Outros"
        print("[AVISO] Categoria não reconhecida. Classificado como 'Outros'.")

    conta["saldo"] = round(conta["saldo"] - valor, 2)
    transacao = registrar_transacao(
        conta, "SAQUE", valor, -valor, categoria, "Saque em conta"
    )
    creditar_pontos(conta, valor, transacao)

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

    transacao = registrar_transacao(
        conta,
        "PIX ENVIADO",
        valor,
        -valor,
        "Transferências",
        f"PIX para {destino['nome']} (conta {destino['numero']})",
        {"destino": destino["numero"]},
    )
    registrar_transacao(
        destino,
        "PIX RECEBIDO",
        valor,
        valor,
        CATEGORIA_ENTRADA,
        f"PIX de {conta['nome']} (conta {conta['numero']})",
    )
    creditar_pontos(conta, valor, transacao)

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

    categoria = escolher_da_lista("Categoria do gasto", CATEGORIAS)
    if categoria is None:
        categoria = "Outros"
        print("[AVISO] Categoria não reconhecida. Classificado como 'Outros'.")

    conta["fila_boletos"].append(
        {"descricao": descricao, "valor": valor, "categoria": categoria}
    )

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
            f"{boleto['descricao']:<26}"
            f"{boleto['categoria']:<16}"
            f"{formatar_moeda(boleto['valor']):>12}"
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
        boleto["categoria"],
        f"Pagamento de boleto: {boleto['descricao']}",
        {"boleto": boleto},
    )

    print(f"[OK] Boleto '{boleto['descricao']}' pago com sucesso.")
    informar_saldo(conta)
    print(f"[FILA] Boletos restantes: {len(conta['fila_boletos'])}")


# ---------------------------------------------------------------------------
# Extra - Cofrinhos / Caixinhas de investimento
# ---------------------------------------------------------------------------
def criar_cofrinho(conta):
    """Cria uma nova subconta de investimento."""
    titulo("CRIAR COFRINHO")

    nome = ler_texto("Nome do cofrinho")
    if not nome:
        print("[ERRO] O nome do cofrinho não pode ficar vazio.")
        return

    if nome in conta["cofrinhos"]:
        print("[ERRO] Já existe um cofrinho com esse nome.")
        return

    conta["cofrinhos"][nome] = {"saldo": 0.0, "rendimento": 0.0, "meses": 0}
    print(f"[OK] Cofrinho '{nome}' criado com sucesso.")


def selecionar_cofrinho(conta):
    """Devolve o nome de um cofrinho escolhido pelo usuário."""
    if not conta["cofrinhos"]:
        print("[ERRO] Nenhum cofrinho cadastrado.")
        return None

    return escolher_da_lista("Selecione o cofrinho", list(conta["cofrinhos"].keys()))


def guardar_no_cofrinho(conta):
    """Transfere saldo da conta corrente para um cofrinho."""
    titulo("GUARDAR NO COFRINHO")

    nome = selecionar_cofrinho(conta)
    if nome is None:
        return

    valor = ler_valor("depósito no cofrinho")
    if valor is None:
        print("[AVISO] Operação não realizada.")
        return

    if valor > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para guardar este valor.")
        return

    conta["saldo"] = round(conta["saldo"] - valor, 2)
    conta["cofrinhos"][nome]["saldo"] = round(
        conta["cofrinhos"][nome]["saldo"] + valor, 2
    )

    registrar_transacao(
        conta,
        "COFRINHO GUARDAR",
        valor,
        -valor,
        "Outros",
        f"Valor guardado no cofrinho '{nome}'",
        {"cofrinho": nome},
    )

    print(f"[OK] {formatar_moeda(valor)} guardados no cofrinho '{nome}'.")
    informar_saldo(conta)


def resgatar_do_cofrinho(conta):
    """Devolve saldo de um cofrinho para a conta corrente."""
    titulo("RESGATAR DO COFRINHO")

    nome = selecionar_cofrinho(conta)
    if nome is None:
        return

    cofrinho = conta["cofrinhos"][nome]
    print(f"Saldo do cofrinho: {formatar_moeda(cofrinho['saldo'])}")

    valor = ler_valor("resgate")
    if valor is None:
        print("[AVISO] Operação não realizada.")
        return

    if valor > cofrinho["saldo"]:
        print("[ERRO] O cofrinho não possui saldo suficiente para este resgate.")
        return

    cofrinho["saldo"] = round(cofrinho["saldo"] - valor, 2)
    conta["saldo"] = round(conta["saldo"] + valor, 2)

    registrar_transacao(
        conta,
        "COFRINHO RESGATE",
        valor,
        valor,
        CATEGORIA_ENTRADA,
        f"Resgate do cofrinho '{nome}'",
        {"cofrinho": nome},
    )

    print(f"[OK] {formatar_moeda(valor)} resgatados do cofrinho '{nome}'.")
    informar_saldo(conta)


def simular_rendimento(conta):
    """
    Aplica o rendimento simulado de um cofrinho por juros simples.

    Fórmula: J = C * i * t (capital x taxa mensal x número de meses).
    """
    titulo("RENDIMENTO DO COFRINHO")

    nome = selecionar_cofrinho(conta)
    if nome is None:
        return

    cofrinho = conta["cofrinhos"][nome]
    if cofrinho["saldo"] <= 0:
        print("[ERRO] O cofrinho está vazio.")
        return

    meses = ler_inteiro("Quantos meses deseja simular")
    if meses is None:
        return

    juros = round(cofrinho["saldo"] * TAXA_COFRINHO * meses, 2)
    cofrinho["saldo"] = round(cofrinho["saldo"] + juros, 2)
    cofrinho["rendimento"] = round(cofrinho["rendimento"] + juros, 2)
    cofrinho["meses"] = cofrinho["meses"] + meses

    print(f"[OK] Rendimento de {meses} mes(es) creditado no cofrinho '{nome}'.")
    print(f"     Juros simples    : {formatar_moeda(juros)}")
    print(f"     Saldo do cofrinho: {formatar_moeda(cofrinho['saldo'])}")


def consultar_cofrinhos(conta):
    """Exibe os cofrinhos da conta e o total guardado."""
    titulo("MEUS COFRINHOS")

    if not conta["cofrinhos"]:
        print("[AVISO] Você ainda não possui cofrinhos.")
        return

    linha("-")
    for nome, cofrinho in conta["cofrinhos"].items():
        print(
            f"{nome:<22}"
            f"{formatar_moeda(cofrinho['saldo']):>14}"
            f"{'rend. ' + formatar_moeda(cofrinho['rendimento']):>20}"
        )
    linha("-")

    total = sum(cofrinho["saldo"] for cofrinho in conta["cofrinhos"].values())
    print(f"Total guardado: {formatar_moeda(total)}")


# ---------------------------------------------------------------------------
# Extra - Categorização de gastos e relatório
# ---------------------------------------------------------------------------
def agrupar_por_categoria(conta):
    """
    Percorre a pilha de transações e acumula os gastos por categoria.

    Devolve um dicionário {categoria: {"total": x, "quantidade": n}}.
    """
    agrupado = {}

    for transacao in conta["historico"]:
        if transacao["tipo"] not in TIPOS_DE_GASTO:
            continue

        categoria = transacao["categoria"]
        if categoria not in agrupado:
            agrupado[categoria] = {"total": 0.0, "quantidade": 0}

        agrupado[categoria]["total"] = round(
            agrupado[categoria]["total"] + transacao["valor"], 2
        )
        agrupado[categoria]["quantidade"] = agrupado[categoria]["quantidade"] + 1

    return agrupado


def relatorio_de_gastos(conta):
    """Exibe os somatórios acumulados por categoria."""
    titulo("RELATÓRIO DE GASTOS POR CATEGORIA")

    agrupado = agrupar_por_categoria(conta)

    if not agrupado:
        print("[AVISO] Nenhum gasto registrado até o momento.")
        return

    linha("-")
    for categoria, dados in agrupado.items():
        print(
            f"{categoria:<22}"
            f"{dados['quantidade']:>4} lanc."
            f"{formatar_moeda(dados['total']):>18}"
        )
    linha("-")

    total = sum(dados["total"] for dados in agrupado.values())
    print(f"{'TOTAL GERAL':<22}{formatar_moeda(total):>22}")


# ---------------------------------------------------------------------------
# Extra - Cartão de crédito e fatura
# ---------------------------------------------------------------------------
def limite_disponivel(conta):
    """Devolve o limite de crédito ainda disponível."""
    return round(conta["cartao"]["limite"] - conta["cartao"]["fatura"], 2)


def comprar_no_credito(conta):
    """Lança uma compra na fatura, respeitando o limite aprovado."""
    titulo("COMPRA NO CRÉDITO")
    print(f"Limite disponível: {formatar_moeda(limite_disponivel(conta))}")

    descricao = ler_texto("Descrição da compra")
    if not descricao:
        print("[ERRO] A descrição da compra não pode ficar vazia.")
        return

    valor = ler_valor("compra")
    if valor is None:
        print("[AVISO] Compra não realizada.")
        return

    if valor > limite_disponivel(conta):
        print("[ERRO] Limite de crédito insuficiente para esta compra.")
        print("[AVISO] Compra não realizada.")
        return

    categoria = escolher_da_lista("Categoria do gasto", CATEGORIAS)
    if categoria is None:
        categoria = "Outros"
        print("[AVISO] Categoria não reconhecida. Classificado como 'Outros'.")

    conta["cartao"]["compras"].append(
        {"descricao": descricao, "valor": valor, "categoria": categoria}
    )
    conta["cartao"]["fatura"] = round(conta["cartao"]["fatura"] + valor, 2)

    registrar_transacao(
        conta,
        "COMPRA CRÉDITO",
        valor,
        0.0,
        categoria,
        f"Compra no crédito: {descricao}",
    )

    print(f"[OK] Compra de {formatar_moeda(valor)} lançada na fatura.")
    print(f"     Fatura atual: {formatar_moeda(conta['cartao']['fatura'])}")


def pagar_fatura(conta):
    """Paga a fatura utilizando o saldo corrente."""
    titulo("PAGAMENTO DA FATURA")

    cartao = conta["cartao"]

    if cartao["fatura"] <= 0:
        print("[AVISO] Não há fatura em aberto.")
        return

    print(f"Fatura em aberto: {formatar_moeda(cartao['fatura'])}")

    valor = ler_valor("pagamento da fatura")
    if valor is None:
        print("[AVISO] Pagamento não realizado.")
        return

    if valor > cartao["fatura"]:
        print("[ERRO] O valor informado é maior que a fatura em aberto.")
        return

    if valor > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para pagar a fatura.")
        return

    conta["saldo"] = round(conta["saldo"] - valor, 2)
    cartao["fatura"] = round(cartao["fatura"] - valor, 2)

    liquidadas = []
    if cartao["fatura"] == 0:
        liquidadas = list(cartao["compras"])
        cartao["compras"].clear()

    registrar_transacao(
        conta,
        "PAGAMENTO FATURA",
        valor,
        -valor,
        "Outros",
        "Pagamento de fatura do cartão de crédito",
        {"compras_liquidadas": liquidadas},
    )

    print(f"[OK] Pagamento de {formatar_moeda(valor)} realizado.")
    print(f"     Fatura restante: {formatar_moeda(cartao['fatura'])}")
    informar_saldo(conta)


def consultar_cartao(conta):
    """Exibe o limite, a fatura e as compras lançadas."""
    titulo("CARTÃO DE CRÉDITO")

    cartao = conta["cartao"]
    print(f"Limite aprovado  : {formatar_moeda(cartao['limite'])}")
    print(f"Fatura em aberto : {formatar_moeda(cartao['fatura'])}")
    print(f"Limite disponível: {formatar_moeda(limite_disponivel(conta))}")

    if not cartao["compras"]:
        print("[AVISO] Nenhuma compra lançada na fatura atual.")
        return

    linha("-")
    for compra in cartao["compras"]:
        print(
            f"{compra['descricao']:<26}"
            f"{compra['categoria']:<16}"
            f"{formatar_moeda(compra['valor']):>12}"
        )
    linha("-")


# ---------------------------------------------------------------------------
# Extra - Carteira multimoedas (câmbio)
# ---------------------------------------------------------------------------
def comprar_moeda(conta):
    """Converte reais em moeda estrangeira pela tabela de taxas."""
    titulo("COMPRA DE MOEDA ESTRANGEIRA")

    moeda = escolher_da_lista("Selecione a moeda", list(TAXAS_CAMBIO.keys()))
    if moeda is None:
        return

    taxa = TAXAS_CAMBIO[moeda]
    print(f"Taxa: 1 {moeda} = {formatar_moeda(taxa)}")

    quantidade = ler_quantidade(moeda)
    if quantidade is None:
        print("[AVISO] Compra não realizada.")
        return

    custo = round(quantidade * taxa, 2)
    print(f"Custo total: {formatar_moeda(custo)}")

    if custo > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para esta compra de moeda.")
        print("[AVISO] Compra não realizada.")
        return

    conta["saldo"] = round(conta["saldo"] - custo, 2)
    conta["moedas"][moeda] = round(conta["moedas"][moeda] + quantidade, 8)

    registrar_transacao(
        conta,
        "CÂMBIO COMPRA",
        custo,
        -custo,
        "Outros",
        f"Compra de {formatar_moeda_estrangeira(quantidade, moeda)}",
        {"moeda": moeda, "quantidade": quantidade},
    )

    print(f"[OK] {formatar_moeda_estrangeira(quantidade, moeda)} adquiridos.")
    informar_saldo(conta)


def vender_moeda(conta):
    """Converte moeda estrangeira em reais pela tabela de taxas."""
    titulo("VENDA DE MOEDA ESTRANGEIRA")

    moeda = escolher_da_lista("Selecione a moeda", list(TAXAS_CAMBIO.keys()))
    if moeda is None:
        return

    if conta["moedas"][moeda] <= 0:
        print(f"[ERRO] Você não possui saldo em {moeda}.")
        return

    taxa = TAXAS_CAMBIO[moeda]
    print(f"Saldo disponível: "
          f"{formatar_moeda_estrangeira(conta['moedas'][moeda], moeda)}")
    print(f"Taxa: 1 {moeda} = {formatar_moeda(taxa)}")

    quantidade = ler_quantidade(moeda)
    if quantidade is None:
        print("[AVISO] Venda não realizada.")
        return

    if quantidade > conta["moedas"][moeda]:
        print(f"[ERRO] Saldo em {moeda} insuficiente para esta venda.")
        return

    recebido = round(quantidade * taxa, 2)
    conta["moedas"][moeda] = round(conta["moedas"][moeda] - quantidade, 8)
    conta["saldo"] = round(conta["saldo"] + recebido, 2)

    registrar_transacao(
        conta,
        "CÂMBIO VENDA",
        recebido,
        recebido,
        CATEGORIA_ENTRADA,
        f"Venda de {formatar_moeda_estrangeira(quantidade, moeda)}",
        {"moeda": moeda, "quantidade": quantidade},
    )

    print(f"[OK] Venda realizada. Creditado {formatar_moeda(recebido)}.")
    informar_saldo(conta)


def consultar_carteira(conta):
    """Exibe os saldos em moeda estrangeira e a tabela de câmbio."""
    titulo("CARTEIRA MULTIMOEDAS")

    linha("-")
    total = 0.0
    for moeda in TAXAS_CAMBIO:
        equivalente = round(conta["moedas"][moeda] * TAXAS_CAMBIO[moeda], 2)
        total = total + equivalente
        print(
            f"{formatar_moeda_estrangeira(conta['moedas'][moeda], moeda):<26}"
            f"{formatar_moeda(equivalente):>16}"
            f"{'taxa ' + formatar_moeda(TAXAS_CAMBIO[moeda]):>14}"
        )
    linha("-")
    print(f"Equivalente total em reais: {formatar_moeda(total)}")


# ---------------------------------------------------------------------------
# Extra - Programa de fidelidade (BytePoints)
# ---------------------------------------------------------------------------
def creditar_pontos(conta, valor, transacao):
    """
    Acumula pontos proporcionais ao valor gasto em saques e transferências.

    Os pontos ficam gravados na própria transação para que o estorno
    retire exatamente o que foi creditado.
    """
    pontos = int(valor * PONTOS_POR_REAL)

    if pontos <= 0:
        return

    conta["pontos"] = conta["pontos"] + pontos
    transacao["pontos"] = pontos
    print(f"[PONTOS] +{pontos} BytePoints (total: {conta['pontos']}).")


def consultar_pontos(conta):
    """Exibe o saldo de pontos e as regras do programa."""
    titulo("BYTEPOINTS")

    equivalente = round(conta["pontos"] * VALOR_DO_PONTO, 2)
    print(f"Saldo de pontos    : {conta['pontos']}")
    print(f"Equivalente em cash: {formatar_moeda(equivalente)}")
    print(f"Acúmulo: 1 ponto a cada {formatar_moeda(1 / PONTOS_POR_REAL)} "
          f"em saques e transferências.")
    print(f"Resgate: cada ponto vale {formatar_moeda(VALOR_DO_PONTO)}.")


def resgatar_pontos(conta):
    """Converte pontos em saldo na conta corrente (cashback)."""
    titulo("RESGATE DE BYTEPOINTS")
    print(f"Saldo de pontos: {conta['pontos']}")

    if conta["pontos"] <= 0:
        print("[ERRO] Você não possui pontos para resgatar.")
        return

    pontos = ler_inteiro("Quantos pontos deseja resgatar")
    if pontos is None:
        return

    if pontos > conta["pontos"]:
        print("[ERRO] Você não possui essa quantidade de pontos.")
        return

    valor = round(pontos * VALOR_DO_PONTO, 2)
    conta["pontos"] = conta["pontos"] - pontos
    conta["saldo"] = round(conta["saldo"] + valor, 2)

    registrar_transacao(
        conta,
        "RESGATE BYTEPOINTS",
        valor,
        valor,
        CATEGORIA_ENTRADA,
        f"Cashback de {pontos} BytePoints",
        {"pontos_resgatados": pontos},
    )

    print(f"[OK] {pontos} pontos resgatados como {formatar_moeda(valor)}.")
    informar_saldo(conta)


# ---------------------------------------------------------------------------
# Extra - Empréstimos pré-aprovados
# ---------------------------------------------------------------------------
def calcular_limite_emprestimo(conta):
    """Calcula o limite pré-aprovado com base no saldo atual."""
    return round(conta["saldo"] * MULTIPLICADOR_EMPRESTIMO, 2)


def montar_emprestimo(conta):
    """
    Monta a simulação de um empréstimo por juros simples.

    Devolve o dicionário do contrato ou None quando a entrada é inválida.
    """
    limite = calcular_limite_emprestimo(conta)
    print(f"Limite pré-aprovado: {formatar_moeda(limite)}")

    if limite <= 0:
        print("[ERRO] Sem saldo em conta, não há limite pré-aprovado.")
        return None

    valor = ler_valor("empréstimo")
    if valor is None:
        return None

    if valor > limite:
        print("[ERRO] Valor acima do limite pré-aprovado.")
        return None

    escolha = escolher_da_lista(
        "Quantidade de parcelas", [f"{p} parcelas" for p in PARCELAS_DISPONIVEIS]
    )
    if escolha is None:
        return None

    parcelas = int(escolha.split()[0])
    juros = round(valor * TAXA_JUROS_EMPRESTIMO * parcelas, 2)
    total = round(valor + juros, 2)
    valor_parcela = round(total / parcelas, 2)

    print("Simulação (juros simples: J = C * i * t)")
    print(f"  Valor solicitado: {formatar_moeda(valor)}")
    print(f"  Juros totais    : {formatar_moeda(juros)}")
    print(f"  Total a pagar   : {formatar_moeda(total)}")
    print(f"  Parcelamento    : {parcelas}x de {formatar_moeda(valor_parcela)}")

    return {
        "principal": valor,
        "juros": juros,
        "total": total,
        "parcelas": parcelas,
        "valor_parcela": valor_parcela,
        "parcelas_pagas": 0,
        "quitado": False,
    }


def simular_emprestimo(conta):
    """Simula um empréstimo sem contratar."""
    titulo("SIMULAÇÃO DE EMPRÉSTIMO")
    montar_emprestimo(conta)


def contratar_emprestimo(conta):
    """Contrata o empréstimo, creditando o valor no saldo da conta."""
    titulo("CONTRATAÇÃO DE EMPRÉSTIMO")

    emprestimo = montar_emprestimo(conta)
    if emprestimo is None:
        print("[AVISO] Empréstimo não contratado.")
        return

    conta["emprestimos"].append(emprestimo)
    conta["saldo"] = round(conta["saldo"] + emprestimo["principal"], 2)

    registrar_transacao(
        conta,
        "EMPRÉSTIMO",
        emprestimo["principal"],
        emprestimo["principal"],
        CATEGORIA_ENTRADA,
        f"Empréstimo em {emprestimo['parcelas']}x de "
        f"{formatar_moeda(emprestimo['valor_parcela'])}",
        {"emprestimo": emprestimo},
    )

    print(f"[OK] Empréstimo de {formatar_moeda(emprestimo['principal'])} creditado.")
    informar_saldo(conta)


def pagar_parcela(conta):
    """Paga a próxima parcela de um empréstimo em aberto."""
    titulo("PAGAMENTO DE PARCELA")

    abertos = [e for e in conta["emprestimos"] if not e["quitado"]]

    if not abertos:
        print("[AVISO] Não há empréstimos em aberto.")
        return

    rotulos = [
        f"{formatar_moeda(e['principal'])} - parcela "
        f"{e['parcelas_pagas'] + 1}/{e['parcelas']} de "
        f"{formatar_moeda(e['valor_parcela'])}"
        for e in abertos
    ]
    escolha = escolher_da_lista("Selecione o empréstimo", rotulos)
    if escolha is None:
        return

    emprestimo = abertos[rotulos.index(escolha)]

    if emprestimo["valor_parcela"] > conta["saldo"]:
        print("[ERRO] Saldo insuficiente para pagar a parcela.")
        print(f"       Saldo disponível: {formatar_moeda(conta['saldo'])}")
        return

    conta["saldo"] = round(conta["saldo"] - emprestimo["valor_parcela"], 2)
    emprestimo["parcelas_pagas"] = emprestimo["parcelas_pagas"] + 1

    if emprestimo["parcelas_pagas"] >= emprestimo["parcelas"]:
        emprestimo["quitado"] = True

    registrar_transacao(
        conta,
        "PARCELA EMPRÉSTIMO",
        emprestimo["valor_parcela"],
        -emprestimo["valor_parcela"],
        "Outros",
        f"Parcela {emprestimo['parcelas_pagas']}/{emprestimo['parcelas']} "
        f"do empréstimo",
        {"emprestimo": emprestimo},
    )

    print(f"[OK] Parcela de {formatar_moeda(emprestimo['valor_parcela'])} paga.")
    print(f"     Parcelas pagas: "
          f"{emprestimo['parcelas_pagas']}/{emprestimo['parcelas']}")

    if emprestimo["quitado"]:
        print("[OK] Empréstimo totalmente quitado.")

    informar_saldo(conta)


def consultar_emprestimos(conta):
    """Exibe os empréstimos contratados e o passivo em aberto."""
    titulo("EMPRÉSTIMOS")

    print(f"Limite pré-aprovado: {formatar_moeda(calcular_limite_emprestimo(conta))}")

    if not conta["emprestimos"]:
        print("[AVISO] Nenhum empréstimo contratado.")
        return

    linha("-")
    for emprestimo in conta["emprestimos"]:
        situacao = "QUITADO" if emprestimo["quitado"] else "EM ABERTO"
        print(
            f"{formatar_moeda(emprestimo['principal']):<14}"
            f"{emprestimo['parcelas']}x de "
            f"{formatar_moeda(emprestimo['valor_parcela']):<14}"
            f"{emprestimo['parcelas_pagas']}/{emprestimo['parcelas']} "
            f"{situacao}"
        )
    linha("-")

    divida = sum(
        (e["parcelas"] - e["parcelas_pagas"]) * e["valor_parcela"]
        for e in conta["emprestimos"]
        if not e["quitado"]
    )
    print(f"Passivo em aberto: {formatar_moeda(divida)}")


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
            criar_cofrinho(conta)
        elif opcao == "13":
            guardar_no_cofrinho(conta)
        elif opcao == "14":
            resgatar_do_cofrinho(conta)
        elif opcao == "15":
            simular_rendimento(conta)
        elif opcao == "16":
            consultar_cofrinhos(conta)
        elif opcao == "17":
            relatorio_de_gastos(conta)
        elif opcao == "18":
            comprar_no_credito(conta)
        elif opcao == "19":
            pagar_fatura(conta)
        elif opcao == "20":
            consultar_cartao(conta)
        elif opcao == "21":
            comprar_moeda(conta)
        elif opcao == "22":
            vender_moeda(conta)
        elif opcao == "23":
            consultar_carteira(conta)
        elif opcao == "24":
            consultar_pontos(conta)
        elif opcao == "25":
            resgatar_pontos(conta)
        elif opcao == "26":
            simular_emprestimo(conta)
        elif opcao == "27":
            contratar_emprestimo(conta)
        elif opcao == "28":
            pagar_parcela(conta)
        elif opcao == "29":
            consultar_emprestimos(conta)
        elif opcao == "30":
            print()
            print(f"[SALDO] Saldo final: {formatar_moeda(conta['saldo'])}")
            print("Obrigado por usar o ByteBank. Até logo!")
            executando = False
        else:
            print()
            print("[ERRO] Opção inválida. Escolha uma opção entre 1 e 30.")


if __name__ == "__main__":
    main()
