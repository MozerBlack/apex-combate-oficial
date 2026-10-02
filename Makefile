.PHONY: run check test smoke docker-build

run:
	python3 server.py

check:
	python3 scripts/check_project.py

test:
	python3 -m unittest discover -s tests -v

smoke:
	python3 scripts/smoke_test.py http://127.0.0.1:8080

docker-build:
	docker build -t apex-combate:local .
