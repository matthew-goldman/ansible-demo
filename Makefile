.DEFAULT_GOAL := all

.PHONY: all
all: mk_dirs setup_requirements roles_up

.PHONY: help
help: ## Displays this help
	@echo "Targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | \
		sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: mk-dirs
mk_dirs: ## Creates directories for storing Ansible temporary stuff
	-mkdir tmp/

.PHONY: setup-requirements
setup_requirements: ## Installs Python requirements for Ansible and enables the virtual environment
	-python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip3 install -r requirements.txt; \
	pre-commit install; \
	ansible-galaxy install -i -r roles/requirements.yml -p roles/;\
	ansible-galaxy collection install amazon.aws community.general ansible.posix community.docker

.PHONY: clean
clean: ## Cleans up the workspace.
	@echo "Cleaning up..."
	@find roles/* -maxdepth 0 -type d ! -name development -exec rm -r -f {} \;
	@find collections/* -maxdepth 0 -type d ! -name development -exec rm -r -f {} \;
	@rm -r -f tmp/ .venv
	@echo "All Done"

.PHONY: show_role_version
show_roles_version: ## Show version from roles
	@ansible-galaxy list

.PHONY: roles_up
roles_up: ## Updates installed roles if version missmatches with the one in requirements.yml 
	-source .venv/bin/activate; \
	scripts/roles_up.py

.PHONY: roles_up_info
roles_up_info: ## Shows roles versions if version missmatches with the one in requirements.yml without performing any action 
	-source .venv/bin/activate; \
	scripts/roles_up.py --info

.PHONY: unittest_scripts
unittest_scripts: ## Run script's unittests
	-source .venv/bin/activate; \
	python -m unittest discover -s scripts/tests/ -t scripts
