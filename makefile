.PHONY: run_frontend run_backend gather_dependencies

run_frontend:
	yarn --cwd components/frontend run dev

run_backend:
	FLASK_APP=components/backend/ov_rest_server.py FLASK_DEBUG=1 flask run

gather_dependencies:
	yarn --cwd components/frontend install
