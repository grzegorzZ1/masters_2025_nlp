FROM python:3.11-slim

COPY ./app /app
COPY .env .env
WORKDIR /app
RUN source .env & pip install -r ./requirements_app.txt

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "/app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]