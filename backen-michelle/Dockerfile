FROM python:3.11.1-bullseye
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y gcc curl wget
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup \ --mariadb-server-version="mariadb-10.6"
RUN apt install -y libmariadb3 libmariadb-dev
RUN pip install uvicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/app
COPY ./src/app/scripts/init_db.py /code/app/scripts/init_db.py
COPY ./start.sh /code/start.sh

# Dar permisos de ejecución
RUN chmod +x /code/start.sh

# Establecer PYTHONPATH
ENV PYTHONPATH=/code

CMD ["/code/start.sh"]