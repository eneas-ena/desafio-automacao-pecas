# -*- coding: utf-8 -*-
"""
============================================================================
 DESAFIO DE AUTOMAÇÃO DIGITAL
 Gestão de Peças, Qualidade e Armazenamento
============================================================================
 Disciplina : Algoritmos e Lógica de Programação
 Linguagem  : Python 3
 Descrição  : Protótipo de sistema de controle de produção e qualidade
              para linha de montagem industrial. O sistema recebe os dados
              de cada peça, avalia automaticamente sua conformidade,
              armazena as peças aprovadas em caixas de capacidade limitada
              e gera relatórios consolidados.
============================================================================
"""

# ===========================================================================
# 1. PARÂMETROS DE QUALIDADE
# ---------------------------------------------------------------------------
# As regras de negócio ficam centralizadas em constantes. Se a engenharia
# mudar um critério, basta alterar aqui — nenhuma outra parte do código
# precisa ser reescrita.
# ===========================================================================

PESO_MINIMO = 95.0            # gramas
PESO_MAXIMO = 105.0           # gramas
COMPRIMENTO_MINIMO = 10.0     # centímetros
COMPRIMENTO_MAXIMO = 20.0     # centímetros
CORES_ACEITAS = ["azul", "verde"]
CAPACIDADE_CAIXA = 10         # peças por caixa


# ===========================================================================
# 2. ESTRUTURAS DE DADOS
# ---------------------------------------------------------------------------
# pecas_aprovadas / pecas_reprovadas : listas de dicionários (cada peça)
# caixas                             : lista de listas (cada caixa guarda
#                                      os IDs das peças que estão nela)
# ===========================================================================

pecas_aprovadas = []
pecas_reprovadas = []
caixas = []


# ===========================================================================
# 3. FUNÇÕES AUXILIARES DE ENTRADA (validação do que o operador digita)
# ===========================================================================

def ler_texto(rotulo):
    """Lê um texto obrigatório do teclado. Repete até receber algo válido."""
    while True:
        valor = input(rotulo).strip()
        if valor != "":
            return valor
        print("   [!] Campo obrigatório. Digite um valor.")


def ler_numero(rotulo):
    """Lê um número real do teclado. Aceita vírgula ou ponto decimal."""
    while True:
        entrada = input(rotulo).strip().replace(",", ".")
        try:
            return float(entrada)
        except ValueError:
            print("   [!] Valor inválido. Use apenas números (ex.: 98.5).")


def id_ja_existe(id_peca):
    """Verifica se um ID já foi cadastrado (aprovado ou reprovado)."""
    for peca in pecas_aprovadas + pecas_reprovadas:
        if peca["id"].lower() == id_peca.lower():
            return True
    return False


def pausar():
    """Segura a tela até o operador pressionar ENTER."""
    input("\n   Pressione ENTER para voltar ao menu...")


def cabecalho(titulo):
    """Imprime um cabeçalho padronizado de seção."""
    print("\n" + "=" * 62)
    print(f" {titulo}")
    print("=" * 62)


# ===========================================================================
# 4. NÚCLEO LÓGICO — AVALIAÇÃO DE QUALIDADE
# ===========================================================================

def avaliar_peca(peca):
    """
    Aplica os três critérios de qualidade a uma peça.

    Retorna uma LISTA de motivos de reprovação.
    Lista vazia  -> peça APROVADA
    Lista com N  -> peça REPROVADA (pode falhar em mais de um critério)
    """
    motivos = []

    if not (PESO_MINIMO <= peca["peso"] <= PESO_MAXIMO):
        motivos.append(
            f"PESO: {peca['peso']:.1f}g fora da faixa "
            f"({PESO_MINIMO:.0f}g a {PESO_MAXIMO:.0f}g)"
        )

    if peca["cor"] not in CORES_ACEITAS:
        motivos.append(
            f"COR: '{peca['cor']}' não permitida "
            f"(aceitas: {', '.join(CORES_ACEITAS)})"
        )

    if not (COMPRIMENTO_MINIMO <= peca["comprimento"] <= COMPRIMENTO_MAXIMO):
        motivos.append(
            f"COMPRIMENTO: {peca['comprimento']:.1f}cm fora da faixa "
            f"({COMPRIMENTO_MINIMO:.0f}cm a {COMPRIMENTO_MAXIMO:.0f}cm)"
        )

    return motivos


# ===========================================================================
# 5. NÚCLEO LÓGICO — ARMAZENAMENTO EM CAIXAS
# ===========================================================================

