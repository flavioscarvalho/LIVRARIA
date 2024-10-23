# LIVRARIA

`Bookstore` é uma aplicação desenvolvida como parte do curso de Backend em Python da EBAC.

## Pré-requisitos

- **Python**: Versão 3.12.2 ou superior
- **Poetry**: Versão 1.8.4
- **Docker** e **Docker Compose**

## Início Rápido

### 1. Clonar este repositório

```bash
git clone git@github.com:drsantos20/bookstore.git


cd bookstore
poetry install


poetry run python manage.py migrate


poetry run python manage.py runserver


docker-compose up -d --build
docker-compose exec web python manage.py migrate


docker-compose exec web python manage.py test



### Resumo das Melhorias:
1. **Organização por Seções**: Dividido em seções claras como "Pré-requisitos", "Início Rápido" e "Notas".
2. **Formatação de Código**: Usado blocos de código para comandos (`bash`) e links claros.
3. **Descrição mais Amigável**: Melhorada a descrição do projeto e a clareza das instruções.

Com esse README, seu projeto será mais acessível para desenvolvedores e colegas que queiram contribuir. Se precisar de mais ajustes, estarei por aqui!
