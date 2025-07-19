SHELL := /bin/bash
HIDE ?= @

.PHONY: build test

name := "mockhub"
port := 11915

gen:
	-$(HIDE)rm -rf .venv
	$(HIDE)uv venv .venv --python=3.12.10
	$(HIDE)source .venv/bin/activate && uv sync

fix:
	$(HIDE)source .venv/bin/activate && uv run ruff format
	$(HIDE)source .venv/bin/activate && uv run ruff check --fix

check:
	$(HIDE)source .venv/bin/activate && MYPY_FORCE_COLOR=1 uv run mypy src/ --color-output | grep --color=always -v "note:"

dev:
	$(HIDE)source .venv/bin/activate && uv run uvicorn src.main:app --port $(port) --reload --host 0.0.0.0