def armazenar_em_caixa(peca):
    """
    Coloca a peça aprovada na caixa atual.
    Se não existe caixa aberta ou a última já atingiu a capacidade,
    fecha a caixa e abre uma nova.

    Retorna o número da caixa onde a peça foi guardada.
    """
    if len(caixas) == 0 or len(caixas[-1]) >= CAPACIDADE_CAIXA:
        caixas.append([])          # abre uma nova caixa

    caixas[-1].append(peca["id"])
    return len(caixas)             # número da caixa (1, 2, 3...)


def reorganizar_caixas():
    """
    Reconstrói todas as caixas a partir da lista de peças aprovadas.
    Necessário após remover uma peça, para não deixar caixas com buracos.
    """
    caixas.clear()
    for peca in pecas_aprovadas:
        armazenar_em_caixa(peca)


def total_caixas_fechadas():
    """Conta quantas caixas já atingiram a capacidade máxima."""
    fechadas = 0
    for caixa in caixas:
        if len(caixa) >= CAPACIDADE_CAIXA:
            fechadas += 1
    return fechadas


# ===========================================================================
# 6. OPÇÃO 1 — CADASTRAR NOVA PEÇA
# ===========================================================================

def cadastrar_peca():
    cabecalho("1) CADASTRAR NOVA PEÇA")

    id_peca = ler_texto("   ID da peça............: ")
    if id_ja_existe(id_peca):
        print(f"\n   [X] O ID '{id_peca}' já está cadastrado. Operação cancelada.")
        pausar()
        return

    peso = ler_numero("   Peso (g)...............: ")
    cor = ler_texto("   Cor....................: ").lower()
    comprimento = ler_numero("   Comprimento (cm).......: ")

    peca = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento
    }

    motivos = avaliar_peca(peca)

    if len(motivos) == 0:
        peca["motivos"] = []
        pecas_aprovadas.append(peca)
        numero_caixa = armazenar_em_caixa(peca)
        ocupacao = len(caixas[numero_caixa - 1])

        print("\n   >>> RESULTADO: PEÇA APROVADA <<<")
        print(f"   Armazenada na CAIXA {numero_caixa} "
              f"({ocupacao}/{CAPACIDADE_CAIXA} peças).")

        if ocupacao == CAPACIDADE_CAIXA:
            print(f"   [*] CAIXA {numero_caixa} FECHADA — capacidade máxima atingida.")
            print("   [*] Uma nova caixa será aberta no próximo cadastro.")
    else:
        peca["motivos"] = motivos
        pecas_reprovadas.append(peca)

        print("\n   >>> RESULTADO: PEÇA REPROVADA <<<")
        print("   Motivo(s):")
        for motivo in motivos:
            print(f"     - {motivo}")

    pausar()


# ===========================================================================
# 7. OPÇÃO 2 — LISTAR PEÇAS APROVADAS / REPROVADAS
# ===========================================================================

def listar_pecas():
    cabecalho("2) LISTAGEM DE PEÇAS")
    print("   [1] Peças aprovadas")
    print("   [2] Peças reprovadas")
    print("   [3] Todas")
    opcao = input("\n   Escolha: ").strip()

    if opcao in ("1", "3"):
        print("\n   ---------- PEÇAS APROVADAS ----------")
        if len(pecas_aprovadas) == 0:
            print("   Nenhuma peça aprovada até o momento.")
        else:
            print(f"   {'ID':<12}{'PESO(g)':>10}{'COR':>10}{'COMPR.(cm)':>14}")
            print("   " + "-" * 46)
            for peca in pecas_aprovadas:
                print(f"   {peca['id']:<12}{peca['peso']:>10.1f}"
                      f"{peca['cor']:>10}{peca['comprimento']:>14.1f}")
            print(f"\n   Total: {len(pecas_aprovadas)} peça(s).")

    if opcao in ("2", "3"):
        print("\n   ---------- PEÇAS REPROVADAS ----------")
        if len(pecas_reprovadas) == 0:
            print("   Nenhuma peça reprovada até o momento.")
        else:
            for peca in pecas_reprovadas:
                print(f"\n   ID: {peca['id']}  |  {peca['peso']:.1f}g  |  "
                      f"{peca['cor']}  |  {peca['comprimento']:.1f}cm")
                for motivo in peca["motivos"]:
                    print(f"      - {motivo}")
            print(f"\n   Total: {len(pecas_reprovadas)} peça(s).")

    if opcao not in ("1", "2", "3"):
        print("\n   [!] Opção inválida.")

    pausar()


# ===========================================================================
# 8. OPÇÃO 3 — REMOVER PEÇA CADASTRADA
# ===========================================================================

