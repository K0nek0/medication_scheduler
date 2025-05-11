set shell := ["powershell.exe"]

# # Directories for source code and tests
# SOURCE_DIR := "app"
# TESTS_DIR := "tests"

# Default command: list available commands
default:
    @just --list

# # Environment variables file
# set dotenv-filename := ".env"

# # Run all checks: linters and formatting validation
# lint: ruff-check mypy format-check

# --- Dependency Management ---

# Update project dependencies
[group('dependencies')]
update:
    uv pip install --upgrade -r requirements.txt

# # --- Linters and Formatting ---

# # Automatically format code
# [group('linters')]
# format:
#     uv run ruff format .

# # Check formatting without modifying files
# [group('linters')]
# format-check:
#     uv run ruff format .

# # Lint code using Ruff
# [group('linters')]
# ruff-check:
#     ruff check {{ SOURCE_DIR }}
#     ruff check {{ TESTS_DIR }}

# # Fix code using Ruff
# [group('linters')]
# ruff:
#     ruff check --fix --unsafe-fixes {{ SOURCE_DIR }}
#     ruff check --fix --unsafe-fixes {{ TESTS_DIR }}

# # Type checking using mypy
# [group('linters')]
# mypy:
#     uv run mypy .

# --- Testing ---

# # Run tests using pytest
# [group('testing')]
# tests:
#     uv run pytest tests/rest

# # --- Building ---

# # Build DataBase
# [group('building')]
# build-depends:
#     docker compose -f .docker/docker-compose-local.yml up -d --remove-orphans --build

# Generate pydantic models
generate-models:
    datamodel-codegen --input ./schemas/openapi.yaml --output ./app/models/models_auto.py --force

# Generate protoc
generate-grpc:
    python -m grpc_tools.protoc -Ischemas --python_out=app/grpc_package --grpc_python_out=app/grpc_package schemas/med_schedule.proto

# Run app
run:
    python -m app
