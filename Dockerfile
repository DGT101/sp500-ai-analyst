# 1. Imagem base otimizada
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Instala dependências do sistema operacional necessárias para o curl (Healthcheck)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia primeiro os requerimentos para otimizar o cache de camadas do Docker
COPY requirements.txt .

# 5. Instala as dependências do ecossistema Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o código do projeto para dentro do contêiner
COPY . .

# 7. Informa ao Docker que a aplicação escuta na porta padrão do Streamlit
EXPOSE 8501

# 8. Healthcheck para monitorar a saúde do contêiner em produção
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 9. Comando de inicialização configurando o host para aceitar conexões externas
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]