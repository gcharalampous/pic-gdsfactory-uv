.PHONY: setup test lint build show clean help

.DEFAULT_GOAL:= help

PY:= uv run python
BUILD_DIR:= build
GDS_DIR:= $(BUILD_DIR)/gds


setup: ## Install/sync environment from lockfile
	uv sync

test: ## Run smoke tests
	uv run pytest -q

lint: ## Lint source code
	uv run ruff check src


build: ## Export GDS files
	mkdir -p $(GDS_DIR)
	$(PY) scripts/build_top.py

show: ## Open interactive viewer for top()
	$(PY) -c "import gdsfactory as gf; from pic_template.chips.top import top; gf.show(top())"


clean: ## Remove generated files
	rm -rf build

drc: ## Run design rule check (OPEN=1 to open KLayout on violations)
	OPEN=$(OPEN) $(PY) src/pic_template/flows/run_drc.py

drc-gui: ## Run design rule check with GUI
	OPEN=1 $(MAKE) drc

help:
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'