def remover_peca():
    cabecalho("3) REMOVER PEÇA CADASTRADA")

    if len(pecas_aprovadas) == 0 and len(pecas_reprovadas) == 0:
        print("   Não há peças cadastradas para remover.")
        pausar()
        return

    id_peca = ler_texto("   Digite o ID da peça a remover: ")

    # Procura entre as aprovadas
    for peca in pecas_aprovadas:
        if peca["id"].lower() == id_peca.lower():
            pecas_aprovadas.remove(peca)
            reorganizar_caixas()   # recompacta as caixas
            print(f"\n   [OK] Peça '{peca['id']}' removida das APROVADAS.")
            print("   [*] As caixas foram reorganizadas automaticamente.")
            pausar()
            return

    # Procura entre as reprovadas
    for peca in pecas_reprovadas:
        if peca["id"].lower() == id_peca.lower():
            pecas_reprovadas.remove(peca)
            print(f"\n   [OK] Peça '{peca['id']}' removida das REPROVADAS.")
            pausar()
            return

    print(f"\n   [X] Nenhuma peça encontrada com o ID '{id_peca}'.")
    pausar()


# ===========================================================================
# 9. OPÇÃO 4 — LISTAR CAIXAS FECHADAS
# ===========================================================================

def listar_caixas():
    cabecalho("4) CAIXAS")

    if len(caixas) == 0:
        print("   Nenhuma caixa foi aberta ainda.")
        pausar()
        return

    fechadas = total_caixas_fechadas()

    print(f"\n   ---------- CAIXAS FECHADAS ({fechadas}) ----------")
    if fechadas == 0:
        print("   Nenhuma caixa atingiu a capacidade máxima ainda.")
    else:
        for indice, caixa in enumerate(caixas, start=1):
            if len(caixa) >= CAPACIDADE_CAIXA:
                print(f"\n   CAIXA {indice} — LACRADA "
                      f"({len(caixa)}/{CAPACIDADE_CAIXA})")
                print(f"   Peças: {', '.join(caixa)}")

    # Mostra também a caixa em uso, se houver
    if len(caixas[-1]) < CAPACIDADE_CAIXA:
        print(f"\n   ---------- CAIXA EM USO ----------")
        print(f"   CAIXA {len(caixas)} — ABERTA "
              f"({len(caixas[-1])}/{CAPACIDADE_CAIXA})")
        print(f"   Peças: {', '.join(caixas[-1])}")

    pausar()


# ===========================================================================
# 10. OPÇÃO 5 — GERAR RELATÓRIO FINAL
# ===========================================================================

def gerar_relatorio():
    cabecalho("5) RELATÓRIO CONSOLIDADO DE PRODUÇÃO")

    total_aprovadas = len(pecas_aprovadas)
    total_reprovadas = len(pecas_reprovadas)
    total_geral = total_aprovadas + total_reprovadas

    if total_geral == 0:
        print("   Nenhuma peça processada. Relatório indisponível.")
        pausar()
        return

    taxa_aprovacao = (total_aprovadas / total_geral) * 100
    taxa_reprovacao = (total_reprovadas / total_geral) * 100

    print(f"\n   PRODUÇÃO TOTAL ANALISADA .......: {total_geral} peça(s)")
    print(f"   Peças APROVADAS ................: {total_aprovadas} "
          f"({taxa_aprovacao:.1f}%)")
    print(f"   Peças REPROVADAS ...............: {total_reprovadas} "
          f"({taxa_reprovacao:.1f}%)")

    # --- Motivos de reprovação agrupados por critério ---
    if total_reprovadas > 0:
        contagem_motivos = {}
        for peca in pecas_reprovadas:
            for motivo in peca["motivos"]:
                criterio = motivo.split(":")[0]     # PESO / COR / COMPRIMENTO
                contagem_motivos[criterio] = contagem_motivos.get(criterio, 0) + 1

        print("\n   --- MOTIVOS DE REPROVAÇÃO (por critério) ---")
        for criterio, quantidade in contagem_motivos.items():
            print(f"   {criterio:<15}: {quantidade} ocorrência(s)")

        print("\n   --- DETALHAMENTO POR PEÇA ---")
        for peca in pecas_reprovadas:
            print(f"   [{peca['id']}]")
            for motivo in peca["motivos"]:
                print(f"      - {motivo}")

    # --- Armazenamento ---
    print("\n   --- ARMAZENAMENTO ---")
    print(f"   Caixas utilizadas ..............: {len(caixas)}")
    print(f"   Caixas fechadas (lacradas) .....: {total_caixas_fechadas()}")

    if len(caixas) > 0 and len(caixas[-1]) < CAPACIDADE_CAIXA:
        print(f"   Caixa em uso ...................: CAIXA {len(caixas)} "
              f"com {len(caixas[-1])}/{CAPACIDADE_CAIXA} peça(s)")
        print(f"   Espaço livre na caixa atual ....: "
              f"{CAPACIDADE_CAIXA - len(caixas[-1])} vaga(s)")

    print("\n" + "=" * 62)
    print(" FIM DO RELATÓRIO")
    print("=" * 62)
    pausar()


