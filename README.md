# Visualização de Dados (Streamlit, Plotly, Matplotlib)

Visualização de dados em Python, com notebook exploratório e um dashboard interativo em Streamlit e visualização em HTML.

## Conteúdo

- Notebook com exemplos de gráficos usando Plotly, Matplotlib e Seaborn (dispersão, histograma, barras, gráfico de bolhas, sliders interativos, etc.).
- `dashboard_streamlit.py`: dashboard Streamlit com os principais KPIs do dataset de clientes/empréstimos (renda média, taxa de aprovação, histórico de crédito, entre outros), com filtros interativos.
- `Vencedor.html`: relatório de análise exploratória (EDA) do dataset, gerado com [YData Profiling](https://github.com/ydataai/ydata-profiling) a partir do mesmo notebook rodado no Google Colab. Basta baixar e abrir no navegador para visualizar estatísticas, correlações e distribuições de todas as colunas.
- `requirements.txt`: dependências do projeto.

## Dataset

O dashboard e parte do notebook usam uma base de clientes com dados de solicitação de empréstimo (colunas como `sexo`, `educacao`, `renda`, `emprestimo`, `historico_credito`, `aprovacao_emprestimo`, entre outras). Ajuste o caminho do CSV em `dashboard_streamlit.py` (constante `CAMINHO_CSV`) para o local do arquivo na sua máquina.

## Como rodar

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 3. Rodar o notebook

Abra o `.ipynb` no VS Code (ou Jupyter) e selecione o kernel do `.venv`.

### 4. Rodar o dashboard

```powershell
streamlit run dashboard_streamlit.py
```

O dashboard abre em `http://localhost:8501`.

## Tecnologias

- Python
- Pandas
- Plotly Express / Graph Objects
- Matplotlib / Seaborn
- Streamlit
