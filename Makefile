include make/Makefile.database
include make/Makefile.backend
include make/Makefile.edge
include make/Makefile.db_gateway

.PHONY: help
help:
	@echo "Usage: make [target]"
	@grep -hE '^[a-zA-Z_-]+:.*?##' make/Makefile.* | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'