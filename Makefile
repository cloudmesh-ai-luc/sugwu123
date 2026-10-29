PYTHON ?= python3

.PHONY: help install test demo run doc view clean

help:
	@echo "Available targets: install, test, demo, run, doc, view, clean"

install:
	$(PYTHON) -m pip install -e .

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s src/sports/tests -t src -v

demo:
	PYTHONPATH=src $(PYTHON) -m sports import-nba
	PYTHONPATH=src $(PYTHON) -m sports model-summary --team CHI --threshold 100

run:
	PYTHONPATH=src $(PYTHON) -m sports serve --host 127.0.0.1 --port 8000

doc:
	mkdocs build

view:
	mkdocs serve

clean:
	rm -rf build dist site *.egg-info src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
