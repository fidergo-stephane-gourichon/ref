.PHONY: all docker static clean clean-db sandbox redirect-ports lint test

FLAKE8_ARGS = --max-line-length 180 --ignore _
DOCKER_RUN_SANDBOX = docker run \
	--rm -it \
	-v `pwd`/store-debug:/store \
	-v `pwd`/src/templates:/templates \
	-v `pwd`/src/static:/static \
	-v `pwd`/src/py:/app \
	alias/ref-python

all: docker

clean:
	rm src/static/jquery-3.4.0.min.js src/static/libsodium.js

	docker rmi alias/ref-python
	docker rmi alias/tls-proxy

clean-db:
	rm -rf store-debug/*

docker: static
	docker build -t alias/ref-python -f docker/Dockerfile.python src
	docker build -t alias/tls-proxy -f docker/Dockerfile.tls-proxy src/tls-proxy

up:
	docker-compose up

sandbox:
	$(DOCKER_RUN_SANDBOX) /bin/sh

test:
	$(DOCKER_RUN_SANDBOX) nosetests

static: \
	src/static/jquery-3.4.0.min.js \
	src/static/libsodium.js

src/static/jquery-3.4.0.min.js:
	wget -O $@ https://code.jquery.com/jquery-3.4.0.min.js

src/static/libsodium.js:
	wget -O $@ https://raw.githubusercontent.com/jedisct1/libsodium.js/master/dist/browsers/sodium.js

lint:
	flake8 $(FLAKE8_ARGS) src/py

