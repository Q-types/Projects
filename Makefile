# ========= Project Makefile (Data Science + Time Series, macOS/conda) =========
# Default goal shows help
.DEFAULT_GOAL := help

# ---- Config ----
ENV ?= base_ds
PY := conda run -n $(ENV) python
PIP := conda run -n $(ENV) pip
JUPYTER := conda run -n $(ENV) jupyter

DATA_DIR := data_science/datasets
RAW := $(DATA_DIR)/raw
PROCESSED := $(DATA_DIR)/processed
MODELS := data_science/models
REPORTS := data_science/reports

# ---- Helpers ----
## help: show this help
help:
	@echo "Useful targets:"
	@awk 'BEGIN {FS":.*##"; printf "\n  make \033[36m%-22s\033[0m %s\n","help","show this help"} \
	     /^[a-zA-Z0-9_-]+:.*##/ { printf "  make \033[36m%-22s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# ---- Environment & Jupyter ----
## env-create: create the conda env from environment.yml
env-create:
	conda env create -f environment.yml || true
	$(MAKE) kernel

## env-update: update existing env to match environment.yml (removes extras)
env-update:
	conda env update -n $(ENV) -f environment.yml --prune
	$(MAKE) kernel

## env-export: export only top-level deps to environment.yml
env-export:
	conda env export --from-history -n $(ENV) > environment.yml

## kernel: register Jupyter kernel for this env
kernel:
	$(PY) -m ipykernel install --user --name $(ENV) --display-name "Python ($(ENV))" --force

## lab: launch JupyterLab using the env kernel
lab:
	$(JUPYTER) lab

# ---- Project Scaffolding ----
## init: create standard folders (idempotent)
init:
	mkdir -p $(RAW) $(PROCESSED) $(MODELS) $(REPORTS) data_science/{configs,notebooks,scripts,tests} research/{experiments,papers} utils

# ---- Code Quality ----
## lint: run ruff (lint) and black (check only)
lint:
	conda run -n $(ENV) ruff check .
	conda run -n $(ENV) black --check .

## fmt: format with black
fmt:
	conda run -n $(ENV) black .

# ---- Data & Pipelines (DVC optional) ----
## dvc-status: show DVC status
dvc-status:
	dvc status

## dvc-pull: fetch data/model artifacts
dvc-pull:
	dvc pull

## dvc-push: push data/model artifacts
dvc-push:
	dvc push

## repro: reproduce the full pipeline (if you add dvc.yaml)
repro:
	dvc repro

# ---- Example workflow hooks (adjust scripts as you add them) ----
## preprocess: run your data preprocessing script
preprocess:
	$(PY) data_science/scripts/preprocess.py --in $(RAW) --out $(PROCESSED) || true

## train: run model training script
train:
	$(PY) data_science/scripts/train.py --data $(PROCESSED) --models $(MODELS) || true

## eval: run evaluation script and save to reports/
eval:
	$(PY) data_science/scripts/evaluate.py --models $(MODELS) --out $(REPORTS) || true

# ---- Testing ----
## test: run pytest if present (won't fail the whole make if missing)
test:
	-$(PY) -m pytest -q

# ---- Utilities ----
## clean: remove caches, temp files, and Python artifacts
clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete || true
	rm -rf .pytest_cache .ipynb_checkpoints tmp || true