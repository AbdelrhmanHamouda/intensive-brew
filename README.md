# intensive brew

Simple cli tool that converts a simple yaml into a compatible Locust Kubernetes Operator custom resource.

## Using

To add and install this package as a dependency of your project, run `poetry add intensive-brew`.

To view this app's commands once it's installed, run `intensive-brew --help`. Alternatively, you can also use `docker compose run --rm app --help`.

## Contributing

<details>
<summary>Setup: once per device</summary>

1. [Install Docker Desktop](https://www.docker.com/get-started).
   - Enable _Use Docker Compose V2_ in Docker Desktop's preferences window.
2. Install [Poetry](https://python-poetry.org/docs/#installation).
3. Install [Pre-commit](https://pre-commit.com/#install)
   - On macOS run: `brew install pre-commit`

</details>


<details>
<summary>Developing</summary>

- Clone repository
- Setup development environment
   - Stage 1: setup _IntelliJ_ to work with the project
      - [prerequisite] [Python plugin](https://plugins.jetbrains.com/plugin/631-python) for _IntelliJ_ from _JetBrains_.
      - Step 1: in _IntelliJ_ go to `File` → `Project Structure` → `SDKs` → <kbd>+</kbd> → `Add Python SDK...` → `Poetry Environment`
        → `OK`
         - An environment will be instantiated and dependencies will be installed
      - Step 2: Select the created SDK as the SDK for the project
         - `File` → `Project Structure` → `Project` → `SDK` → `SDK with project name`
   - Stage 2: from the terminal
      - `cd` to the repository location
      - Install _git_ pre-commit hooks
        ```sh
        pre-commit install --install-hooks
        ```

###### Documentation
The project uses [mkdocs.org](https://www.mkdocs.org) to build and maintain its documentation. 

-  Commands
   - `mkdocs new [dir-name]` - Create a new project.
   - `mkdocs serve` - Start the live-reloading docs server.
   - `mkdocs build` - Build the documentation site.
   - `mkdocs -h` - Print help message and exit.

- Project layout
  ```
  mkdocs.yml    # The configuration file.
  docs/
    index.md      # The documentation homepage.
    ...           # Other markdown pages, images and other files.
  ```

###### General information

- This project follows the [Conventional Commits](https://www.conventionalcommits.org/) standard to
  automate [Semantic Versioning](https://semver.org/) and [Keep A Changelog](https://keepachangelog.com/)
  with [Commitizen](https://github.com/commitizen-tools/commitizen).
- Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available
  to run on this project.
- Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml`
  and `poetry.lock`. Add `--group test` or `--group dev` to install a CI or development dependency, respectively.
- Run `poetry remove {package}` from within the development environment to uninstall a run time dependency and remove it
  from `pyproject.toml` and `poetry.lock`. Add `--group test` or `--group dev` to uninstall a CI or development dependency, respectively.
- Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.
- Run `cz bump` to bump the package's version, update the `CHANGELOG.md`, and create a git tag.
- Project has a protection against pushing to `main/msater` branches by utilizing pre-commit hooks.
</details>
