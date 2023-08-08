# if no env forenvfile, then dev
ifndef env
override env=dev
endif

PYTHON_VERSION=3.9
VIRTUAL_ENV := .venv
IMAGE := cocus-assignment

.PHONY: build-docker-image
build:
	@echo $(env)
	@echo "Building image..."
	@docker build -t ${IMAGE}:dev .

.PHONY: run-docker-image
run: build
	@echo "Building image and opening shell..."
	@docker run -i -t \
		--env-file $(PWD)/configs/envfile-$(env) \
		-v $(PWD)/src:/usr/app/ \
		${IMAGE}:dev /bin/bash
