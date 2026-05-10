.PHONY: install run test lint generate-data train-model benchmark clean docker-build docker-run

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check app/ tests/ scripts/

generate-data:
	python scripts/generate_data.py

train-model:
	python scripts/train_model.py

benchmark:
	python scripts/benchmark_astar.py

seed-courts:
	python scripts/seed_courts.py

demo:
	python -m app.cli.demo

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

docker-build:
	docker build -t courtfind-ai:latest .

docker-run:
	docker-compose up

full-setup: install generate-data train-model
	@echo "CourtFind AI is ready. Run: make run"
