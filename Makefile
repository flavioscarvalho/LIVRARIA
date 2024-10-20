# Definir a versão do Python utilizada no projeto
PYTHON_VERSION ?= 3.12.2

# Diretórios contendo as bibliotecas do projeto
LIBRARY_DIRS = order product bookstore

# Diretório de build do projeto
BUILD_DIR ?= build

# Opções para o PyTest
PYTEST_HTML_OPTIONS = --html=$(BUILD_DIR)/report.html --self-contained-html
PYTEST_TAP_OPTIONS = --tap-combined --tap-outdir $(BUILD_DIR)
PYTEST_COVERAGE_OPTIONS = --cov=$(LIBRARY_DIRS)
PYTEST_OPTIONS ?= $(PYTEST_HTML_OPTIONS) $(PYTEST_TAP_OPTIONS) $(PYTEST_COVERAGE_OPTIONS)

# Opções para o MyPy (verificação de tipos estáticos)
MYPY_OPTS ?= --python-version $(basename $(PYTHON_VERSION)) --show-column-numbers --pretty --html-report $(BUILD_DIR)/mypy

# Arquivo de versão do Python
PYTHON_VERSION_FILE=.python-version
ifeq ($(shell which pyenv),)
# Se pyenv não estiver instalado, estimar o caminho do Python
PYENV_VERSION_DIR ?= $(HOME)/.pyenv/versions/$(PYTHON_VERSION)
else
# Se pyenv estiver instalado
PYENV_VERSION_DIR ?= $(shell pyenv root)/versions/$(PYTHON_VERSION)
endif

# Definição do pip e do Poetry
PIP ?= pip3
POETRY_OPTS ?=
POETRY ?= poetry $(POETRY_OPTS)
RUN_PYPKG_BIN = $(POETRY) run

# Cores para saída no terminal
COLOR_ORANGE = \033[33m
COLOR_RESET = \033[0m

##@ Utility

.PHONY: help
help:  ## Exibir esta ajuda
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: version-python
version-python: ## Exibir a versão do Python em uso
	@echo $(PYTHON_VERSION)

##@ Testing

.PHONY: test
test: ## Executar testes
	$(RUN_PYPKG_BIN) pytest \
		$(PYTEST_OPTIONS) \
		tests/*.py

##@ Building and Publishing

.PHONY: build
build: ## Executar build do projeto
	$(POETRY) build

.PHONY: publish
publish: ## Publicar um build para o repositório configurado
	$(POETRY) publish $(POETRY_PUBLISH_OPTIONS_SET_BY_CI_ENV)

.PHONY: deps-py-update
deps-py-update: pyproject.toml ## Atualizar dependências do Poetry, por exemplo, após adicionar novas dependências manualmente
	$(POETRY) update

##@ Setup
# Instalação dinâmica do Python com pyenv
# $(PYENV_VERSION_DIR):
# 	pyenv install --skip-existing $(PYTHON_VERSION)

# $(PYTHON_VERSION_FILE): $(PYENV_VERSION_DIR)
# 	pyenv local $(PYTHON_VERSION)

.PHONY: deps
deps: deps-brew deps-py  ## Instalar todas as dependências

.PHONY: deps-brew
deps-brew: Brewfile ## Instalar dependências de desenvolvimento com Homebrew
	brew bundle --file=Brewfile
	@echo "$(COLOR_ORANGE)Certifique-se de que o pyenv está configurado no seu shell.$(COLOR_RESET)"
	@echo "$(COLOR_ORANGE)Deveria haver algo como 'eval \$$(pyenv init -)'$(COLOR_RESET)"

.PHONY: deps-py
deps-py: $(PYTHON_VERSION_FILE) ## Instalar dependências de desenvolvimento e runtime do Python
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade poetry
	$(POETRY) install

##@ Code Quality

.PHONY: check
check: check-py ## Executar verificações de qualidade de código

.PHONY: check-py
check-py: check-py-flake8 check-py-black check-py-mypy ## Verificar arquivos Python

.PHONY: check-py-flake8
check-py-flake8: ## Executar linter flake8
	$(RUN_PYPKG_BIN) flake8 --exclude=venv .

.PHONY: check-py-black
check-py-black: ## Executar black em modo de verificação (sem alterar arquivos)
	-$(RUN_PYPKG_BIN) black --check --line-length 118 --fast .

.PHONY: check-py-mypy
check-py-mypy: ## Executar mypy (verificação de tipos)
	$(RUN_PYPKG_BIN) mypy $(MYPY_OPTS) $(LIBRARY_DIRS)

.PHONY: format-py
format-py: ## Formatar arquivos Python com black
	$(RUN_PYPKG_BIN) black .

.PHONY: format-autopep8
format-autopep8: ## Formatar arquivos Python com autopep8
	$(RUN_PYPKG_BIN) autopep8 --in-place --recursive .

.PHONY: format-isort
format-isort: ## Ordenar imports com isort
	$(RUN_PYPKG_BIN) isort --recursive .
