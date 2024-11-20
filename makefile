DOCKER_DIR = ./docker
TEST_COMPOSE = $(DOCKER_DIR)/docker-test-compose.yml

PYTHON_VERSION = 3.11

TEST_COMMAND = "poetry run pytest --durations=100 --ignore-glob='test_*.py' tests --cov=datasetpreparator --cov-report term-missing --cov-report html 2>&1 | tee /app/logs/test_output.log"

###################
#### PIPELINE #####
###################
sc2reset_sc2egset: ## Runs the entire processing pipeline to recreate SC2ReSet and SC2EGSet or any other dataset using our standard tooling.
	@make flatten
	@make process_replaypacks
	@make rename_files
	@make package_sc2egset_dataset

flatten: ## Flattens the directory if the files are held in nested directories. This helps with streamlining the processing.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 directory_flattener.py

json_merge: ## Merges two JSON files.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 json_merger.py \
		--json_one=../processing/json_merger/map_translation.json \
		--json_two=../processing/json_merger/new_maps_processed.json

download_maps: ## Runs over directories with .SC2Replay files and downloads maps that were used in the games.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 sc2_map_downloader.py

process_replaypacks: ## Parses the raw (.SC2Replay) data into JSON files.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 sc2_replaypack_processor.py \
		--n_processes 8 \
		--perform_chat_anonymization "true"

rename_files: ## Renames the files after processing with SC2InfoExtractorGo.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 file_renamer.py \
		--input_dir ../processing/sc2_replaypack_processor/output

package_sc2reset_dataset: ## Packages the raw data. Used to prepare SC2ReSet Replaypack set.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 src/datasetpreparator/ file_packager.py \
		--input_dir ../processing/directory_flattener/output

package_sc2egset_dataset: ## Packages the pre-processed dataset from the output of datasetpreparator. Used to prepare SC2EGSet Dataset.
	docker run \
		-v "./processing:/app/processing" \
		datasetpreparator:latest \
		python3 file_packager.py \
		--input_dir ../processing/sc2_replaypack_processor/output

###################
#### DOCKER #######
###################
docker_build: ## Builds the image containing all of the tools.
	docker build \
	--build-arg="PYTHON_VERSION=$(PYTHON_VERSION)" \
	-f ./docker/Dockerfile . \
	--tag=datasetpreparator

docker_build_dev: ## Builds the development image containing all of the tools.
	docker build \
	--build-arg="PYTHON_VERSION=$(PYTHON_VERSION)" \
	-f ./docker/Dockerfile.dev . \
	--tag=datasetpreparator:devcontainer

docker_run_test: ## Runs the test command using Docker.
	docker run --rm \
		datasetpreparator:devcontainer \
		sh -c \
		$(TEST_COMMAND)

docker_run_dev: ## Runs the development image containing all of the tools.
	docker run \
		-v ".:/app" \
		-it \
		-e "TEST_WORKSPACE=/app" \
		datasetpreparator:devcontainer \
		bash

###################
#### DOCS #########
###################
doc_serve: ## Serves the Mkdocs documentation locally.
	poetry run mkdocs serve

doc_build: ## Builds the Mkdocs documentation.
	poetry run mkdocs build

docker_doc_build: ## Builds the Mkdocs documentation using Docker.
	docker run \
		-v "./docs:/docs" \
		datasetpreparator:devcontainer \
		poetry run mkdocs build

docker_doc_build_action: ## Builds the Mkdocs documentation using Docker.
	docker run \
		-v "./docs:/docs" \
		datasetpreparator:devcontainer \
		poetry run mkdocs build

###################
#### PRE-COMMIT ###
###################
docker_pre_commit: ## Runs pre-commit hooks using Docker.
	docker run \
		-v ".:/app" \
		datasetpreparator:devcontainer \
		pre-commit run --all-files

docker_pre_commit_action: ## Runs pre-commit hooks using Docker.
	docker run \
		datasetpreparator:devcontainer \
		pre-commit run --all-files

###################
#### TESTING ######
###################
compose_build: ## Builds the Docker Image with docker-compose.
	docker-compose -f $(TEST_COMPOSE) build

action_compose_test: ## Runs the tests using Docker.
	docker compose -f $(TEST_COMPOSE) run --rm lib \
	bash -c $(TEST_COMMAND)

compose_remove: ## Stops and removes the testing containers, images, volumes.
	docker-compose -f $(TEST_COMPOSE) down --volumes --remove-orphans

compose_test: compose_build action_compose_test compose_remove

.PHONY: help
help: ## Show available make targets
	@awk '/^[^\t ]*:.*?##/{sub(/:.*?##/, ""); printf "\033[36m%-30s\033[0m %s\n", $$1, substr($$0, index($$0,$$2))}' $(MAKEFILE_LIST)
