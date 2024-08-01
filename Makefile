all:
	pytest -l

dev:
	pytest tests/integration/test_dev.py -s

upload:
	python setup.py sdist upload