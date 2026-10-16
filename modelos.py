"""
ByteBank - Modelos de domínio (Programação Orientada a Objetos)
===================================================
Disciplina: Algoritmo e Estrutura de Dados
Professor : Fernando Ferreira de Carvalho

Classes
---------------------------------------------------
Cliente        -> CPF, nome e contatos do titular.
ContaCorrente  -> id do cliente, saldo e limite (cheque especial).
CartaoCredito  -> nome, número, validade, CVV, limite, data de pagamento,
                  saldo da fatura, compras e parcelamento.

As regras de negócio ficam dentro dos métodos. Quando uma operação não é
permitida, o método levanta ValueError com a mensagem do motivo, e a camada
de interface (main.py) apenas exibe essa mensagem ao usuário.

Cada classe sabe se converter em dicionário (para_dict) e ser reconstruída
a partir de um (de_dict), porque a base de contas continua sendo gravada
em JSON, um registro por linha.
"""

import random
from datetime import date


def somente_digitos(texto):
    """Devolve apenas os dígitos de um texto (remove pontos, traços etc.)."""
    return "".join(caractere for caractere in str(texto) if caractere.isdigit())


def validar_valor(valor, operacao):
    """
    Garante que o valor de uma operação seja positivo.

    Devolve o valor arredondado em 2 casas ou levanta ValueError.
    """
    if valor <= 0:
        raise ValueError(f"Não é permitido {operacao} de valor negativo ou zerado.")
    return round(valor, 2)


# ---------------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------------
class Cliente:
    """Titular de uma conta do ByteBank."""

    TIPOS_CONTATO = ("Telefone", "E-mail")

    def __init__(self, cpf, nome, contatos=None):
        cpf = somente_digitos(cpf)
        nome = str(nome).strip()

        if cpf and len(cpf) != 11:
            raise ValueError("O CPF deve ter 11 dígitos.")
        if not nome:
            raise ValueError("O nome do cliente não pode ficar vazio.")

        self.cpf = cpf
        self.nome = nome
        self.contatos = [dict(contato) for contato in (contatos or [])]

    def adicionar_contato(self, tipo, valor):
        """
        Valida e adiciona um contato (telefone ou e-mail) ao cliente.

        Telefone: DDD + número, com 10 ou 11 dígitos.
        E-mail  : precisa ter usuário, '@' e domínio com ponto.
        """
        if tipo not in self.TIPOS_CONTATO:
            raise ValueError(f"Tipo de contato inválido: {tipo}.")

        valor = str(valor).strip()

        if tipo == "Telefone":
            valor = somente_digitos(valor)
            if len(valor) not in (10, 11):
                raise ValueError("O telefone deve ter DDD + número "
                                 "(10 ou 11 dígitos).")
        else:
            valor = valor.lower()
            usuario, arroba, dominio = valor.partition("@")
            if not usuario or not arroba or "." not in dominio or " " in valor:
                raise ValueError("E-mail inválido (ex.: nome@dominio.com).")

        contato = {"tipo": tipo, "valor": valor}
        if contato in self.contatos:
            raise ValueError("Este contato já está cadastrado.")

        self.contatos.append(contato)
        return contato

    def consultar_contatos(self, tipo=None):
        """
        Devolve uma cópia da lista de contatos do cliente.

        Com 'tipo' informado, devolve só os contatos daquele tipo.
        """
        return [
            dict(contato)
            for contato in self.contatos
            if tipo is None or contato["tipo"] == tipo
        ]

    @staticmethod
    def formatar_contato(contato):
        """Formata o contato para exibição (ex.: (81) 99999-1234)."""
        valor = contato["valor"]

        if contato["tipo"] == "Telefone":
            ddd, numero = valor[:2], valor[2:]
            return f"({ddd}) {numero[:-4]}-{numero[-4:]}"

        return valor

    def para_dict(self):
        return {"cpf": self.cpf, "nome": self.nome, "contatos": self.consultar_contatos()}

    @classmethod
    def de_dict(cls, dados):
        return cls(dados.get("cpf", ""), dados["nome"], dados.get("contatos", []))


