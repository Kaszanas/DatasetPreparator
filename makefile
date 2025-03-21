CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))

# Docker variables:
DOCKER_DIR = ./docker
DOCKER_FILE = $(DOCKER_DIR)/Dockerfile
DOCKER_FILE_DEV = $(DOCKER_DIR)/Dockerfile.dev

# Local devcontainer
DEVCONTAINER = datasetpreparator:devcontainer
DEV_BRANCH_CONTAINER = kaszanas/datasetpreparator:dev

# Compose variables:
TEST_COMPOSE = $(DOCKER_DIR)/docker-test-compose.yml
COMPOSE_PROJECT_NAME = datasetpreparator

# Python variables:
PYTHON_VERSION = 3.11

TEST_COMMAND_RAW = poetry run pytest --durations=100 --ignore-glob='test_*.py' tests --cov=datasetpreparator --cov-report term-missing --cov-report html 2>&1

TEST_COMMAND = "$(TEST_COMMAND_RAW)"

TEST_COMMAND_LOG = "poetry run pytest --durations=100 --ignore-glob='test_*.py' tests --cov=datasetpreparator --cov-report term-missing --cov-report html 2>&1 | tee /app/logs/test_output.log"

###################
#### PIPELINE #####
###################
.PHONY: sc2reset_sc2egset_pipeline
sc2reset_sc2egset_pipeline: ## Runs the entire processing pipeline to recreate SC2ReSet and SC2EGSet or any other dataset using our standard tooling.
	@echo "Running the entire processing pipeline."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 sc2egset_pipeline.py \
		--input_path ./processing/input/directory_flattener \
		--output_path ./processing/output \
		--maps_path ./processing/maps \
		--n_processes 12 \
		--force_overwrite True

.PHONY: sc2reset_sc2egset_pipeline_dev
sc2reset_sc2egset_pipeline_dev: ## Runs the entire processing pipeline to recreate SC2ReSet and SC2EGSet or any other dataset using our standard tooling.
	@echo "Running the entire processing pipeline."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 sc2egset_pipeline.py \
		--input_path ./processing/input/directory_flattener \
		--output_path ./processing/output \
		--maps_path ./processing/maps \
		--n_processes 12 \
		--force_overwrite True


.PHONY: flatten
flatten: ## Flattens the directory if the files are held in nested directories. This helps with streamlining the processing.
	@echo "Flattening the directory structure."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 directory_flattener.py \
		--input_path ./processing/input/directory_flattener \
		--output_path ./processing/output/directory_flattener \
		--n_threads 12 \
		--force_overwrite True

.PHONY: flatten_dev
flatten_dev: ## Flattens the directory using the development container
	@echo "Flattening the directory structure."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 directory_flattener.py \
		--input_path ./processing/input/directory_flattener \
		--output_path ./processing/output/directory_flattener \
		--n_threads 12 \
		--force_overwrite True


.PHONY: process_replaypacks
process_replaypacks: ## Parses the raw (.SC2Replay) data into JSON files.
	@echo "Processing the replaypacks."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm\
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 sc2egset_replaypack_processor.py \
		--input_path ./processing/output/directory_flattener \
		--output_path ./processing/output/sc2egset_replaypack_processor \
		--maps_path ./processing/maps \
		--n_processes 12 \
		--force_overwrite True \


.PHONY: process_replaypacks_dev
process_replaypacks_dev: ## Parses the raw (.SC2Replay) data into JSON files.
	@echo "Processing the replaypacks."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm\
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 sc2egset_replaypack_processor.py \
		--input_path ./processing/output/directory_flattener \
		--output_path ./processing/output/sc2egset_replaypack_processor \
		--maps_path ./processing/maps \
		--n_processes 12 \
		--force_overwrite True \

.PHONY: processed_mapping_copier
processed_mapping_copier: ## Copies the processed mapping files.
	@echo "Copying the processed mapping files."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm\
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 processed_mapping_copier.py \
		--input_path ./processing/output/directory_flattener \
		--output_path ./processing/output/sc2egset_replaypack_processor

