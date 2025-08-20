.PHONY: all ${MAKECMDGOALS}

MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(dir $(MAKEFILE_PATH))

MOLECULE_SCENARIO ?= create
MOLECULE_DOCKER_IMAGE ?= ubuntu2204
GALAXY_API_KEY ?=
GITHUB_REPOSITORY ?= $$(git config --get remote.origin.url | cut -d':' -f 2 | cut -d. -f 1)
GITHUB_ORG = $$(echo ${GITHUB_REPOSITORY} | cut -d/ -f 1)
GITHUB_REPO = $$(echo ${GITHUB_REPOSITORY} | cut -d/ -f 2)
REQUIREMENTS = requirements.yml
COLLECTION_NAMESPACE = $$(yq -r '.namespace' < galaxy.yml)
COLLECTION_NAME = $$(yq -r '.name' < galaxy.yml)
COLLECTION_VERSION = $$(yq -r '.version' < galaxy.yml)

all: install version lint test

test: requirements
	uv run molecule test -s ${MOLECULE_SCENARIO}

install:
	@uv sync

lint: requirements
	uv run yamllint . -c .yamllint
	ANSIBLE_COLLECTIONS_PATH=$(MAKEFILE_DIR) \
	uv run ansible-lint -p playbooks/ --exclude ".ansible/*"

requirements: install
	@python --version
	ANSIBLE_COLLECTIONS_PATH=$(MAKEFILE_DIR) \
	uv run ansible-galaxy collection install \
		--force-with-deps .
	@find ./ -name "*.ymle*" -delete

ifeq (login,$(firstword $(MAKECMDGOALS)))
    LOGIN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
    $(eval $(subst $(space),,$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))):;@:)
endif

dependency create prepare converge idempotence side-effect verify destroy login reset:
	ANSIBLE_COLLECTIONS_PATH=$(MAKEFILE_DIR) \
	MOLECULE_REVISION=${MOLECULE_REVISION} \
	MOLECULE_KVM_IMAGE=${MOLECULE_KVM_IMAGE} \
	MOLECULE_DOCKER_IMAGE=${MOLECULE_DOCKER_IMAGE} \
	uv run molecule $@ -s ${MOLECULE_SCENARIO} ${LOGIN_ARGS}

rebuild: destroy prepare create

ignore:
	uv run ansible-lint --generate-ignore

clean: destroy reset
	uv env remove $$(which python)

publish: install
	uv run ansible-galaxy collection publish --api-key ${GALAXY_API_KEY} \
		"${COLLECTION_NAMESPACE}-${COLLECTION_NAME}-${COLLECTION_VERSION}.tar.gz"

version: install
	@uv run molecule --version
