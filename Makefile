PYTHON = python3
PIP = pip3
TEST_PATH = ./tests/
SETUP_FILE = setup.py
MODULE_NAME = UIP

clean-pyc:
	find . -name '__pycache__' \
		-exec rm --force --recursive {} +
	find . -name '*~' \
		-exec rm --force {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive UIP.egg-info/
	rm --force --recursive .cache/
	rm --force .coverage

clean: clean-pyc clean-build

install: clean-pyc
	$(PYTHON) $(SETUP_FILE) install

uninstall: clean-pyc
	$(PIP) uninstall $(MODULE_NAME)

test:
	pytest --cov --verbose --color=yes $(TEST_PATH)
	rm .coverage

lint:
	coala --non-interactive