.PHONY: processed_mapping_copier_dev
processed_mapping_copier_dev: ## Copies the processed mapping files using the devcontainer.
	@echo "Copying the processed mapping files."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker run --rm\
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 processed_mapping_copier.py \
		--input_path ./processing/output/directory_flattener \
		--output_path ./processing/output/sc2egset_replaypack_processor

.PHONY: rename_files
rename_files: ## Renames the files after processing with SC2InfoExtractorGo.
	@echo "Renaming the files."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run \
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 file_renamer.py \
		--input_path ./processing/output/sc2egset_replaypack_processor

.PHONY: rename_files_dev
rename_files_dev: ## Renames the files after processing with SC2InfoExtractorGo.
	@echo "Renaming the files."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker run \
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 file_renamer.py \
		--input_path ./processing/output/sc2egset_replaypack_processor

.PHONY: package_sc2reset_dataset
package_sc2reset_dataset: ## Packages the raw data. Used to prepare SC2ReSet Replaypack set.
	@echo "Packaging the dataset."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 directory_packager.py \
		--input_path ./processing/output/directory_flattener
		--n_threads 12

.PHONY: package_sc2reset_dataset_dev
package_sc2reset_dataset_dev: ## Packages the raw data using the devcontainer. Used to prepare SC2ReSet Replaypack set.
	@echo "Packaging the dataset."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 directory_packager.py \
		--input_path ./processing/output/directory_flattener \
		--n_threads 12


.PHONY: package_sc2egset_dataset
package_sc2egset_dataset: ## Packages the pre-processed dataset from the output of datasetpreparator. Used to prepare SC2EGSet Dataset.
	@echo "Packaging the dataset."
	@make docker_pull_dev
	@echo "Using the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEV_BRANCH_CONTAINER) \
		python3 directory_packager.py \
		--input_path ./processing/output/sc2egset_replaypack_processor

.PHONY: package_sc2egset_dataset_dev
package_sc2egset_dataset_dev: ## Packages the SC2EGSet dataset using the devcontainer.
	@echo "Packaging the dataset."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker run --rm \
		-v ".\processing:/app/processing" \
		$(DEVCONTAINER) \
		python3 directory_packager.py \
		--input_path ./processing/output/sc2egset_replaypack_processor


###################
#### LOCAL ########
###################
.PHONY: test
test: ## Runs the tests using the local environment.
	@echo "Running the tests using the local environment."
	@echo "Using the test command: $(TEST_COMMAND)"
	$(TEST_COMMAND_RAW)


###################
#### DOCKER #######
###################
.PHONY: create_temp_container
create_temp_container:
	@echo "Creating a temporary container."
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	docker create --name temp_container $(DEVCONTAINER)

.PHONY: remove_temp_container
remove_temp_container:
	@echo "Removing the temporary container."
	docker rm temp_container

.PHONY: seed_maps_locally
seed_maps_locally:
	@echo "Seeding the maps locally."
	@make docker_build_devcontainer
	@echo "Using the dev branch Docker image: $(DEVCONTAINER)"
	@make create_temp_container
	docker cp \
		temp_container:/app/processing/maps \
		$(CURRENT_DIR)processing
	@make remove_temp_container

.PHONY: docker_pull
docker_pull_dev: ## Pulls the latest image from the Docker Hub.
	@echo "Pulling the dev branch Docker image: $(DEV_BRANCH_CONTAINER)"
	docker pull $(DEV_BRANCH_CONTAINER)

.PHONY: docker_build
docker_build: ## Builds the image containing all of the tools.
	@echo "Building the Dockerfile: $(DOCKER_FILE)"
	@echo "Using Python version: $(PYTHON_VERSION)"
	docker build \
		--build-arg="PYTHON_VERSION=$(PYTHON_VERSION)" \
		-f $(DOCKER_FILE) . \
		--tag=datasetpreparator

.PHONY: docker_build_devcontainer
docker_build_devcontainer: ## Builds the development image containing all of the tools.
	docker build \
		--build-arg="PYTHON_VERSION=$(PYTHON_VERSION)" \
		-f $(DOCKER_FILE_DEV) . \
		--tag=$(DEVCONTAINER)

