# 🌾 AgroEstoque

**Sistema de Controle de Produção e Estoque Rural**

---

## 📌 Problema Tratado

Pequenos e médios produtores rurais frequentemente não possuem controle digitalizado sobre o que produzem e vendem. Isso resulta em:

- Desconhecimento do saldo real em estoque;
- Dificuldade para identificar prejuízos por excesso de venda ou perda de produto;
- Ausência de histórico para tomada de decisão.

Este sistema resolve esse problema oferecendo um controle simples, via terminal, de entradas (colheitas) e saídas (vendas) de produtos agrícolas, com persistência local em JSON e registro histórico em banco de dados Oracle.

---

## 💡 Solução

O **AgroEstoque** permite ao produtor rural:

1. **Registrar colheitas** — entrada de produto no estoque;
2. **Registrar vendas** — saída de produto do estoque com validação de saldo;
3. **Consultar o estoque atual** — com alerta visual para estoques baixos;
4. **Ver o histórico** — todas as movimentações em ordem cronológica;
5. **Gerar relatório** — consolidado em tela e exportado em arquivo `.txt`.

---

## 📁 Estrutura do Projeto

```
agroestoque/
├── main.py          # Menu principal e ponto de entrada
├── estoque.py       # Funções e procedimentos de estoque
├── relatorio.py     # Geração de relatórios
├── arquivo.py       # Leitura e gravação de arquivos JSON e TXT
├── banco.py         # Conexão e operações com banco Oracle
├── dados/
│   └── estoque.json # Persistência local dos dados
└── README.md
```

---

## 🔧 Conteúdos da Disciplina Aplicados

| Conteúdo | Aplicação no Projeto |
|---|---|
| **Funções com parâmetros** | `calcular_saldo(produto)`, `validar_quantidade(mensagem)`, `inserir_movimentacao(...)` |
| **Procedimentos** | `registrar_colheita()`, `registrar_venda()`, `exibir_estoque()`, `exibir_historico()` |
| **Lista** | `historico` — lista de dicionários com todas as movimentações |
| **Tupla** | `PRODUTOS_DISPONIVEIS` — produtos e unidades (dados imutáveis) |
| **Dicionário** | `estoque` — saldo atual por produto; `totais` no relatório |
| **Tabela de memória** | Lista de dicionários usada para o histórico completo |
| **Arquivo JSON** | `estoque.json` — persiste estoque e histórico entre execuções |
| **Arquivo TXT** | Exportação do relatório consolidado |
| **Banco Oracle** | Tabela `TB_MOVIMENTACAO` com todas as entradas e saídas |

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
pip install oracledb
```

### Configuração do Banco

No arquivo `banco.py`, edite as credenciais:

```python
user="seu_usuario",
password="sua_senha",
dsn="oracle.fiap.com.br:1521/orcl"
```

### Execução

```bash
python main.py
```

---

## 🖥️ Exemplo de Uso

```
==================================================
        🌾  AGROESTOQUE  🌾
  Sistema de Controle de Produção Rural
==================================================
  [1] Registrar Colheita
  [2] Registrar Venda
  [3] Consultar Estoque Atual
  [4] Ver Histórico de Movimentações
  [5] Gerar Relatório
  [0] Sair
==================================================
```

---

## 👥 Grupo

- José Artur Barreira do Vale — RM572062
- Guilherme Agostinho Rodrigues — RM569886

