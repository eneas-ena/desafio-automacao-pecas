# Sistema de Controle de Produção e Qualidade

**Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento**

Protótipo desenvolvido em Python para automatizar a inspeção de qualidade e o
armazenamento de peças em uma linha de montagem industrial.

- **Disciplina:** Algoritmos e Lógica de Programação
- **Curso:** Inteligência Artificial e Automação Digital — UniFECAF
- **Linguagem:** Python 3 (biblioteca padrão, sem dependências externas)

---

## 1. O problema

Em uma linha de montagem, a inspeção manual de peças gera três custos: atraso na
produção, falhas de conferência humana e aumento do custo operacional. O
conferente precisa medir cada peça, comparar mentalmente com a especificação,
anotar o resultado e ainda controlar o preenchimento das caixas de expedição.

Este sistema transfere essa rotina para o computador. O operador informa apenas
os dados brutos da peça; a decisão de aprovação, o registro do motivo da recusa,
o controle das caixas e a consolidação dos números passam a ser automáticos.

---

## 2. Como o sistema funciona

### 2.1 Critérios de qualidade

Uma peça só é aprovada se atender **simultaneamente** aos três critérios:

| Critério | Faixa aceita |
|---|---|
| Peso | entre 95 g e 105 g (inclusive) |
| Cor | azul **ou** verde |
| Comprimento | entre 10 cm e 20 cm (inclusive) |

Falhar em qualquer um deles reprova a peça. O sistema **não interrompe a
verificação no primeiro erro**: ele testa os três critérios e registra todos os
motivos de reprovação encontrados. Numa inspeção real, o operador precisa saber
tudo o que está errado na peça, e não apenas o primeiro defeito.

Esses limites estão declarados como constantes no início do arquivo. Se a
engenharia alterar o padrão de qualidade, basta mudar essas linhas — nenhuma
outra parte do programa precisa ser reescrita.

```python
PESO_MINIMO = 95.0
PESO_MAXIMO = 105.0
COMPRIMENTO_MINIMO = 10.0
COMPRIMENTO_MAXIMO = 20.0
CORES_ACEITAS = ["azul", "verde"]
CAPACIDADE_CAIXA = 10
```

### 2.2 Armazenamento em caixas

Toda peça aprovada é encaminhada para a caixa em uso. Quando a caixa atinge
**10 peças**, ela é considerada fechada (lacrada) e uma nova caixa é aberta
automaticamente no cadastro seguinte. Peças reprovadas nunca entram em caixas.

Ao remover uma peça aprovada, o sistema **reconstrói todas as caixas** a partir
da lista atualizada. Isso evita que uma caixa fique com um espaço vazio no meio
enquanto outras já foram abertas — o lote permanece sempre compactado.

### 2.3 Estruturas de dados

| Estrutura | Tipo | Conteúdo |
|---|---|---|
| `pecas_aprovadas` | lista de dicionários | id, peso, cor, comprimento |
| `pecas_reprovadas` | lista de dicionários | os mesmos campos + lista de motivos |
| `caixas` | lista de listas | cada caixa guarda os IDs das peças nela |

### 2.4 Organização do código

O programa é dividido em funções de responsabilidade única:

| Função | Responsabilidade |
|---|---|
| `ler_texto` / `ler_numero` | Validam o que o operador digita e insistem até receber um valor aceitável |
| `id_ja_existe` | Impede o cadastro de dois IDs iguais |
| `avaliar_peca` | Aplica os três critérios e devolve a lista de motivos de reprovação |
| `armazenar_em_caixa` | Coloca a peça na caixa atual, abrindo uma nova se necessário |
| `reorganizar_caixas` | Recompacta o lote após uma remoção |
| `total_caixas_fechadas` | Conta as caixas que atingiram a capacidade máxima |
| `cadastrar_peca` | Opção 1 do menu |
| `listar_pecas` | Opção 2 do menu |
| `remover_peca` | Opção 3 do menu |
| `listar_caixas` | Opção 4 do menu |
| `gerar_relatorio` | Opção 5 do menu |
| `carregar_demonstracao` | Opção 6 — popula o sistema com um lote de teste |
| `main` | Laço principal que mantém o menu em execução |

---

## 3. Como rodar o programa

### Pré-requisito

Python 3 instalado. Para verificar, abra o terminal e digite:

```bash
python3 --version
```

