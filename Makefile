setup:
	poetry shell
	poetry install

configure-pre-commit-hook:
	poetry run pre-commit install

lint or pre-commit:
	poetry run pre-commit run -a

build-and-publish:
	poetry build
	poetry publish
