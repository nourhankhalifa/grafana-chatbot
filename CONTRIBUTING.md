# Contributing

Thanks for your interest in contributing to this Grafana panel plugin. This document explains how to prepare contributions, run the project locally, and what we look for in pull requests.

Getting started

- Fork the repository and create a feature branch from `main`.
- Keep changes small and focused; one feature or bug fix per PR.

Local development

We provide a top-level `Makefile` to simplify common tasks. From the repository root run:

```sh
# install dependencies for the plugin
make install

# build the plugin
make build

# run the unit tests
make test

# clean build artifacts
make clean
```

If you prefer to run npm directly, change into `chatbot-panel-plugin` and run `npm ci`, `npm run build`, or `npm test`.

Code style & formatting

- The project uses TypeScript and React. Prefer `prettier` formatting and follow common TypeScript conventions.
- If the repository includes lint/format scripts, run them before opening a PR. You can add `npm run format` or `npm run lint` in your branch if needed.

Testing

- Unit tests are run with Jest. Keep tests small and deterministic.
- Add tests for bug fixes and core behaviors when possible.

Pull request checklist

- [ ] I opened the PR against the `main` branch.
- [ ] The change has a descriptive title and explanation.
- [ ] New code includes tests or an explanation why tests are not needed.
- [ ] I ran `make install`, `make build`, and `make test` locally.
- [ ] I updated relevant documentation (README, plugin metadata) if applicable.

Maintainers will review and give feedback. Thank you for your contribution!
