PYTHON ?= python3
NAME ?= sports-midterm

.PHONY: demo serve test analyze history model historical-serve vm-deploy vm-status vm-start vm-stop

demo:
	cd .. && $(PYTHON) -m sports demo

serve:
	cd .. && $(PYTHON) -m sports serve

test:
	cd .. && $(PYTHON) -m unittest discover -s sports/tests -v

analyze:
	cd .. && $(PYTHON) -m sports analyze --team "Lake City Lynx" --player "Morgan Lee" --threshold 20.5

history:
	cd .. && $(PYTHON) -m sports.history --season 2015

model:
	cd .. && $(PYTHON) -m sports --db sports/data/history.sqlite3 model --team CHI --threshold 100.5

historical-serve:
	cd .. && $(PYTHON) -m sports --db sports/data/history.sqlite3 serve

vm-deploy:
	cd .. && $(PYTHON) -m sports.vm deploy --name "$(NAME)"

vm-status:
	cd .. && $(PYTHON) -m sports.vm status --name "$(NAME)"

vm-start:
	cd .. && $(PYTHON) -m sports.vm start --name "$(NAME)"

vm-stop:
	cd .. && $(PYTHON) -m sports.vm stop --name "$(NAME)"
