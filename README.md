Repository Overview

Purpose: Grafana panel plugin scaffold for a "chatbot" panel. The plugin follows Grafana best-practice layout for a React/TypeScript panel.
Top-level

README.md: Project-level documentation and usage notes.
chatbot-panel/: Plugin package directory (contains the plugin source, build config, and package metadata).
chatbot-panel (key files)

package.json: NPM manifest for the plugin — scripts, dependencies, build/publish settings, Grafana plugin metadata hooks.
tsconfig.json: TypeScript compiler options for building the plugin.
jest.config.js: Jest configuration for running unit tests.
LICENSE and CHANGELOG.md: Licensing and change history for the plugin package.
README.md: Plugin-specific documentation, install/build instructions and Grafana integration notes.
plugin.json: Grafana plugin descriptor (ID, panels, dependencies, info that Grafana reads to register the plugin).
src/: TypeScript source for the plugin.
ChatPanel.tsx: The React component implementing the panel UI (the runtime panel code).
module.ts: Grafana plugin module bootstrap (registers the panel with Grafana).
module.test.ts: Unit tests for module-related logic (runs under Jest).
types.ts: Shared TypeScript types/interfaces used by the panel (props, options, data shapes).
img/: Static images/assets used by the plugin UI or docs.