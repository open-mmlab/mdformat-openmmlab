# mdformat-openmmlab

[![Build Status][ci-badge]][ci-link]
[![codecov.io][cov-badge]][cov-link]
[![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for OpenMMLab standard.

## How to use it

Add the follow section to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.14
    hooks:
      - id: mdformat
        args: ["--number", "--table-width", "200"]
        additional_dependencies:
          - git+https://github.com/mzr1996/mdformat-openmmlab.git#egg=mdformat-openmmlab
          - mdformat_frontmatter
          - linkify-it-py
```

The argument `--table-width` is used to limit the max width of tables.

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

[ci-badge]: https://github.com/executablebooks/mdformat-plugin/workflows/CI/badge.svg?branch=master
[ci-link]: https://github.com/executablebooks/mdformat/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush
[cov-badge]: https://codecov.io/gh/executablebooks/mdformat-plugin/branch/master/graph/badge.svg
[cov-link]: https://codecov.io/gh/executablebooks/mdformat-plugin
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-plugin.svg
[pypi-link]: https://pypi.org/project/mdformat-plugin
