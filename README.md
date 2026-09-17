# ByteBank

Sistema bancário FinTech desenvolvido em Python como projeto avaliativo (AV2) da disciplina
**Algoritmo e Estrutura de Dados** — CESAR School.
Professor: Fernando Ferreira de Carvalho.

O projeto é construído em **três sprints incrementais**, cada nível servindo de pré-requisito
para o próximo. Este repositório documenta essa evolução no histórico de commits.

## Squad

Projeto individual.

- **Filipe Oliveira Nava** — fon2@cesar.school

## Estado atual: os três níveis concluídos + funcionalidades extras

O sistema entrega os Níveis 1, 2 e 3 da especificação e as seis funcionalidades do cardápio
de pontuação bônus. Tudo roda em memória, operado por um menu interativo em loop contínuo.

## Funcionalidades

### Nível 1 — Operações básicas e interface

| Opção | Funcionalidade | Descrição |
|-------|----------------|-----------|
| `[1]` | Consultar Saldo | Exibe o saldo disponível formatado em Real (R$). |
| `[2]` | Depositar | Credita um valor na conta. |
| `[3]` | Sacar | Debita um valor da conta, respeitando o limite por operação. |
| `[30]` | Sair | Encerra o sistema exibindo o saldo final. |

### Nível 2 — Múltiplas contas e transferência PIX

| Opção | Funcionalidade | Descrição |
|-------|----------------|-----------|
| `[4]` | Cadastrar Conta | Registra nome, CPF e gera um número de conta único. |
| `[5]` | Buscar Conta | Varre a coleção em memória e localiza a conta pelo número ou pelo CPF. |
| `[6]` | Transferir via PIX | Debita a origem e credita o destino após validar a chave e o saldo. |

### Nível 3 — Estruturas de dados avançadas

| Opção | Funcionalidade | Estrutura |
|-------|----------------|-----------|
| `[7]` | Exibir Extrato | **Pilha (LIFO)** — lida do topo para a base. |
| `[8]` | Estornar Última Transação | **Pilha (LIFO)** — `pop()` no topo e reversão do movimento. |
| `[9]` | Agendar Boleto | **Fila (FIFO)** — `append()` no fim da fila. |
| `[10]` | Pagar Próximo Boleto | **Fila (FIFO)** — `pop(0)` no início da fila. |
| `[11]` | Consultar Fila de Boletos | Exibe a fila na ordem de processamento. |

### Funcionalidades extras (pontuação bônus)

| Opções | Módulo | Descrição |
|--------|--------|-----------|
| `[12]`–`[16]` | Cofrinhos / Caixinhas | Subcontas de investimento com operações de guardar e resgatar, e rendimento simulado por juros simples (`J = C · i · t`). |
| `[17]` | Categorização e analytics | Classifica cada gasto em uma categoria e gera o relatório com os somatórios acumulados (agrupamento em memória). |
| `[18]`–`[20]` | Cartão de crédito | Limite aprovado, compras na modalidade crédito e pagamento da fatura com o saldo corrente. |
| `[21]`–`[23]` | Carteira multimoedas | Saldos em USD, EUR e BTC convertidos por uma tabela de taxas de câmbio. |
| `[24]`–`[25]` | BytePoints | Acúmulo automático de pontos em saques e transferências, resgatáveis como cashback em saldo. |
| `[26]`–`[29]` | Empréstimos pré-aprovados | Simulação e contratação com base no saldo atual, creditando o valor e gerando o parcelamento passivo. |

## Regras de negócio implementadas

- **Saldo insuficiente:** saques, PIX, boletos e pagamentos maiores que o saldo disponível
  são recusados, e o saldo permanece inalterado.
- **Valores negativos:** depósitos, saques e demais operações de valor negativo ou zerado
  são bloqueados.
- **Entradas inválidas:** texto não numérico nos valores e opções fora do menu são tratados
  com mensagem de erro, sem interromper a execução do programa.
- **Limite por operação:** o saque é recusado acima do limite configurado em `LIMITE_SAQUE`.
- **PIX atômico:** o débito na origem e o crédito no destino só acontecem depois que a chave
  de destino e o saldo são validados — não existe dinheiro em trânsito.
- **Boleto sem saldo:** o pagamento é recusado e o boleto permanece na primeira posição da
  fila, aguardando novo saldo.
- **Estorno consistente:** o estorno é recusado quando a reversão deixaria o sistema
  inconsistente — por exemplo, um PIX cujo destinatário já gastou o valor recebido, ou um
  empréstimo com parcelas já pagas. Ao ser aceito, o estorno desfaz também os efeitos
  colaterais: devolve o valor ao remetente, recompõe a fatura do cartão, devolve o boleto ao
  início da fila e retira os pontos que haviam sido creditados.

## Organização do código

O `main.py` está modularizado em funções (`def` / `return`), separadas em camadas:

- **Apresentação:** `exibir_cabecalho`, `exibir_menu`, `formatar_moeda`,
  `formatar_moeda_estrangeira`, `linha`, `titulo`.
- **Entrada e validação:** `ler_opcao`, `ler_texto`, `ler_valor`, `ler_quantidade`,
  `ler_inteiro`, `escolher_da_lista`.
- **Coleção de contas (Nível 2):** `criar_conta`, `gerar_numero_conta`, `buscar_conta`,
  `cadastrar_conta`, `consultar_conta`.
- **Pilha e estorno (Nível 3):** `registrar_transacao`, `exibir_extrato`, `validar_estorno`,
  `aplicar_reversao`, `estornar_ultima_transacao`.
- **Operações financeiras:** `consultar_saldo`, `depositar`, `sacar`, `transferir_pix`,
  `agendar_boleto`, `pagar_proximo_boleto`, `consultar_fila`.
- **Funcionalidades extras:** um bloco de funções por módulo (cofrinhos, relatório, cartão,
  câmbio, BytePoints e empréstimos).

O loop principal fica isolado em `main()`.

### Estruturas de dados

As contas são armazenadas em uma **lista de dicionários**. Cada conta carrega as próprias
estruturas:

```python
{
    "numero": "1001",
    "nome": "Cliente ByteBank",
    "cpf": "",
    "saldo": 0.0,
    "historico": [],        # PILHA (LIFO) de transações
    "fila_boletos": [],     # FILA  (FIFO) de boletos agendados
    "cofrinhos": {},        # subcontas de investimento
    "cartao": {...},        # limite, fatura e compras
    "moedas": {...},        # saldos em USD, EUR e BTC
    "pontos": 0,            # BytePoints acumulados
    "emprestimos": [],      # contratos e parcelamento
}
```

Os parâmetros de negócio (limite de saque, taxas de câmbio, juros do cofrinho e do
empréstimo, valor do ponto) estão isolados como constantes no topo do arquivo.

## Roadmap

- [x] **Sprint 1 — Nível 1 (Básico):** menu interativo, saldo, depósito, saque e validações.
- [x] **Sprint 2 — Nível 2 (Intermediário):** múltiplas contas em lista de dicionários,
      cadastro, busca e transferência PIX com verificação da chave de destino.
- [x] **Sprint 3 — Nível 3 (Avançado):** extrato como Pilha (LIFO) com estorno da última
      transação e Fila (FIFO) de pagamentos agendados.
- [x] **Funcionalidades extras:** cofrinhos, categorização de gastos, cartão de crédito,
      carteira multimoedas, BytePoints e empréstimos pré-aprovados.

## Como executar

Pré-requisito: **Python 3.10 ou superior** instalado.

```bash
git clone https://github.com/RedAkasha/bytebank-aed-cesar.git
cd bytebank-aed-cesar
python main.py
```

No Windows, caso o comando `python` não seja reconhecido, use:

```bash
py main.py
```

Não há dependências externas: o projeto usa apenas a biblioteca padrão do Python.

O sistema inicia com uma única conta (número `1001`, saldo zerado) e opera sempre sobre ela.
As contas criadas pela opção `[4]` servem como destino de PIX e podem ser localizadas pela
busca. Para testar o fluxo completo, comece por um depósito na opção `[2]`.

## Exemplo de uso

```
========================================================
                    === ByteBank ===
         Conta 1001 - Titular: Cliente ByteBank
========================================================

--------------------------------------------------------
[1]  Consultar Saldo
[2]  Depositar
[3]  Sacar
...
[30] Sair
--------------------------------------------------------
> Digite a operação desejada: 2

>>> DEPÓSITO
Informe o valor do depósito: R$ 3000
[OK] Depósito de R$ 3.000,00 realizado com sucesso.
[SALDO] Novo saldo: R$ 3.000,00
```

Extrato como pilha, após alguns movimentos:

```
>>> EXTRATO
Leitura da pilha: do topo (mais recente) para a base.
--------------------------------------------------------
  4. 17/09/2026 20:48 BOLETO PAGO             -R$ 150,00
     Pagamento de boleto: Conta de luz
  3. 17/09/2026 20:48 PIX ENVIADO             -R$ 300,00
     PIX para Maria (conta 1002)
  2. 17/09/2026 20:48 SAQUE                   -R$ 200,00
     Saque em conta
  1. 17/09/2026 20:48 DEPÓSITO              +R$ 3.000,00
     Depósito em conta
--------------------------------------------------------
Transações empilhadas: 4
Saldo atual          : R$ 2.350,00
```

Estorno desempilhando o topo (LIFO) e devolvendo o boleto para a fila:

```
>>> ESTORNO DA ÚLTIMA TRANSAÇÃO
Topo da pilha: BOLETO PAGO de R$ 150,00
Registrada em: 17/09/2026 20:48
[OK] Transação 'BOLETO PAGO' estornada com sucesso.
[SALDO] Novo saldo: R$ 2.500,00
```