# ---------------------------------------------------------------------------
# Conta corrente
# ---------------------------------------------------------------------------
class ContaCorrente:
    """
    Conta corrente com cheque especial.

    O 'limite' é o cheque especial: o saque pode deixar o saldo negativo
    até esse valor. Saldo disponível = saldo + limite.
    """

    LIMITE_PADRAO = 500.00
    LIMITE_MAXIMO = 5000.00

    def __init__(self, id_cliente, saldo=0.0, limite=LIMITE_PADRAO):
        if limite < 0:
            raise ValueError("O limite não pode ser negativo.")

        self.id_cliente = id_cliente
        self.saldo = round(float(saldo), 2)
        self.limite = round(float(limite), 2)

    def saldo_disponivel(self):
        """Quanto pode ser sacado: saldo + cheque especial."""
        return round(self.saldo + self.limite, 2)

    def em_cheque_especial(self):
        return self.saldo < 0

    def sacar(self, valor):
        """Debita o valor, permitindo usar o cheque especial."""
        valor = validar_valor(valor, "saque")

        if valor > self.saldo_disponivel():
            raise ValueError("Saldo insuficiente para realizar o saque, "
                             "mesmo usando o limite do cheque especial.")

        self.saldo = round(self.saldo - valor, 2)
        return self.saldo

    def depositar(self, valor):
        """Credita o valor no saldo."""
        valor = validar_valor(valor, "depósito")
        self.saldo = round(self.saldo + valor, 2)
        return self.saldo

    def consultar_saldo(self):
        return self.saldo

    def consultar_limite(self):
        return self.limite

    def aumentar_limite(self, valor):
        """Aumenta o cheque especial, respeitando o LIMITE_MAXIMO."""
        valor = validar_valor(valor, "aumento de limite")
        novo_limite = round(self.limite + valor, 2)

        if novo_limite > self.LIMITE_MAXIMO:
            raise ValueError("O novo limite ultrapassa o máximo permitido "
                             "para o cheque especial.")

        self.limite = novo_limite
        return self.limite

    def para_dict(self):
        return {"id_cliente": self.id_cliente, "saldo": self.saldo, "limite": self.limite}

    @classmethod
    def de_dict(cls, dados):
        return cls(
            dados.get("id_cliente", ""),
            dados.get("saldo", 0.0),
            dados.get("limite", cls.LIMITE_PADRAO),
        )


# ---------------------------------------------------------------------------
# Cartão de crédito
# ---------------------------------------------------------------------------
def digito_luhn(numero_parcial):
    """
    Calcula o dígito verificador pelo algoritmo de Luhn (usado pelas
    bandeiras de cartão para detectar erros de digitação).
    """
    soma = 0
    for posicao, digito in enumerate(reversed(numero_parcial)):
        valor = int(digito)
        if posicao % 2 == 0:
            valor = valor * 2
            if valor > 9:
                valor = valor - 9
        soma = soma + valor
    return str((10 - soma % 10) % 10)


def gerar_numero_cartao(numero_conta):
    """Gera um número de 16 dígitos ligado à conta, com dígito de Luhn."""
    parcial = "5309" + somente_digitos(numero_conta).zfill(11)[-11:]
    return parcial + digito_luhn(parcial)


