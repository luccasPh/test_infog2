## Pré-requisitos

- [Python 3](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Git](https://git-scm.com/)

Para executar API no modo de desenvolvimento:

- Em ambiente Linux, e preciso instalar este pacote: `sudo apt install python3-dev libpq-dev`

- Instale as dependências do projeto:
  `poetry install`

- Ative o ambiente virtual:
  `poetry shell`

- Execute docker-compose:
  `docker-compose up -d`

- Execute as migrações:
  `python app/manage.py migrate`

- Finalmente execute o servidor de desenvolvimento: `python app/manage.py runserver`

- Você pode testar a API atraveis da documentação em: http://localhost:8000/api/docs

- Para rodar os testes: `python app/manage.py test app`

---

Para executar API no modo de produção:

- Pare os contêineres:
  `docker-compose stop`

- Execute docker-compose produção:
  `docker-compose -f prod.yml up -d`
- Você pode testar a API prod com as collection do Postman localizada neste repositório. `teste_infog2.postman_collection.json`
