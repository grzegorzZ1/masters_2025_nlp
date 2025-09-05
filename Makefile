ifneq (,$(wildcard .env))
	include .env
	export
endif

start:
	docker compose up -d
	docker compose logs -f app

end:
	docker compose down

download-model:
	docker exec -it ollama ollama pull $(MODEL_NAME)

test-locally:
	streamlit run app/Home_Page.py