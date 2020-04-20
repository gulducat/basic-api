requirements: requirements-build requirements-test

requirements%:
	pip install -r requirements$*.txt

lint:
	flake8 setup.py test_basic_api.py basic_api/

test:
	pytest --cov=basic_api test_basic_api.py
	coverage report --show-missing

build:
	python setup.py sdist bdist_wheel

release:
	twine upload dist/*

clean:
	rm -rf .coverage .pytest_cache/ build/ dist/ *.egg-info/
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

# convenient for local dev
docker: docker-3.8

docker-%:
	docker run --rm -it -v `pwd`:/work -w /work python:$* bash

.PHONY: requirements lint test build publish clean docker docker-%
