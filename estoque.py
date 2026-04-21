from datetime import date
from arquivo import carregar_dados, salvar_dados
from banco import inserir_movimentacao

# Tupla com produtos cadastrados: (nome_exibição, unidade_de_medida)
PRODUTOS_DISPONIVEIS: tuple = (
    ("Cana-de-Açúcar", "tonelada"),
    ("Milho",          "saca 60kg"),
    ("Soja",           "saca 60kg"),
    ("Laranja",        "caixa 40kg"),
    ("Café",           "saca 60kg"),
)


def listar_produtos() -> None:
    """Procedimento: exibe os produtos disponíveis no sistema."""
    print("\n  Produtos disponíveis:")
    for i, (nome, unidade) in enumerate(PRODUTOS_DISPONIVEIS, start=1):
        print(f"  [{i}] {nome} ({unidade})")


def selecionar_produto() -> tuple | None:
    """
    Solicita que o usuário escolha um produto da lista.
    Retorna a tupla (nome, unidade) ou None se inválido.
    """
    listar_produtos()
    entrada = input("\n  Digite o número do produto: ").strip()

    if not entrada.isdigit():
        print("  [ERRO] Digite apenas o número da opção.")
        return None

    idx = int(entrada) - 1
    if idx < 0 or idx >= len(PRODUTOS_DISPONIVEIS):
        print("  [ERRO] Opção inválida.")
        return None

    return PRODUTOS_DISPONIVEIS[idx]


def validar_quantidade(mensagem: str) -> float | None:
    """
    Função: solicita e valida uma quantidade numérica positiva.
    Retorna o float válido ou None se inválido.
    """
    entrada = input(mensagem).strip().replace(",", ".")
    try:
        quantidade = float(entrada)
        if quantidade <= 0:
            print("  [ERRO] A quantidade deve ser maior que zero.")
            return None
        return quantidade
    except ValueError:
        print("  [ERRO] Valor inválido. Digite um número (ex: 10 ou 10.5).")
        return None


def registrar_colheita() -> None:
    """Procedimento: registra uma entrada de colheita no estoque e no banco."""
    print("\n" + "="*50)
    print("  REGISTRAR COLHEITA")
    print("="*50)

    produto_info = selecionar_produto()
    if not produto_info:
        return

    nome, unidade = produto_info
    quantidade = validar_quantidade(f"  Quantidade colhida (em {unidade}): ")
    if not quantidade:
        return

    obs = input("  Observação (opcional): ").strip()
    hoje = date.today().strftime("%d/%m/%Y")

    # Atualiza JSON local
    dados = carregar_dados()
    estoque: dict = dados["estoque"]
    historico: list = dados["historico"]

    estoque[nome] = estoque.get(nome, 0) + quantidade

    registro = {
        "produto":    nome,
        "tipo":       "COLHEITA",
        "quantidade": quantidade,
        "unidade":    unidade,
        "data":       hoje,
        "observacao": obs
    }
    historico.append(registro)
    dados["estoque"]   = estoque
    dados["historico"] = historico
    salvar_dados(dados)

    # Salva no Oracle
    inserir_movimentacao(nome, "COLHEITA", quantidade, unidade, hoje, obs)

    print(f"\n  ✔ Colheita de {quantidade} {unidade}(s) de {nome} registrada com sucesso!")


def registrar_venda() -> None:
    """Procedimento: registra uma saída (venda) do estoque e no banco."""
    print("\n" + "="*50)
    print("  REGISTRAR VENDA")
    print("="*50)

    produto_info = selecionar_produto()
    if not produto_info:
        return

    nome, unidade = produto_info

    dados   = carregar_dados()
    estoque: dict = dados["estoque"]
    saldo_atual   = estoque.get(nome, 0)

    if saldo_atual <= 0:
        print(f"\n  [AVISO] Não há estoque disponível de {nome}.")
        return

    print(f"  Saldo disponível: {saldo_atual:.2f} {unidade}(s)")
    quantidade = validar_quantidade(f"  Quantidade vendida (em {unidade}): ")
    if not quantidade:
        return

    if quantidade > saldo_atual:
        print(f"\n  [ERRO] Quantidade ({quantidade}) maior que o saldo ({saldo_atual:.2f}).")
        return

    obs = input("  Observação (opcional): ").strip()
    hoje = date.today().strftime("%d/%m/%Y")

    estoque[nome] = saldo_atual - quantidade
    historico: list = dados["historico"]
    registro = {
        "produto":    nome,
        "tipo":       "VENDA",
        "quantidade": quantidade,
        "unidade":    unidade,
        "data":       hoje,
        "observacao": obs
    }
    historico.append(registro)
    dados["estoque"]   = estoque
    dados["historico"] = historico
    salvar_dados(dados)

    inserir_movimentacao(nome, "VENDA", quantidade, unidade, hoje, obs)

    print(f"\n  ✔ Venda de {quantidade} {unidade}(s) de {nome} registrada com sucesso!")


def calcular_saldo(produto: str) -> float:
    """Função: retorna o saldo atual de um produto no estoque."""
    dados   = carregar_dados()
    estoque: dict = dados["estoque"]
    return estoque.get(produto, 0.0)


def exibir_estoque() -> None:
    """Procedimento: imprime o estado atual do estoque de forma organizada."""
    print("\n" + "="*50)
    print("  ESTOQUE ATUAL")
    print("="*50)

    dados   = carregar_dados()
    estoque: dict = dados["estoque"]

    if not estoque:
        print("  Nenhum produto em estoque ainda.")
        return

    print(f"  {'PRODUTO':<22} {'SALDO':>10}  UNIDADE")
    print("  " + "-"*46)
    for nome, saldo in estoque.items():
        unidade = next((u for n, u in PRODUTOS_DISPONIVEIS if n == nome), "unid.")
        alerta = " ⚠ BAIXO" if saldo < 10 else ""
        print(f"  {nome:<22} {saldo:>10.2f}  {unidade}{alerta}")
    print("="*50)


def exibir_historico() -> None:
    """Procedimento: imprime o histórico completo de movimentações."""
    print("\n" + "="*50)
    print("  HISTÓRICO DE MOVIMENTAÇÕES")
    print("="*50)

    dados     = carregar_dados()
    historico: list = dados["historico"]

    if not historico:
        print("  Nenhuma movimentação registrada ainda.")
        return

    for mov in reversed(historico):
        tipo_label = "🌾 COLHEITA" if mov["tipo"] == "COLHEITA" else "💰 VENDA   "
        print(f"  {mov['data']}  {tipo_label}  {mov['produto']:<22}  "
              f"{mov['quantidade']:>8.2f} {mov['unidade']}")
        if mov.get("observacao"):
            print(f"             Obs: {mov['observacao']}")
    print("="*50)
