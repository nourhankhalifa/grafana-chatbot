CHATBOT_DIR := chatbot-panel-plugin

.PHONY: help install build test clean fmt

help:
	@echo "Makefile for chatbot-panel plugin"
	@echo "Targets: install build test clean fmt"

install:
	@echo "Installing dependencies for $(CHATBOT_DIR)..."
	# Ensure a package-lock exists for consistent installs and audit commands
	if [ ! -f $(CHATBOT_DIR)/package-lock.json ]; then \
		if [ -f $(CHATBOT_DIR)/package.json ]; then \
			cd $(CHATBOT_DIR) && npm i --package-lock-only; \
		else \
			echo "Warning: $(CHATBOT_DIR)/package.json not found; skipping lockfile creation"; \
		fi \
	fi
	cd $(CHATBOT_DIR) && npm ci

build:
	@echo "Building plugin in $(CHATBOT_DIR)..."
	cd $(CHATBOT_DIR) && npm run build

test:
	@echo "Running tests for $(CHATBOT_DIR)..."
	cd $(CHATBOT_DIR) && npm test --silent

clean:
	@echo "Cleaning dist and node_modules for $(CHATBOT_DIR)..."
	rm -rf $(CHATBOT_DIR)/dist $(CHATBOT_DIR)/node_modules

fmt:
	@echo "Formatting not configured; add formatting steps here if desired"