Se aparecer algo como `Python 3.12.0`, está pronto. Caso contrário, instale a
partir de [python.org/downloads](https://www.python.org/downloads/).

### Passo a passo

**1. Obtenha o arquivo**

Baixe o repositório (botão *Code > Download ZIP* no GitHub e descompacte), ou
clone via terminal:

```bash
git clone https://github.com/eneas-ena/desafio-automacao-pecas.git
```

**2. Entre na pasta do projeto**

```bash
cd desafio-automacao-pecas
```

**3. Execute**

```bash
python3 sistema_pecas.py
```

No Windows, o comando costuma ser `python sistema_pecas.py`.

**Alternativa pelo VS Code:** abra a pasta em *File > Open Folder*, clique no
arquivo `sistema_pecas.py` e pressione o botão ▶ (Run Python File) no canto
superior direito.

### Primeira execução recomendada

Escolha a **opção 6 (Carregar lote de demonstração)**. Ela processa 16 peças de
uma vez — 12 aprovadas e 4 reprovadas — o suficiente para lacrar uma caixa,
abrir a segunda e produzir os quatro tipos de reprovação. Em seguida, escolha a
opção 5 para ver o relatório completo.

---

## 4. Exemplos de entradas e saídas

### Menu principal

```
==============================================================
   SISTEMA DE CONTROLE DE PRODUÇÃO E QUALIDADE
   Automação Digital — Linha de Montagem
==============================================================
   Aprovadas: 12   Reprovadas: 4    Caixas: 2
--------------------------------------------------------------
   1 - Cadastrar nova peça
   2 - Listar peças aprovadas/reprovadas
   3 - Remover peça cadastrada
   4 - Listar caixas fechadas
   5 - Gerar relatório final
   6 - Carregar lote de demonstração
   0 - Sair do sistema
==============================================================
   Selecione uma opção:
```

O cabeçalho exibe os totais atualizados a cada operação, funcionando como um
painel de acompanhamento da produção.

### Exemplo 1 — Peça aprovada

**Entrada:**

```
   ID da peça............: PC-001
   Peso (g)...............: 98.5
   Cor....................: azul
   Comprimento (cm).......: 15.2
```

**Saída:**

```
   >>> RESULTADO: PEÇA APROVADA <<<
   Armazenada na CAIXA 1 (1/10 peças).
```

### Exemplo 2 — Peça reprovada por dois critérios

**Entrada:**

```
   ID da peça............: PC-002
   Peso (g)...............: 112
   Cor....................: vermelho
   Comprimento (cm).......: 15
```

**Saída:**

```
   >>> RESULTADO: PEÇA REPROVADA <<<
   Motivo(s):
     - PESO: 112.0g fora da faixa (95g a 105g)
     - COR: 'vermelho' não permitida (aceitas: azul, verde)
```

O comprimento estava correto e por isso não aparece na lista.

### Exemplo 3 — Fechamento automático de caixa

Ao cadastrar a décima peça aprovada:

```
   >>> RESULTADO: PEÇA APROVADA <<<
   Armazenada na CAIXA 1 (10/10 peças).
   [*] CAIXA 1 FECHADA — capacidade máxima atingida.
   [*] Uma nova caixa será aberta no próximo cadastro.
```

### Exemplo 4 — Validação de entrada inválida

Se o operador digitar um texto no campo de peso:

```
   Peso (g)...............: abc
   [!] Valor inválido. Use apenas números (ex.: 98.5).
   Peso (g)...............:
```

O programa não trava nem encerra: repete a pergunta até receber um número
válido. O mesmo vale para campos deixados em branco.

### Exemplo 5 — Listagem de caixas (opção 4)

```
   ---------- CAIXAS FECHADAS (1) ----------

   CAIXA 1 — LACRADA (10/10)
   Peças: PC-001, PC-002, PC-003, PC-005, PC-007, PC-008, PC-010, PC-011, PC-012, PC-014

   ---------- CAIXA EM USO ----------
   CAIXA 2 — ABERTA (2/10)
   Peças: PC-015, PC-016
```

### Exemplo 6 — Relatório final (opção 5)

```
==============================================================
 5) RELATÓRIO CONSOLIDADO DE PRODUÇÃO
==============================================================

   PRODUÇÃO TOTAL ANALISADA .......: 16 peça(s)
   Peças APROVADAS ................: 12 (75.0%)
   Peças REPROVADAS ...............: 4 (25.0%)

   --- MOTIVOS DE REPROVAÇÃO (por critério) ---
   PESO           : 2 ocorrência(s)
   COR            : 2 ocorrência(s)
   COMPRIMENTO    : 2 ocorrência(s)

   --- DETALHAMENTO POR PEÇA ---
   [PC-004]
      - PESO: 120.0g fora da faixa (95g a 105g)
   [PC-006]
      - COR: 'vermelho' não permitida (aceitas: azul, verde)
   [PC-009]
      - COMPRIMENTO: 25.0cm fora da faixa (10cm a 20cm)
   [PC-013]
      - PESO: 80.0g fora da faixa (95g a 105g)
      - COR: 'preto' não permitida (aceitas: azul, verde)
      - COMPRIMENTO: 5.0cm fora da faixa (10cm a 20cm)

   --- ARMAZENAMENTO ---
   Caixas utilizadas ..............: 2
   Caixas fechadas (lacradas) .....: 1
   Caixa em uso ...................: CAIXA 2 com 2/10 peça(s)
   Espaço livre na caixa atual ....: 8 vaga(s)

==============================================================
 FIM DO RELATÓRIO
==============================================================
```

O relatório traz dois níveis de leitura: a **contagem por critério**, que aponta
onde o processo produtivo está falhando com mais frequência, e o
**detalhamento por peça**, para rastreabilidade individual.

### Exemplo 7 — Remoção de peça (opção 3)

```
   Digite o ID da peça a remover: PC-001

   [OK] Peça 'PC-001' removida das APROVADAS.
   [*] As caixas foram reorganizadas automaticamente.
```

---

## 5. Boas práticas aplicadas

- **Constantes nomeadas** para as regras de negócio, em vez de números soltos
  espalhados pelo código.
- **Funções de responsabilidade única**, cada uma resolvendo um problema
  específico.
- **Separação entre lógica e interface**: `avaliar_peca` e `armazenar_em_caixa`
  não imprimem nada na tela; apenas calculam e devolvem resultados. Isso permite
  reaproveitá-las em uma futura versão web ou com sensores, sem alteração.
- **Validação defensiva de entrada**, impedindo que o programa quebre com dados
  malformados.
- **Prevenção de IDs duplicados**, garantindo a integridade do cadastro.
- **Comentários e docstrings** explicando a intenção de cada bloco.

---

## 6. Limitações conhecidas

Os dados são mantidos em memória durante a execução. Ao encerrar o programa, o
cadastro é perdido. A persistência em arquivo ou banco de dados é o passo
natural seguinte, discutido na parte teórica do trabalho.

---

## 7. Estrutura do repositório

```
.
├── sistema_pecas.py    # Código-fonte do sistema
└── README.md           # Este arquivo
```
