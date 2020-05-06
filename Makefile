requirements: requirements-build requirements-test

requirements%:
	pip install -r requirements$*.txt

lint:
	flake8 .

test:
	pytest --cov=basic_api

build: clean
	python setup.py sdist bdist_wheel

release: build
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
