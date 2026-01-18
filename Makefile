.PHONY: setup test lint build show clean help

.DEFAULT_GOAL:= help

PY:= uv run python
BUILD_DIR:= build
GDS_DIR:= $(BUILD_DIR)/gds


setup: ## Install/sync environment from lockfile
	uv sync

init: ## Initialize project (rename from template)
	$(PY) scripts/init.py

test: ## Run smoke tests
	uv run pytest -q

lint: ## Lint source code
	uv run ruff check src


build: ## Export GDS files
	$(PY) scripts/build_top.py

show: ## Open interactive viewer for top()
	$(PY) -c "import gdsfactory as gf; from pic_template.chips.top import top; gf.show(top())"


clean: ## Remove generated files
	rm -rf build

drc: ## Run design rule check (OPEN=1 to open KLayout on violations)
	OPEN=$(OPEN) $(PY) src/pic_template/flows/run_drc.py

drc-gui: ## Run design rule check with GUI
	OPEN=1 $(MAKE) drc

verify: ## Run comprehensive verification flow (DRC + geometry)
	$(PY) -m pic_template.flows.verify

verify-enhanced: ## Run verification with enhanced DRC rules
	$(PY) -m pic_template.flows.verify --enhanced

geometry: ## Print geometry check results as JSON
	$(PY) -c "import json; from pic_template.flows.geometry_check import GeometryChecker; from pic_template.chips.top import top; print(json.dumps(GeometryChecker(top()).run_all_checks(is_top_level=True), indent=2))"

help:
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'
