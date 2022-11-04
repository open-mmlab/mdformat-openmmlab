# mdformat-openmmlab

[![Build Status][ci-badge]][ci-link]
[![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for OpenMMLab standard.

## How to use it

Add the follow section to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/executablebooks/mdformat
    # To be compatible with Python 3.6, specify the version here.
    rev: 0.7.9
    hooks:
      - id: mdformat
        args: ["--number", "--table-width", "200"]
        additional_dependencies:
          - mdformat-openmmlab
          - mdformat_frontmatter
          - linkify-it-py
```

The argument `--table-width` is used to limit the max width of tables.

If you want to avoid escaping some symbols, you can use `--disable-escape` and specify the symbols to skip.

For example, to avoid escaping backslash (`\`) and uri-enclosure (`<`).

```yaml
  - repo: https://github.com/executablebooks/mdformat
    # To be compatible with Python 3.6, specify the version here.
    rev: 0.7.9
    hooks:
      - id: mdformat
        args: ["--number", "--table-width", "200", "--disable-escape", "backslash", "uri-enclosure"]
        additional_dependencies:
          - "mdformat-openmmlab>=0.0.2"
          - mdformat_frontmatter
          - linkify-it-py
```

Here are available options:

- `backslash` (`\`)
- `asterisk` (`*`)
- `underscore` (`_`)
- `link-enclosure` (`[` and `]`)
- `uri-enclosure` (`<`)

ATTENTION: This plugin already include all functionalities of `mdformat-gfm` and `mdformat-tables`, and is
not compatible with them, please don't install them again.

## Development

This package utilises [flit](https://flit.readthedocs.io) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To install these development dependencies:

```bash
pip install tox
```

To run the tests:

```bash
tox
```

and with test coverage:

```bash
tox -e py37-cov
```

The easiest way to write tests, is to edit tests/fixtures.md

To run the code formatting and style checks:

```bash
tox -e py37-pre-commit
```

or directly

```bash
pip install pre-commit
pre-commit run --all
```

To run the pre-commit hook test:

```bash
tox -e py37-hook
```

## Publish to PyPi

Either use flit directly:

```bash
pip install flit
flit publish
```

or trigger the GitHub Action job, by creating a release with a tag equal to the version, e.g. `v0.0.1`.

Note, this requires generating an API key on PyPi and adding it to the repository `Settings/Secrets`, under the name `PYPI_KEY`.

[ci-badge]: https://github.com/open-mmlab/mdformat-openmmlab/workflows/CI/badge.svg?branch=master
[ci-link]: https://github.com/open-mmlab/mdformat-openmmlab/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-openmmlab.svg
[pypi-link]: https://pypi.org/project/mdformat-openmmlab
