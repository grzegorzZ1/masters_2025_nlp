FROM python:3.11-slim

COPY ./app /app
COPY .env /app/.env
WORKDIR /app
RUN pip install -r ./requirements_app.txt
ENV IS_IN_DOCKER=Yes

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "/app/Home_Page.py", "--server.address=0.0.0.0", "--server.port=8501"]