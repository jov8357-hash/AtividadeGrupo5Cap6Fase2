import oracledb


def conectar():
    """Conecta ao banco de dados Oracle e retorna a conexão."""
    try:
        conn = oracledb.connect(
            user="rm572062",          
            password="22071999",     
            dsn="oracle.fiap.com.br:1521/orcl"
        )
        return conn
    except oracledb.DatabaseError as e:
        print(f"[ERRO] Falha ao conectar ao banco de dados: {e}")
        return None


def criar_tabelas():
    """Cria as tabelas necessárias no banco Oracle, se ainda não existirem."""
    conn = conectar()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE '
                    CREATE TABLE TB_MOVIMENTACAO (
                        ID          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        PRODUTO     VARCHAR2(100)  NOT NULL,
                        TIPO        VARCHAR2(10)   NOT NULL,
                        QUANTIDADE  NUMBER(10, 2)  NOT NULL,
                        UNIDADE     VARCHAR2(20)   NOT NULL,
                        DATA_MOV    VARCHAR2(10)   NOT NULL,
                        OBSERVACAO  VARCHAR2(255)
                    )
                ';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -955 THEN RAISE; END IF;
            END;
        """)
        conn.commit()
        print("[OK] Tabelas verificadas/criadas com sucesso.")
    except oracledb.DatabaseError as e:
        print(f"[ERRO] Não foi possível criar as tabelas: {e}")
    finally:
        cursor.close()
        conn.close()


def inserir_movimentacao(produto: str, tipo: str, quantidade: float,
                         unidade: str, data_mov: str, observacao: str = ""):
    """Insere um registro de movimentação (colheita ou venda) no banco Oracle."""
    conn = conectar()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO TB_MOVIMENTACAO (PRODUTO, TIPO, QUANTIDADE, UNIDADE, DATA_MOV, OBSERVACAO)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (produto, tipo, quantidade, unidade, data_mov, observacao))
        conn.commit()
        return True
    except oracledb.DatabaseError as e:
        print(f"[ERRO] Falha ao inserir movimentação: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def buscar_historico(produto: str = None):
    """
    Retorna o histórico de movimentações do banco Oracle.
    Se produto for informado, filtra por ele.
    Retorna lista de dicionários.
    """
    conn = conectar()
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        if produto:
            cursor.execute("""
                SELECT ID, PRODUTO, TIPO, QUANTIDADE, UNIDADE, DATA_MOV, OBSERVACAO
                FROM TB_MOVIMENTACAO
                WHERE UPPER(PRODUTO) = UPPER(:1)
                ORDER BY ID DESC
            """, (produto,))
        else:
            cursor.execute("""
                SELECT ID, PRODUTO, TIPO, QUANTIDADE, UNIDADE, DATA_MOV, OBSERVACAO
                FROM TB_MOVIMENTACAO
                ORDER BY ID DESC
            """)

        colunas = ["id", "produto", "tipo", "quantidade", "unidade", "data_mov", "observacao"]
        resultados = []
        for linha in cursor.fetchall():
            resultados.append(dict(zip(colunas, linha)))
        return resultados

    except oracledb.DatabaseError as e:
        print(f"[ERRO] Falha ao buscar histórico: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