class CartaoCredito:
    """
    Cartão de crédito vinculado à conta.

    saldo        -> valor da fatura atual (em aberto)
    compras      -> lançamentos da fatura atual
    parcelamento -> plano ativo de parcelamento da fatura (ou None)
    """

    LIMITE_PADRAO = 1500.00
    DIA_PAGAMENTO_PADRAO = 10
    ANOS_VALIDADE = 5
    TAXA_JUROS_PARCELAMENTO = 0.03     # 3% ao mês, juros simples
    PARCELAS_DISPONIVEIS = (2, 3, 6, 10, 12)

    def __init__(self, nome, numero, validade, cvv, limite=LIMITE_PADRAO,
                 data_pagamento=DIA_PAGAMENTO_PADRAO, saldo=0.0,
                 compras=None, parcelamento=None):
        if not 1 <= int(data_pagamento) <= 28:
            raise ValueError("O dia de pagamento deve estar entre 1 e 28.")

        self.nome = nome
        self.numero = numero
        self.validade = validade
        self.cvv = cvv
        self.limite = round(float(limite), 2)
        self.data_pagamento = int(data_pagamento)
        self.saldo = round(float(saldo), 2)
        self.compras = [dict(compra) for compra in (compras or [])]
        self.parcelamento = dict(parcelamento) if parcelamento else None

    @classmethod
    def emitir(cls, nome, numero_conta, limite=LIMITE_PADRAO):
        """Emite um cartão novo: número, validade de 5 anos e CVV aleatório."""
        hoje = date.today()
        validade = f"{hoje.month:02d}/{(hoje.year + cls.ANOS_VALIDADE) % 100:02d}"
        cvv = f"{random.randint(0, 999):03d}"
        return cls(str(nome).upper(), gerar_numero_cartao(numero_conta),
                   validade, cvv, limite)

    # ---- consultas -------------------------------------------------------
    def numero_mascarado(self):
        return f"**** **** **** {self.numero[-4:]}"

    def consultar_limite(self):
        return self.limite

    def consultar_saldo(self):
        return self.saldo

    def parcelas_restantes(self):
        """Parcelas ainda não lançadas em fatura."""
        if not self.parcelamento:
            return 0
        return self.parcelamento["parcelas"] - self.parcelamento["lancadas"]

    def saldo_parcelado(self):
        """Valor das parcelas futuras, que já comprometem o limite."""
        if not self.parcelamento:
            return 0.0
        return round(self.parcelas_restantes() * self.parcelamento["valor_parcela"], 2)

    def saldo_devedor(self):
        """Fatura atual + parcelas futuras."""
        return round(self.saldo + self.saldo_parcelado(), 2)

    def limite_disponivel(self):
        return round(self.limite - self.saldo_devedor(), 2)

    def proximo_vencimento(self):
        """Data do próximo pagamento da fatura (dd/mm/aaaa)."""
        hoje = date.today()

        if hoje.day <= self.data_pagamento:
            vencimento = date(hoje.year, hoje.month, self.data_pagamento)
        elif hoje.month == 12:
            vencimento = date(hoje.year + 1, 1, self.data_pagamento)
        else:
            vencimento = date(hoje.year, hoje.month + 1, self.data_pagamento)

        return vencimento.strftime("%d/%m/%Y")

    # ---- operações -------------------------------------------------------
    def comprar(self, valor, descricao, categoria):
        """Lança uma compra na fatura, respeitando o limite disponível."""
        valor = validar_valor(valor, "compra")

        if valor > self.limite_disponivel():
            raise ValueError("Limite de crédito insuficiente para esta compra.")

        self.compras.append(
            {"descricao": descricao, "valor": valor, "categoria": categoria}
        )
        self.saldo = round(self.saldo + valor, 2)

    def pagar(self, valor):
        """
        Abate o valor da fatura atual.

        Quando a fatura é quitada, as compras são liquidadas e, se houver
        parcelamento em andamento, a próxima parcela é lançada na nova
        fatura. Devolve True quando uma parcela foi lançada.
        """
        if self.saldo <= 0:
            raise ValueError("Não há fatura em aberto.")

        valor = validar_valor(valor, "pagamento")

        if valor > self.saldo:
            raise ValueError("O valor informado é maior que a fatura em aberto.")

        self.saldo = round(self.saldo - valor, 2)

        if self.saldo > 0:
            return False

        self.compras.clear()

        if self.parcelas_restantes() == 0:
            return False

        self.parcelamento["lancadas"] = self.parcelamento["lancadas"] + 1
        self._lancar_parcela()
        return True

    def simular_parcelamento(self, parcelas):
        """
        Calcula o parcelamento da fatura atual por juros simples
        (J = C * i * t), sem alterar o cartão.
        """
        if parcelas not in self.PARCELAS_DISPONIVEIS:
            raise ValueError("Quantidade de parcelas não disponível.")
        if self.saldo <= 0:
            raise ValueError("Não há saldo na fatura para parcelar.")

        juros = round(self.saldo * self.TAXA_JUROS_PARCELAMENTO * parcelas, 2)
        total = round(self.saldo + juros, 2)

        return {
            "principal": self.saldo,
            "juros": juros,
            "total": total,
            "parcelas": parcelas,
            "valor_parcela": round(total / parcelas, 2),
            "lancadas": 1,
        }

    def parcelar_saldo(self, parcelas):
        """
        Parcela a fatura atual: a 1ª parcela passa a ser a fatura e as
        demais são lançadas uma a uma, a cada fatura quitada.
        """
        if self.parcelas_restantes() > 0:
            raise ValueError("Já existe um parcelamento em andamento.")

        plano = self.simular_parcelamento(parcelas)

        if plano["total"] > self.limite:
            raise ValueError("Limite insuficiente para cobrir os juros "
                             "do parcelamento.")

        # A fatura atual é substituída pela 1ª parcela.
        self.parcelamento = plano
        self.saldo = 0.0
        self.compras.clear()
        self._lancar_parcela()
        return dict(plano)

    def _lancar_parcela(self):
        """Coloca a parcela atual do parcelamento na fatura."""
        plano = self.parcelamento
        self.saldo = round(self.saldo + plano["valor_parcela"], 2)
        self.compras.append({
            "descricao": f"Parcela {plano['lancadas']}/{plano['parcelas']} "
                         f"da fatura",
            "valor": plano["valor_parcela"],
            "categoria": "Outros",
        })

    # ---- conversão -------------------------------------------------------
    def para_dict(self):
        return {
            "nome": self.nome,
            "numero": self.numero,
            "validade": self.validade,
            "cvv": self.cvv,
            "limite": self.limite,
            "data_pagamento": self.data_pagamento,
            "saldo": self.saldo,
            "compras": [dict(compra) for compra in self.compras],
            "parcelamento": dict(self.parcelamento) if self.parcelamento else None,
        }

    @classmethod
    def de_dict(cls, dados):
        return cls(
            dados["nome"],
            dados["numero"],
            dados["validade"],
            dados["cvv"],
            dados.get("limite", cls.LIMITE_PADRAO),
            dados.get("data_pagamento", cls.DIA_PAGAMENTO_PADRAO),
            dados.get("saldo", 0.0),
            dados.get("compras", []),
            dados.get("parcelamento"),
        )
