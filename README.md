# A Grafana Chatbot Panel Plugin

Purpose: Grafana panel plugin for a "chatbot" panel. The plugin follows Grafana best-practice layout for a React/TypeScript panel.

Repository layout:

```sh
.
├── chatbot-panel-plugin
│   ├── CHANGELOG.md         # Change log for the plugin
│   ├── jest.config.js       # Jest configuration for tests
│   ├── LICENSE              # License file
│   ├── package-lock.json    # Exact dependency versions (lockfile)
│   ├── package.json         # NPM manifest and scripts
│   ├── README.md            # Plugin-specific documentation
│   ├── src
│   │   ├── ChatPanel.tsx    # React component implementing the panel UI
│   │   ├── img
│   │   │   └── logo.svg     # Static image assets
│   │   ├── module.test.ts   # Unit tests for module-related logic
│   │   ├── module.ts        # Grafana plugin bootstrap/register
│   │   ├── plugin.json      # Grafana plugin descriptor
│   │   └── types.ts         # Shared TypeScript types/interfaces
│   └── tsconfig.json        # TypeScript compiler options
└── README.md                # This file (project overview)
```

Key files explained:

- **ChatPanel.tsx**: The React component that renders the Grafana panel UI. It contains the runtime code for drawing the panel and handling interactions.
- **module.ts**: Registers the panel with Grafana and wires up plugin lifecycle behavior.
- **plugin.json**: Grafana descriptor that declares the plugin ID, panels, dependencies, and UI hooks Grafana uses to surface the plugin.
- **module.test.ts**: Unit tests for the module and registration logic; run with Jest.
- **types.ts**: Shared TypeScript definitions used across the plugin (props, options, and data shapes).
- **package.json**: Declares scripts for building, testing, and packaging the panel; lists dependencies used during build and runtime.
- **tsconfig.json**: Compiler options to build the project with TypeScript and generate output compatible with Grafana's build environment.
- **jest.config.js**: Test runner configuration used by Jest when running unit tests.
- **CHANGELOG.md**: Lists notable changes between releases of the plugin.
- **LICENSE**: The project's license and copyright terms.

## Build & test

This repository includes a top-level `Makefile`. Use these targets from the repository root.

Example commands:

```sh
make install # install exact dependencies

make build # build the plugin

make test # run unit tests

make clean # clean build artifacts and node_modules
```