# ===========================================================================
# 11. OPÇÃO 6 — CARREGAR DADOS DE DEMONSTRAÇÃO
# ---------------------------------------------------------------------------
# Recurso de apoio: popula o sistema com um lote de teste, útil para
# demonstrar rapidamente o funcionamento (inclusive no vídeo pitch).
# ===========================================================================

def carregar_demonstracao():
    cabecalho("6) CARREGAR LOTE DE DEMONSTRAÇÃO")

    lote = [
        # id,        peso,   cor,       comprimento
        ("PC-001",   98.0,  "azul",    15.0),
        ("PC-002",  101.5,  "verde",   12.5),
        ("PC-003",   95.0,  "azul",    10.0),
        ("PC-004",  120.0,  "azul",    14.0),   # reprovada: peso
        ("PC-005",  100.0,  "verde",   18.0),
        ("PC-006",   99.2,  "vermelho", 16.0),  # reprovada: cor
        ("PC-007",  103.0,  "azul",    19.5),
        ("PC-008",   97.5,  "verde",   11.0),
        ("PC-009",  100.1,  "azul",    25.0),   # reprovada: comprimento
        ("PC-010",  104.0,  "verde",   13.3),
        ("PC-011",   96.8,  "azul",    17.7),
        ("PC-012",  102.2,  "verde",   14.4),
        ("PC-013",   80.0,  "preto",    5.0),   # reprovada: 3 critérios
        ("PC-014",   99.9,  "azul",    20.0),
        ("PC-015",  105.0,  "verde",   10.5),
        ("PC-016",   98.4,  "azul",    16.6),
    ]

    adicionadas = 0
    for id_peca, peso, cor, comprimento in lote:
        if id_ja_existe(id_peca):
            continue

        peca = {"id": id_peca, "peso": peso,
                "cor": cor, "comprimento": comprimento}
        motivos = avaliar_peca(peca)
        peca["motivos"] = motivos

        if len(motivos) == 0:
            pecas_aprovadas.append(peca)
            armazenar_em_caixa(peca)
        else:
            pecas_reprovadas.append(peca)

        adicionadas += 1

    print(f"\n   [OK] {adicionadas} peça(s) processada(s).")
    print(f"   Aprovadas: {len(pecas_aprovadas)} | "
          f"Reprovadas: {len(pecas_reprovadas)} | "
          f"Caixas: {len(caixas)}")
    pausar()


# ===========================================================================
# 12. MENU PRINCIPAL — LAÇO DE REPETIÇÃO DO PROGRAMA
# ===========================================================================

def exibir_menu():
    print("\n")
    print("=" * 62)
    print("   SISTEMA DE CONTROLE DE PRODUÇÃO E QUALIDADE")
    print("   Automação Digital — Linha de Montagem")
    print("=" * 62)
    print(f"   Aprovadas: {len(pecas_aprovadas):<4} "
          f"Reprovadas: {len(pecas_reprovadas):<4} "
          f"Caixas: {len(caixas)}")
    print("-" * 62)
    print("   1 - Cadastrar nova peça")
    print("   2 - Listar peças aprovadas/reprovadas")
    print("   3 - Remover peça cadastrada")
    print("   4 - Listar caixas fechadas")
    print("   5 - Gerar relatório final")
    print("   6 - Carregar lote de demonstração")
    print("   0 - Sair do sistema")
    print("=" * 62)


def main():
    """Função principal: mantém o sistema em execução até o usuário sair."""
    while True:
        exibir_menu()
        opcao = input("   Selecione uma opção: ").strip()

        if opcao == "1":
            cadastrar_peca()
        elif opcao == "2":
            listar_pecas()
        elif opcao == "3":
            remover_peca()
        elif opcao == "4":
            listar_caixas()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "6":
            carregar_demonstracao()
        elif opcao == "0":
            print("\n   Encerrando o sistema. Produção finalizada.")
            print("   Até logo!\n")
            break
        else:
            print("\n   [!] Opção inválida. Escolha um número de 0 a 6.")
            pausar()


# ===========================================================================
# 13. PONTO DE ENTRADA
# ===========================================================================

if __name__ == "__main__":
    main()