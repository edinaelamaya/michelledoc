FROM python:3.11.1-bullseye
WORKDIR /code
COPY ./src/requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y gcc curl wget
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup \ --mariadb-server-version="mariadb-10.6"
RUN apt install -y libmariadb3 libmariadb-dev
RUN pip install uvicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src/app /code/app
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]