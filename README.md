# ByteBank

Sistema bancário FinTech desenvolvido em Python como projeto avaliativo (AV2) da disciplina
**BD015 - Algoritmo e Estrutura de Dados** — CESAR School.
Professor: Fernando Ferreira de Carvalho.

O projeto é construído em **três sprints incrementais**, cada nível servindo de pré-requisito
para o próximo. Este repositório documenta essa evolução no histórico de commits.

## Squad

Projeto individual.

- **Filipe Oliveira Nava** — fon2@cesar.school

## Estado atual: Sprint 1 — Nível 1 (MVP)

O sistema já entrega o **Produto Mínimo Viável**: uma conta em memória operada por um menu
interativo em loop contínuo.

### Funcionalidades

| Opção | Funcionalidade | Descrição |
|-------|----------------|-----------|
| `[1]` | Consultar Saldo | Exibe o saldo disponível formatado em Real (R$ 1.234,56). |
| `[2]` | Depositar | Credita um valor na conta. |
| `[3]` | Sacar | Debita um valor da conta. |
| `[4]` | Sair | Encerra o sistema exibindo o saldo final. |

### Regras de negócio implementadas

- **Saldo insuficiente:** saques maiores que o saldo disponível são recusados, e o saldo
  permanece inalterado.
- **Valores negativos:** depósitos e saques de valor negativo ou zerado são bloqueados.
- **Entradas inválidas:** texto não numérico no valor da operação e opções fora do menu
  são tratados com mensagem de erro, sem interromper a execução do programa.

### Organização do código

O `main.py` está modularizado em funções (`def` / `return`), separando responsabilidades em
três camadas: apresentação (`exibir_cabecalho`, `exibir_menu`, `formatar_moeda`), entrada e
validação (`ler_opcao`, `ler_valor`) e operações financeiras (`consultar_saldo`, `depositar`,
`sacar`). O loop principal fica isolado em `main()`.

## Roadmap

- [x] **Sprint 1 — Nível 1 (Básico):** menu interativo, saldo, depósito, saque e validações.
- [ ] **Sprint 2 — Nível 2 (Intermediário):** múltiplas contas em matriz/lista de dicionários
      e transferência PIX com verificação da chave de destino.
- [ ] **Sprint 3 — Nível 3 (Avançado):** extrato como Pilha (LIFO) com estorno da última
      transação e Fila (FIFO) de pagamentos agendados.

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

## Exemplo de uso

```
==========================================
           === ByteBank MVP ===
        Titular: Cliente ByteBank
==========================================

------------------------------------------
[1] Consultar Saldo
[2] Depositar
[3] Sacar
[4] Sair
------------------------------------------
> Digite a operação desejada: 2

>>> DEPÓSITO
Informe o valor do depósito: R$ 500,50
[OK] Depósito de R$ 500,50 realizado com sucesso.
[SALDO] Novo saldo: R$ 500,50
```
