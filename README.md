# 📈 S&P 500 AI Analyst & Advisor

[![Code Quality CI](https://github.com/DGT101/sp500-ai-analyst/actions/workflows/linter.yml/badge.svg)](https://github.com/DGT101/sp500-ai-analyst/actions)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker Supported](https://img.shields.io/badge/docker-supported-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Uma plataforma inteligente de análise financeira baseada em dados que combina Engenharia de Dados clássica, Inteligência Artificial Analítica (Orquestração de LLMs via Groq) e práticas modernas de MLOps. O sistema coleta indicadores técnicos e fundamentalistas de ativos do S&P 500 em tempo real e gera relatórios personalizados com sugestões de alocação baseadas no perfil de risco do investidor.

---

## 🛠️ Tecnologias e Ferramentas

*   **Interface Interativa:** Streamlit (Módulos visuais e reatividade)
*   **Visualização de Dados:** Plotly (Gráficos interativos de Candlestick)
*   **Ingestão de Dados:** Yahoo Finance API (`yfinance`) & `pandas`
*   **Orquestração de IA:** Groq API (Modelo open-source `llama-3.3-70b-versatile` de altíssima velocidade)
*   **Conteinerização & Infraestrutura:** Docker & Docker Compose
*   **Integração Contínua (CI):** GitHub Actions (Linter automatizado com `black` e `flake8`)

---

## 📐 Arquitetura do Sistema

O fluxo de dados do projeto segue uma pipeline dividida em três camadas principais:

```text
┌────────────────────────┐      ┌─────────────────────────┐      ┌────────────────────────┐
│   Camada de Ingestão   │ ───> │  Orquestração de IA     │ ───> │   Camada de Entrega    │
│  (yfinance + Pandas)   │      │  (Groq API / Llama-3)   │      │      (Streamlit)       │
└────────────────────────┘      └─────────────────────────┘      └────────────────────────┘
 - Dados Históricos Preço        - Prompt Ingestion               - Gráficos Interativos
 - Cálculo RSI e Mídias Móveis   - Alinhamento de Perfil          - Métricas Financeiras
 - Múltiplos Fundamentalistas    - Geração de Parecer Técnico     - Renderização Markdown
```

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para replicar e rodar este projeto na sua própria máquina.

### 1. Pré-requisitos
* **Git** instalado.
* Conta na [Groq](https://console.groq.com/) para gerar uma API Key gratuita.
* **Opção A:** Docker e Docker Compose instalados.
* **Opção B:** Python 3.11+ instalado.

### 2. Clonando o Repositório
```bash
git clone https://github.com/DGT101/sp500-ai-analyst.git
cd sp500-ai-analyst
```

### 3. Configurando as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do Groq:
```env
GROQ_API_KEY=sua_chave_api_aqui
```

### 4. Executando a Aplicação

Escolha uma das opções abaixo para rodar a aplicação:

#### Opção A: Usando Docker (Recomendado)
Com o Docker e Docker Compose instalados, execute o seguinte comando na raiz do projeto:
```bash
docker-compose up --build -d
```
A aplicação estará disponível em [http://localhost:8501](http://localhost:8501). 
Para parar a aplicação, execute `docker-compose down`.

#### Opção B: Rodando Localmente (Python Venv)
Caso prefira rodar sem Docker, siga os passos para ambiente virtual:

1. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   
   # No Windows:
   .venv\Scripts\activate
   
   # No Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o aplicativo:**
   ```bash
   streamlit run src/app.py
   ```
A interface do Streamlit abrirá automaticamente no seu navegador padrão, também disponível em [http://localhost:8501](http://localhost:8501).
