import os
from openai import OpenAI

# 1. Inicializa o cliente apontando para a infraestrutura da Groq
# O SDK da OpenAI aceita esse redirecionamento de forma nativa através da base_url.
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),  # Usando a variável de ambiente correta
)

def build_analysis_prompt(
    ticker: str,
    target_date: str,
    tech_metrics: dict,
    fundamental_metrics: dict,
    investor_profile: str,
) -> str:
    """Monta um prompt altamente estruturado isolando as variáveis do contexto."""

    prompt = f"""
    Você é um analista financeiro sênior (CNPI) especialista em ações do S&P 500.
    Sua tarefa é gerar uma análise criteriosa e uma recomendação para um ativo com base nos dados fornecidos abaixo.

    [CONTEÚDO DA SOLICITAÇÃO]
    - Ativo: {ticker}
    - Data de Referência da Análise: {target_date}
    - Perfil do Investidor: {investor_profile} (Ex: 'Dividendos' foca em renda passiva e margens de segurança; 'Construção de Patrimônio' aceita mais volatilidade focando em crescimento/múltiplos).

    [DADOS TÉCNICOS DA AÇÃO NA DATA]
    - Preço de Fechamento: ${tech_metrics.get('Close'):.2f}
    - Média Móvel Simples (50 dias): ${tech_metrics.get('SMA_50'):.2f}
    - Média Móvel Simples (200 dias): ${tech_metrics.get('SMA_200'):.2f}
    - RSI (Índice de Força Relativa): {tech_metrics.get('RSI'):.2f} (Abaixo de 30 = Sobrevendido, Acima de 70 = Sobrecomprado)

    [DADOS FUNDAMENTALISTAS ATUAIS]
    - Empresa: {fundamental_metrics.get('company_name')}
    - Setor: {fundamental_metrics.get('sector')}
    - Múltiplo P/L (Preço/Lucro): {fundamental_metrics.get('pe_ratio')}
    - Preço/Valor Patrimonial (P/VP): {fundamental_metrics.get('price_to_book')}
    - Dividend Yield Histórico: {fundamental_metrics.get('dividend_yield'):.2f}%

    [DIRETRIZES DE SAÍDA]
    Gere um relatório macro dividido estritamente nos seguintes tópicos (use markdown para formatação):
    1. **Análise Gráfica & Momento**: Interprete a posição do preço em relação às médias móveis e o estado do RSI.
    2. **Análise Fundamentalista**: Avalie se os múltiplos (P/L, P/VP) indicam que a ação está cara ou barata e comente sobre a distribuição de dividendos.
    3. **Alinhamento de Perfil**: Explique se esta ação faz sentido para o perfil '{investor_profile}'.
    4. **Sugestão Prática**: Conclua com uma recomendação clara (Compra, Venda ou Cautela/Espera) baseada estritamente no momento do mercado e no perfil do usuário. Adicione um aviso de que isso não constitui recomendação formal de investimento.
    """
    return prompt

def generate_financial_report(
    ticker: str,
    target_date: str,
    tech_metrics: dict,
    fundamental_metrics: dict,
    investor_profile: str,
) -> str:
    """Envia o cenário estruturado para a Groq e retorna a resposta em texto."""
    print(f"Gerando relatório via Groq para {ticker}...")

    prompt = build_analysis_prompt(
        ticker, target_date, tech_metrics, fundamental_metrics, investor_profile
    )

    try:
        # Usamos um dos modelos abertos mais robustos do mercado disponíveis de graça na Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista financeiro analítico, direto e pragmático. Evite jargões excessivos e foque em decisões baseadas em dados.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  # Mantido baixo para evitar alucinações matemáticas
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao acionar o analista de IA na Groq: {e}"

# --- Bloco de Teste Executável ---
if __name__ == "__main__":
    # Dados fictícios simulando o output do passo 1 para teste
    exemplo_tecnico = {"Close": 180.20, "SMA_50": 175.10, "SMA_200": 162.00, "RSI": 45.2}

    exemplo_fundamental = {
        "company_name": "Microsoft Corp.",
        "sector": "Technology",
        "pe_ratio": 35.2,
        "price_to_book": 12.1,
        "dividend_yield": 0.72,
    }

    # Teste de execução direta
    relatorio = generate_financial_report(
        ticker="MSFT",
        target_date="2026-01-15",
        tech_metrics=exemplo_tecnico,
        fundamental_metrics=exemplo_fundamental,
        investor_profile="Construção de Patrimônio",
    )

    print("\n=== RELATÓRIO DO AGENTE DE IA (GROQ) ===\n")
    print(relatorio)
