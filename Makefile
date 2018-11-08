BLACK ?= \033[0;30m
RED ?= \033[0;31m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
BLUE ?= \033[0;34m
PURPLE ?= \033[0;35m
CYAN ?= \033[0;36m
GRAY ?= \033[0;37m
COFF ?= \033[0m

# Mark non-file targets as PHONY
.PHONY: all help shell makemigrations migrate isort isort-fix prospector test quality check
all: help

help:
	@echo "======                                     Tasks                                    ======"
	@echo ""
	@echo "$(CYAN)make migrate$(COFF)   - Run migrations"
	@echo ""
	@echo "$(CYAN)make makemigrations$(COFF)   - Make new migrations after model changes"
	@echo ""
	@echo "$(CYAN)make shell$(COFF)     - Run python shell inside docker"
	@echo ""
	@echo "$(CYAN)make isort$(COFF)     - Check imports"
	@echo ""
	@echo "$(CYAN)make isort-fix$(COFF) - Fix imports automatically with isort"
	@echo ""
	@echo "$(CYAN)make test$(COFF)      - Run automated tests"
	@echo ""
	@echo "$(CYAN)make quality$(COFF)   - Check code quality"
	@echo ""

shell:
	docker-compose run --rm django python manage.py shell

makemigrations:
	docker-compose run --rm django python manage.py makemigrations $(cmd)

migrate:
	docker-compose run --rm django python manage.py migrate $(cmd)

prospector:
	@echo "$(CYAN)Running Prospector$(COFF)"
	@docker-compose run --rm django prospector

isort:
	@echo "$(CYAN)Checking imports with isort$(COFF)"
	docker-compose run --rm django isort --recursive --check-only -p . --diff

isort-fix:
	@echo "$(CYAN)Fixing imports with isort$(COFF)"
	docker-compose run --rm django isort --recursive -p .

test:
	@echo "$(CYAN)Running automated tests$(COFF)"
	docker-compose run --rm django python manage.py test

quality: prospector isort

check: prospector isort test