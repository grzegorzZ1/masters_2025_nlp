ifneq (,$(wildcard .env))
	include .env
	export
endif

start:
	docker compose up -d
	docker compose logs -f app

download-model:
	docker exec -it ollama ollama pull $(MODEL_NAME)