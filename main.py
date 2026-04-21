from banco import criar_tabelas
from estoque import (
    registrar_colheita,
    registrar_venda,
    exibir_estoque,
    exibir_historico,
)
from relatorio import gerar_relatorio


def exibir_menu() -> None:
    """Procedimento: exibe o menu principal do sistema."""
    print("\n" + "="*50)
    print("        🌾  AGROESTOQUE  🌾")
    print("  Sistema de Controle de Produção Rural")
    print("="*50)
    print("  [1] Registrar Colheita")
    print("  [2] Registrar Venda")
    print("  [3] Consultar Estoque Atual")
    print("  [4] Ver Histórico de Movimentações")
    print("  [5] Gerar Relatório")
    print("  [0] Sair")
    print("="*50)


def obter_opcao() -> str:
    """Função: lê e valida a opção digitada pelo usuário."""
    opcoes_validas = {"0", "1", "2", "3", "4", "5"}
    entrada = input("  Escolha uma opção: ").strip()
    if entrada not in opcoes_validas:
        print("  [ERRO] Opção inválida. Digite um número de 0 a 5.")
        return ""
    return entrada


def main() -> None:
    """Ponto de entrada principal do sistema AgroEstoque."""
    print("\n  Inicializando AgroEstoque...")
    criar_tabelas()

    while True:
        exibir_menu()
        opcao = obter_opcao()

        if opcao == "1":
            registrar_colheita()
        elif opcao == "2":
            registrar_venda()
        elif opcao == "3":
            exibir_estoque()
        elif opcao == "4":
            exibir_historico()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "0":
            print("\n  Encerrando AgroEstoque. Até logo! 🌱\n")
            break


if __name__ == "__main__":
    main()
