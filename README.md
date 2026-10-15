# ByteBank

Sistema bancário FinTech desenvolvido em Python como projeto avaliativo (AV2) da disciplina
**Algoritmo e Estrutura de Dados** — CESAR School.
Professor: Fernando Ferreira de Carvalho.

O projeto é construído em **três sprints incrementais**, cada nível servindo de pré-requisito
para o próximo, e recebe por fim um **módulo de manipulação de arquivos**. Este repositório
documenta essa evolução no histórico de commits.

## Squad

Projeto individual.

- **Filipe Oliveira Nava** — fon2@cesar.school

## Estado atual: os três níveis concluídos + extras + manipulação de arquivos

O sistema entrega os Níveis 1, 2 e 3 da especificação, as seis funcionalidades do cardápio
de pontuação bônus e dois módulos de manipulação de arquivos:

- **Persistência TXT:** a base de contas é gravada em arquivo texto e restaurada
  automaticamente quando a aplicação é reiniciada.
- **Analisador de Log HTTP:** leitura de um arquivo de log de servidor web e contabilização
  das requisições com código 200 (Sucesso) e 404 (Não Encontrado).

Durante a execução, as operações acontecem em memória, por um menu interativo em loop
contínuo. A base só vai para o disco nos momentos descritos em
[Persistência TXT](#persistência-txt).

## Funcionalidades

### Nível 1 — Operações básicas e interface

| Opção | Funcionalidade | Descrição |
|-------|----------------|-----------|
| `[1]` | Consultar Saldo | Exibe o saldo disponível formatado em Real (R$). |
| `[2]` | Depositar | Credita um valor na conta. |
| `[3]` | Sacar | Debita um valor da conta, respeitando o limite por operação. |
| `[32]` | Sair | Grava a base de contas e encerra o sistema exibindo o saldo final. |

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

### Manipulação de arquivos

| Opção | Módulo | Descrição |
|-------|--------|-----------|
| `[30]` | Persistência TXT | Grava sob demanda a base de contas em `contas_bytebank.txt`. A restauração acontece sozinha ao iniciar. |
| `[31]` | Analisador de Log HTTP | Lê um log de servidor (padrão: `access.log`) e contabiliza as requisições 200 e 404, com percentuais. |

#### Persistência TXT

- `salvar_contas_txt(contas)` grava todas as contas em `contas_bytebank.txt`: uma linha de
  cabeçalho (comentário iniciado por `#`) e **um registro por linha**, em JSON.
- `carregar_contas_txt()` lê o arquivo ao iniciar o programa e reconstrói a lista de
  dicionários. Saldos, pilha de transações, fila de boletos, cofrinhos, cartão, moedas,
  BytePoints e empréstimos voltam exatamente como estavam.
- A base é gravada em três momentos: ao sair pela opção `[32]`, sob demanda pela opção `[30]`
  e quando a execução é interrompida (Ctrl+C ou fim da entrada).
- Na primeira execução o arquivo ainda não existe; o sistema cria a conta padrão `1001`.

#### Analisador de Log HTTP

- Lê o arquivo **linha a linha**, sem carregar o log inteiro na memória.
- Aceita o formato padrão dos servidores web (Common/Combined Log Format, usado por Apache e
  Nginx), em que o código de status é o número de 3 dígitos logo após a requisição entre aspas:

  ```
  192.168.0.10 - - [14/Oct/2026:09:00:01 -0300] "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0"
  ```

- Contabiliza os códigos 200 (Sucesso) e 404 (Não Encontrado) e informa também os demais
  códigos, as linhas fora do padrão e o total de linhas lidas.
- O repositório inclui um `access.log` de exemplo para teste.

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
- **Gravação segura:** a base é escrita primeiro em um arquivo temporário, que só depois
  substitui o original. Uma falha no meio da gravação não corrompe a base já salva.
- **Arquivo de base corrompido:** linhas inválidas ou com número de conta repetido são
  ignoradas com aviso, e as demais contas são carregadas normalmente.
- **Estorno após reiniciar:** o vínculo entre cada transação de empréstimo e o contrato
  correspondente é preservado no arquivo. Uma parcela paga antes de reiniciar o sistema
  continua estornável depois.
- **Log inexistente ou fora do padrão:** arquivo não encontrado gera mensagem de erro sem
  encerrar o programa; linhas que não seguem o formato são contadas à parte, sem distorcer
  os percentuais.

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
- **Persistência TXT:** `salvar_contas_txt`, `carregar_contas_txt`,
  `preparar_conta_para_gravacao`, `restaurar_conta`, `indice_do_emprestimo`, `salvar_base`,
  `iniciar_base`.
- **Analisador de Log HTTP:** `analisar_log_http`, `exibir_analise_log`, `percentual`.

O loop do menu fica em `executar_menu()`. A função `main()` restaura a base, executa o menu e,
ao final (por escolha do usuário ou por interrupção), chama `encerrar()`, que grava a base.

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
empréstimo, valor do ponto) e os nomes de arquivo (`ARQUIVO_CONTAS`, `ARQUIVO_LOG_PADRAO`)
estão isolados como constantes no topo do arquivo.

### Formato do arquivo de base

