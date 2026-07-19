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
