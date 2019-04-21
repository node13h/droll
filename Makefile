DOCKER_TAG := latest
DOCKER_REPOSITORY := docker.io/alikov/droll

VERSION = $(shell cat VERSION)

.PHONY: sdist clean build-image push-image

clean:
	rm -rf dist

sdist: dist/droll-$(VERSION).tar.gz

dist/droll-$(VERSION).tar.gz:
	python setup.py sdist

build-image: sdist
	docker build -t $(DOCKER_REPOSITORY):$(DOCKER_TAG) --build-arg VERSION=$(shell cat VERSION) .
	docker build -f Dockerfile.nginx -t $(DOCKER_REPOSITORY)-nginx:$(DOCKER_TAG) .

push-image: build-image
	docker push $(DOCKER_REPOSITORY):$(DOCKER_TAG)
	docker push $(DOCKER_REPOSITORY)-nginx:$(DOCKER_TAG)
