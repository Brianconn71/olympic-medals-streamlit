FROM python:3.10-slim

WORKDIR /app 

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common


COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]