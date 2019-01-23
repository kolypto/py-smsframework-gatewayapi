all:

SHELL := /bin/bash

# Package
.PHONY: clean
clean:
	@rm -rf build/ dist/ *.egg-info/
#README.md:
#	@python misc/_doc/README.py | j2 --format=json -o README.md misc/_doc/README.md.j2

.PHONY: build publish-test publish
build:
	@./setup.py build sdist bdist_wheel
publish-test:
	@twine upload --repository pypitest dist/*
publish:
	@twine upload dist/*


.PHONY: test test-tox test-docker
test:
	@nosetests
test-tox:
	@tox
test-docker:
	@docker run --rm -it -v `pwd`:/src themattrix/tox
