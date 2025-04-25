MODE ?= dev

ifeq ($(MODE),dev)
	include make/Makefile.database.dev
	include make/Makefile.backend.dev
	include make/Makefile.edge.dev
	include make/Makefile.db_gateway.dev
	include make/Makefile.frontend.dev
else ifeq ($(MODE),prod)
	include make/Makefile.database.prod
	include make/Makefile.backend.prod
	include make/Makefile.edge.prod
	include make/Makefile.db_gateway.prod
	include make/Makefile.frontend.prod
else
  $(error Invalid MODE "$(MODE)". Use MODE=dev or MODE=prod)
endif

.PHONY: help
help:
	@echo "Usage: make [target]"
	@grep -hE '^[a-zA-Z_-]+:.*?##' make/Makefile.*.$(MODE) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'