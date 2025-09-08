# # # Setting up Makefile behavior
.SILENT:

# === CONSTRAINTS ===
DOCKER = docker
COMPOSE = $(DOCKER) compose

EXEC_SERVICE = exec-service

include ./resources/scripts/makefile/dev.mk
include ./resources/scripts/makefile/ci.mk
