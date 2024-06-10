# fastapi-postgres-REST-API-example
Example REST API via fastapi, sqlalchemy, postgres, pydantic

==========

### Install PostgreSQL

```bash
sudo apt-get install postgresql
sudo apt-get install postgresql-client

sudo -u postgres createuser --interactive
# (use REPL to create "cocolacre" user)

sudo -u postgres psql
  ALTER USER cocolacre WITH PASSWORD '123456';
sudo -u postgres createdb myappdb
sudo -u postgres psql
  GRANT ALL PRIVILEGES ON DATABASE myappdb TO cocolacre;
```

### Configure PostgreSQL
Edit /etc/postgresql/14/main/pg_hba.conf:

```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```
Add the following line:

```bash
  host    myappdb    cocolacre    127.0.0.1/32    password
```

Перезагрузим poastres:
```bash
sudo service postgresql restart
```

В коле приложения конфигурируем подключение к базе:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://cocolacre:123456@localhost/myappdb"
```

### Alembic

https://alembic.sqlalchemy.org/en/latest/tutorial.html

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

Создали таблицу "tasks" после изначальной миграции.

### Тесты

```bash
pip install pytest
# запускаем тесты и радуемся.
pytest -s
```
<img width="728" alt="example_output" src="https://github.com/cocolacre/fastapi-postgres-REST-API-example/assets/13518992/662c672c-0d80-466d-b5ac-39aff8b4d39f">