.PHONY: docker_run_test
docker_run_test: ## Runs the test command using Docker.
	docker run --rm \
		$(DEVCONTAINER) \
		sh -c \
		$(TEST_COMMAND)

.PHONY: docker_run_dev
docker_run_dev: ## Runs the development image containing all of the tools.
	@echo "Running the devcontainer image: $(DEVCONTAINER)"
	docker run \
		-v ".:/app" \
		-it \
		-e "TEST_WORKSPACE=/app" \
		$(DEVCONTAINER) \
		bash

###################
#### DOCS #########
###################
.PHONY: doc_serve
doc_serve: ## Serves the Mkdocs documentation locally.
	@echo "Serving the Mkdocs documentation."
	poetry run mkdocs serve

.PHONY: doc_build
doc_build: ## Builds the Mkdocs documentation.
	@echo "Building the Mkdocs documentation."
	poetry run mkdocs build

.PHONY: docker_doc_build
docker_doc_build: ## Builds the Mkdocs documentation using Docker.
	@echo "Building the Mkdocs documentation using Docker."
	@make docker_build_devcontainer
	@echo "Using the devcontainer image: $(DEVCONTAINER)"
	docker run \
		-v ".\docs:/docs" \
		$(DEVCONTAINER) \
		poetry run mkdocs build

.PHONY: docker_doc_build_action
docker_doc_build_action: ## Builds the Mkdocs documentation using Docker.
	@echo "Building the Mkdocs documentation using Docker."
	@make docker_build_devcontainer
	@echo "Using the devcontainer image: $(DEVCONTAINER)"
	docker run \
		-v "docs:/docs" \
		$(DEVCONTAINER) \
		poetry run mkdocs build

###################
#### PRE-COMMIT ###
###################
.PHONY: docker_pre_commit
docker_pre_commit: ## Runs pre-commit hooks using Docker.
	@echo "Running pre-commit hooks using Docker."
	@make docker_build_devcontainer
	@echo "Using the devcontainer image: $(DEVCONTAINER)"
	docker run \
		-v ".:/app" \
		$(DEVCONTAINER) \
		pre-commit run --all-files

.PHONY: docker_pre_commit_action
docker_pre_commit_action: ## Runs pre-commit hooks using Docker.
	@echo "Running pre-commit hooks using Docker."
	@make docker_build_devcontainer
	@echo "Using the devcontainer image: $(DEVCONTAINER)"
	docker run \
		$(DEVCONTAINER) \
		pre-commit run --all-files

###################
#### TESTING ######
###################
.PHONY: compose_build
compose_build: ## Builds the Docker Image with docker-compose.
	@echo "Building the Docker Image with docker-compose."
	@echo "Using the test compose file: $(TEST_COMPOSE)"
	docker compose \
		-p $(COMPOSE_PROJECT_NAME) \
		-f $(TEST_COMPOSE) \
		build

.PHONY: action_compose_test
action_compose_test: ## Runs the tests using Docker.
	@echo "Running the tests using Docker."
	@echo "Using the test compose file: $(TEST_COMPOSE)"
	docker compose -p $(COMPOSE_PROJECT_NAME) -f $(TEST_COMPOSE) run --rm lib \
	bash -c $(TEST_COMMAND) --exit-code-from lib

.PHONY: compose_remove
compose_remove: ## Stops and removes the testing containers, images, volumes.
	@echo "Stopping and removing the testing containers, images, volumes."
	@echo "Using the test compose file: $(TEST_COMPOSE)"
	docker compose \
		-p $(COMPOSE_PROJECT_NAME) \
		-f $(TEST_COMPOSE) \
		down --volumes \
		--remove-orphans

.PHONY: compose_test
compose_test: compose_build action_compose_test compose_remove

.PHONY: help
help: ## Show available make targets
	@awk '/^[^\t ]*:.*?##/{sub(/:.*?##/, ""); printf "\033[36m%-30s\033[0m %s\n", $$1, substr($$0, index($$0,$$2))}' $(MAKEFILE_LIST)