Cada linha de `contas_bytebank.txt` guarda um dicionário de conta completo (aqui abreviado):

```
# ByteBank - base de contas (um registro JSON por linha)
{"numero": "1001", "nome": "Cliente ByteBank", "cpf": "", "saldo": 1385.0, "historico": [...], ...}
{"numero": "1002", "nome": "Ana Souza", "cpf": "12345678900", "saldo": 100.0, "historico": [...], ...}
```

O registro por linha em JSON foi escolhido porque a conta tem estruturas aninhadas (pilha,
fila, cofrinhos, cartão), que um formato de colunas separadas por `;` não representaria sem
um formato próprio para cada uma.

Em memória, cada transação de empréstimo e a lista `emprestimos` apontam para o **mesmo**
dicionário. No arquivo não existe referência entre objetos. Por isso a transação grava apenas
a posição do contrato (`emprestimo_ref`), e o vínculo é refeito na leitura. Sem isso, após
reiniciar, o estorno de uma parcela alteraria uma cópia solta e não o contrato.

## Roadmap

- [x] **Sprint 1 — Nível 1 (Básico):** menu interativo, saldo, depósito, saque e validações.
- [x] **Sprint 2 — Nível 2 (Intermediário):** múltiplas contas em lista de dicionários,
      cadastro, busca e transferência PIX com verificação da chave de destino.
- [x] **Sprint 3 — Nível 3 (Avançado):** extrato como Pilha (LIFO) com estorno da última
      transação e Fila (FIFO) de pagamentos agendados.
- [x] **Funcionalidades extras:** cofrinhos, categorização de gastos, cartão de crédito,
      carteira multimoedas, BytePoints e empréstimos pré-aprovados.
- [x] **Manipulação de arquivos:** persistência da base de contas em TXT e analisador de
      log HTTP (códigos 200 e 404).

## Versionamento

A evolução do código está registrada no histórico de commits, um commit principal por etapa:

| Commit | Entrega |
|--------|---------|
| `feat: ... (Nivel 1)` | Menu interativo, saldo, depósito e saque com validações. |
| `feat: ... (Nivel 2)` | Lista de dicionários com múltiplas contas, cadastro, busca e PIX. |
| `feat: ... (Nivel 3)` | Extrato em Pilha (LIFO) com estorno via `pop()` e fila de boletos (FIFO) via `pop(0)`. |
| `feat: ... (bonus)` | Cofrinhos, categorização de gastos, cartão, multimoedas, BytePoints e empréstimos. |
| `feat: ... (arquivos)` | Persistência TXT da base de contas e analisador de log HTTP. |

Para acompanhar a evolução: `git log --oneline`.

## Estrutura do repositório

```
bytebank-aed-cesar/
├── main.py               # sistema completo
├── access.log            # log de servidor de exemplo para o analisador
└── README.md
```

O arquivo `contas_bytebank.txt` é gerado na primeira execução, na pasta de onde o programa é
executado. Por conter os dados de uso, convém mantê-lo fora do repositório (`.gitignore`).

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

Não há dependências externas: o projeto usa apenas a biblioteca padrão do Python
(`json`, `os`, `re` e `datetime`).

Na primeira execução, o sistema inicia com uma única conta (número `1001`, saldo zerado). Nas
execuções seguintes, restaura a base gravada em `contas_bytebank.txt`. O menu opera sempre
sobre a primeira conta da base. As contas criadas pela opção `[4]` servem como destino de PIX
e podem ser localizadas pela busca. Para testar o fluxo completo, comece por um depósito na
opção `[2]`.

Para começar do zero, basta apagar `contas_bytebank.txt` antes de executar.

## Exemplo de uso

Primeira execução, com depósito e saída:

```
[BASE] Nenhuma base salva encontrada. Iniciando nova base.

========================================================
                    === ByteBank ===
         Conta 1001 - Titular: Cliente ByteBank
========================================================

--------------------------------------------------------
[1]  Consultar Saldo
[2]  Depositar
[3]  Sacar
...
[30] Salvar Base de Contas (TXT)
[31] Analisar Log HTTP
[32] Sair
--------------------------------------------------------
> Digite a operação desejada: 2

>>> DEPÓSITO
Informe o valor do depósito: R$ 3000
[OK] Depósito de R$ 3.000,00 realizado com sucesso.
[SALDO] Novo saldo: R$ 3.000,00
...
> Digite a operação desejada: 32

[BASE] Base de contas gravada em 'contas_bytebank.txt'.
[SALDO] Saldo final: R$ 3.000,00
Obrigado por usar o ByteBank. Até logo!
```

Ao executar novamente, a base é restaurada:

```
[BASE] 1 conta(s) restaurada(s) de 'contas_bytebank.txt'.
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

Análise do `access.log` de exemplo (opção `[31]`, Enter para usar o arquivo padrão):

```
>>> ANALISADOR DE LOG HTTP
Arquivo de log [Enter = access.log]:
Arquivo analisado: access.log
--------------------------------------------------------
200 - Sucesso                        9     56,2%
404 - Não Encontrado                 4     25,0%
Demais códigos                       3     18,8%
--------------------------------------------------------
Requisições válidas                 16
Linhas fora do padrão                1
Total de linhas lidas               17
```
