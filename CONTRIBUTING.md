# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Types of Contributions

### Report Bugs

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can never have enough documentation! Please feel free to contribute to any
part of the documentation, such as the official docs, docstrings, or even
on the web in blog posts, articles, and such.

### Submit Feedback

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

### Development with Docker

If you wish to develop using Docker, there is a `Dockerfile.dev` defined. Please use the following commands:

Build the Dockerfile:
```
docker build --tag=datasetpreparator:devcontainer -f .\docker\Dockerfile.dev .
```

Run the Dockerfile:
```
docker run -it -v .:/app datasetpreparator:devcontainer
```

### Local Development

Ready to contribute? Here's how to set up `datasetpreparator` for local development.

1. Download a copy of `datasetpreparator` locally.
2. Install `datasetpreparator` using `poetry`:

```console
  poetry install
```

3. Install the pre-commit hooks:

```console
  poetry run pre-commit install
```

4. Use `git` (or similar) to create a branch for local development and make your changes:

```console
  git checkout -b name-of-your-bugfix-or-feature
```

5. When you're done making changes, check that your changes conform to any code formatting requirements and pass any tests.

6. Format your commit with `commitizen`:

```console
  poetry run cz commit
```

7. Commit your changes (we are using commitizen to check commit messages) and open a pull request.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include additional tests if appropriate.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all currently supported operating systems and versions of Python.

## Code of Conduct

Please note that the `datasetpreparator` project is released
with a Contributor License Agreement (CLA)
Code of Conduct. By contributing to this project you agree to abide by its terms.
