PYTHON = python3
PIP = pip3
SETUP_FILE = setup.py
COAFILE = .coafile
MODULE_NAME = UIP
TEST_REQUIREMENTS = test-requirements.txt

clean-pyc:
	find . -name '__pycache__' \
		-exec rm -rf {} +
	find . -name '*~' \
		-exec rm -rf {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf UIP.egg-info/
	rm -rf .cache/
	rm -f .coverage

clean: clean-pyc clean-build

install: clean-pyc
	$(PYTHON) $(SETUP_FILE) install

uninstall: clean-pyc
	$(PIP) uninstall $(MODULE_NAME)

test-install: clean
	$(PIP) install --requirement $(TEST_REQUIREMENTS)
	cib install -c $(COAFILE)

test:
	pytest

lint:
	coala --non-interactive
