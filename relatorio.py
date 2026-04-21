from datetime import date
from arquivo import carregar_dados, exportar_relatorio_txt
from estoque import PRODUTOS_DISPONIVEIS


def _separador(char: str = "-", largura: int = 50) -> str:
    return char * largura


def gerar_relatorio() -> None:
    """
    Função: gera um relatório consolidado do estoque e das movimentações,
    exibindo no terminal e exportando para arquivo .txt.
    """
    dados     = carregar_dados()
    estoque: dict  = dados["estoque"]
    historico: list = dados["historico"]
    hoje      = date.today().strftime("%d/%m/%Y")

    linhas = []
    linhas.append(_separador("="))
    linhas.append("  AGROESTOQUE — RELATÓRIO CONSOLIDADO")
    linhas.append(f"  Emitido em: {hoje}")
    linhas.append(_separador("="))

    # --- Resumo do estoque ---
    linhas.append("\n  ESTOQUE ATUAL")
    linhas.append(_separador())
    if estoque:
        linhas.append(f"  {'PRODUTO':<22} {'SALDO':>10}  UNIDADE")
        linhas.append("  " + _separador())
        for nome, saldo in estoque.items():
            unidade = next((u for n, u in PRODUTOS_DISPONIVEIS if n == nome), "unid.")
            alerta = "  ⚠ ATENÇÃO: estoque baixo" if saldo < 10 else ""
            linhas.append(f"  {nome:<22} {saldo:>10.2f}  {unidade}{alerta}")
    else:
        linhas.append("  Nenhum produto em estoque.")

    # --- Totais por produto ---
    linhas.append("\n  TOTAIS POR PRODUTO (colheita x venda)")
    linhas.append(_separador())

    totais: dict = {}
    for mov in historico:
        prod = mov["produto"]
        if prod not in totais:
            totais[prod] = {"COLHEITA": 0.0, "VENDA": 0.0}
        totais[prod][mov["tipo"]] += mov["quantidade"]

    if totais:
        linhas.append(f"  {'PRODUTO':<22} {'COLHIDO':>10}  {'VENDIDO':>10}")
        linhas.append("  " + _separador())
        for prod, vals in totais.items():
            linhas.append(
                f"  {prod:<22} {vals['COLHEITA']:>10.2f}  {vals['VENDA']:>10.2f}"
            )
    else:
        linhas.append("  Nenhuma movimentação registrada.")

    # --- Histórico completo ---
    linhas.append("\n  HISTÓRICO COMPLETO DE MOVIMENTAÇÕES")
    linhas.append(_separador())
    if historico:
        for mov in reversed(historico):
            tipo_label = "COLHEITA" if mov["tipo"] == "COLHEITA" else "VENDA   "
            linhas.append(
                f"  {mov['data']}  {tipo_label}  {mov['produto']:<22}  "
                f"{mov['quantidade']:>8.2f} {mov['unidade']}"
            )
            if mov.get("observacao"):
                linhas.append(f"             Obs: {mov['observacao']}")
    else:
        linhas.append("  Nenhuma movimentação registrada.")

    linhas.append(_separador("="))
    linhas.append("  Fim do relatório.")
    linhas.append(_separador("="))

    conteudo = "\n".join(linhas)

    # Exibe no terminal
    print("\n" + conteudo)

    # Exporta para arquivo .txt
    nome_arquivo = f"relatorio_{date.today().strftime('%Y%m%d')}.txt"
    if exportar_relatorio_txt(conteudo, nome_arquivo):
        print(f"\n  ✔ Relatório exportado: {nome_arquivo}")
    else:
        print("\n  [AVISO] Não foi possível exportar o arquivo.")
