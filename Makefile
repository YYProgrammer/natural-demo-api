SHELL := /bin/bash
HIDE ?= @

.PHONY: help lint type-check format check all dev standards-check

name := "natural-demo-api"
port := 5001

lint:  ## Run ruff linter
	$(HIDE)ruff check src/

type-check:  ## Run mypy type checker
	$(HIDE)mypy src/

fix:  ## Fix code with ruff
	$(HIDE)ruff format src/
	$(HIDE)ruff check --fix src/

check: lint type-check  ## Run both linting and type checking

dev:  ## Start development server
	$(HIDE).venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port $(port)

gen:  ## Generate new virtual environment
# $(HIDE)@if [ ! -f .env ]; then cp make/env.example .env; fi
	$(HIDE)rm -rf .venv
	$(HIDE)uv venv .venv --python=3.12
	$(HIDE)uv sync

install:  ## Install dependencies
	$(HIDE)python3 -m venv .venv
	$(HIDE).venv/bin/pip install uv
