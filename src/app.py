import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Importa as funções que criamos nos passos anteriores
from data_pipeline import (
    fetch_stock_history,
    calculate_technical_indicators,
    fetch_fundamental_metrics,
)
from llm_analyst import generate_financial_report

# ==========================================
# 1. CONFIGURAÇÕES DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="S&P 500 AI Analyst & Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 S&P 500 AI Analyst & Advisor")
st.caption(
    "Uma ferramenta integrada de Machine Learning, NLP (Groq Llama-3) e Engenharia de Dados para Portfólio."
)

# ==========================================
# 2. BARRA LATERAL (INPUTS DO USUÁRIO)
# ==========================================
st.sidebar.header("Parâmetros da Análise")

# Lista simplificada para o MVP. Futuramente pode vir de uma lista dinâmica ou CSV do S&P 500.
SP500_TICKERS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NVDA",
    "TSLA",
    "BRK-B",
    "JNJ",
    "V",
]
ticker = st.sidebar.selectbox("Selecione o Ativo (S&P 500)", SP500_TICKERS)

# Definição de datas pelo usuário
data_alvo = st.sidebar.date_input(
    "Data de Referência", datetime.today() - timedelta(days=1)
)

# Perfil do Investidor (para calibrar o conselho da LLM)
perfil = st.sidebar.selectbox(
    "Perfil do Investidor / Objetivo",
    [
        "Construção de Patrimônio",
        "Foco em Dividendos/Renda Passiva",
        "Conservador/Proteção",
    ],
)

submit_button = st.sidebar.button("Gerar Análise Completa")

# ==========================================
# 3. LOGICA PRINCIPAL DE PROCESSAMENTO
# ==========================================
if submit_button:
    # Mostra um spinner amigável de carregamento
    with st.spinner("Processando dados do mercado e acionando analista de IA..."):

        # 1. Pipeline de Dados: Coleta o histórico para calcular as métricas.
        # Pegamos 365 dias antes da data alvo para garantir histórico suficiente para as Médias Móveis de 200 dias
        start_date = (data_alvo - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = (data_alvo + timedelta(days=1)).strftime("%Y-%m-%d")

        df_raw = fetch_stock_history(ticker, start_date, end_date)

        if not df_raw.empty:
            df_technical = calculate_technical_indicators(df_raw)
            fundamentals = fetch_fundamental_metrics(ticker)

            # Obtém a linha exata da data alvo selecionada pelo usuário
            target_str = data_alvo.strftime("%Y-%m-%d")

            try:
                # Se a data alvo caiu em um final de semana, pegamos o último dia útil disponível
                if target_str in df_technical.index:
                    latest_metrics = df_technical.loc[target_str]
                else:
                    latest_metrics = df_technical.iloc[-1]
                    st.warning(
                        "Os mercados estavam fechados na data selecionada. "
                        "Exibindo dados do último dia útil disponível."
                    )

                # Prepara os dicionários para passar para o módulo de IA
                tech_dict = {
                    "Close": float(latest_metrics["Close"]),
                    "SMA_50": float(latest_metrics["SMA_50"]),
                    "SMA_200": float(latest_metrics["SMA_200"]),
                    "RSI": float(latest_metrics["RSI"]),
                }

                # ==========================================
                # 4. RENDERIZAÇÃO DA INTERFACE (STREAMLIT COLUMNS)
                # ==========================================
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("📊 Indicadores Técnicos & Gráfico")

                    # Exibição de Métricas Rápidas
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    metric_col1.metric(
                        "Preço de Fechamento", f"${tech_dict['Close']:.2f}"
                    )
                    metric_col2.metric("RSI (14)", f"{tech_dict['RSI']:.1f}")
                    metric_col3.metric(
                        "Div. Yield", f"{fundamentals.get('dividend_yield', 0):.2f}%"
                    )

                    # Gráfico Candlestick Interativo com Plotly
                    # Mostra os últimos 60 dias de pregão para não poluir a tela
                    df_plot = df_technical.tail(60)

                    fig = go.Figure()
                    # Velas
                    fig.add_trace(
                        go.Candlestick(
                            x=df_plot.index,
                            open=df_plot["Open"],
                            high=df_plot["High"],
                            low=df_plot["Low"],
                            close=df_plot["Close"],
                            name="Candles",
                        )
                    )
                    # Média Móvel de 50
                    fig.add_trace(
                        go.Scatter(
                            x=df_plot.index,
                            y=df_plot["SMA_50"],
                            line=dict(color="#deff9a", width=1.5),
                            name="SMA 50",
                        )
                    )

                    fig.update_layout(
                        template="plotly_dark",
                        xaxis_rangeslider_visible=False,
                        margin=dict(l=20, r=20, t=20, b=20),
                        height=350,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.subheader("🤖 Parecer do Analista de IA (Groq)")

                    # Executa a chamada assíncrona/rápida para o modelo Llama-3 através da Groq
                    relatorio = generate_financial_report(
                        ticker=ticker,
                        target_date=target_str,
                        tech_metrics=tech_dict,
                        fundamental_metrics=fundamentals,
                        investor_profile=perfil,
                    )

                    # O Streamlit renderiza markdown perfeitamente com todas as quebras e negritos
                    st.markdown(relatorio)

            except Exception as e:
                st.error(f"Erro ao computar as métricas para a data selecionada: {e}")
        else:
            st.error(
                "Não foi possível carregar dados para o ticker informado. Verifique se o ticker está correto ou tente um período diferente."
            )
else:
    # Estado inicial amigável quando o usuário entra na tela
    st.info(
        "👈 Selecione os parâmetros na barra lateral esquerda e clique em 'Gerar Análise Completa' para iniciar."
    )
