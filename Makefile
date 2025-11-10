.PHONY: help install run test clean

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Run application"
	@echo "  make test     - Run tests"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
