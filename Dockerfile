# Usar a imagem base do Python 3.12.2 slim
FROM python:3.12.2-slim AS python-base

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Adicionar Poetry e o ambiente virtual ao PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Atualizar os pacotes e instalar dependências essenciais
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl build-essential libpq-dev gcc

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Definir o diretório de trabalho e copiar os arquivos de dependências do projeto
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Instalar as dependências de produção do projeto
RUN poetry install --no-dev

# Copiar todo o código da aplicação para o diretório /app
WORKDIR /app
COPY . /app/

# Expor a porta padrão do Django
EXPOSE 8000

# Comando padrão para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
