import pandas as pd
import yfinance as yf

def fetch_stock_history(
    ticker: str, start_date: str, end_date: str
) -> pd.DataFrame:
    """Coleta o histórico de preços de uma ação usando a biblioteca yfinance."""
    print(f"Buscando dados históricos para {ticker}...")
    try:
        # Baixa os dados brutos
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            raise ValueError(
                f"Nenhum dado encontrado para o ticker {ticker} no período selecionado."
            )

        # Ajusta o multi-index que o yfinance gera por padrão se necessário
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return df
    except Exception as e:
        print(f"Erro ao buscar dados técnicos: {e}")
        return pd.DataFrame()

def calculate_technical_indicators(
    df: pd.DataFrame, rsi_period: int = 14
) -> pd.DataFrame:
    """Calcula Médias Móveis (SMA) e o RSI (Wilder's Smoothing) usando Pandas puro."""
    df = df.copy()

    # 1. Médias Móveis Simples (SMA)
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()

    # 2. Cálculo do RSI (Relative Strength Index)
    delta = df["Close"].diff()

    # Isola ganhos e perdas
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Média Móvel Exponencial (Wilder's Smoothing)
    # com = period - 1 é o equivalente matemático ao padrão de Wilder
    ema_gain = gain.ewm(com=rsi_period - 1, adjust=False).mean()
    ema_loss = loss.ewm(com=rsi_period - 1, adjust=False).mean()

    # Evita divisão por zero caso a perda seja nula
    rs = ema_gain / ema_loss.replace(0, 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

def fetch_fundamental_metrics(ticker: str) -> dict:
    """Extrai métricas fundamentais essenciais do ticker informado."""
    print(f"Buscando dados fundamentais para {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Dicionário com dados cruciais para a análise da LLM
        fundamentals = {
            "company_name": info.get("longName", ticker),
            "pe_ratio": info.get("trailingPE"),  # Preço / Lucro
            "forward_pe": info.get("forwardPE"),
            "dividend_yield": info.get(
                "dividendYield"
            ),  # Ex: 0.02 = 2% ao ano
            "price_to_book": info.get("priceToBook"),  # P/VP
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector"),
        }

        # Multiplica o Dividend Yield por 100 para facilitar a visualização posterior
        if fundamentals["dividend_yield"]:
            fundamentals["dividend_yield"] *= 100

        return fundamentals
    except Exception as e:
        print(f"Erro ao buscar dados fundamentais: {e}")
        return {}

# --- Bloco de Teste Executável ---
if __name__ == "__main__":
    # Testando com a Apple (AAPL) para o ano de 2025
    TICKER_TESTE = "NVDA"
    DATA_INICIO = "2025-01-01"
    DATA_FIM = "2025-12-31"

    # 1. Executa coleta e cálculo técnico
    df_raw = fetch_stock_history(TICKER_TESTE, DATA_INICIO, DATA_FIM)

    if not df_raw.empty:
        df_indicators = calculate_technical_indicators(df_raw)

        print("\n=== Últimas 5 linhas dos dados técnicos ===")
        print(
            df_indicators[["Close", "SMA_50", "SMA_200", "RSI"]].tail().round(2)
        )

    # 2. Executa coleta fundamentalista
    dados_fundamentais = fetch_fundamental_metrics(TICKER_TESTE)

    print("\n=== Indicadores Fundamentais ===")
    for chave, valor in dados_fundamentais.items():
        print(f"{chave}: {valor}")
