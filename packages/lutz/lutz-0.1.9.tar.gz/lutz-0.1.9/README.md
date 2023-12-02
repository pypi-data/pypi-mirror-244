# Python package with Rust

Python package with some functions in Rust using [PyO3](https://pyo3.rs/) and [Maturin](https://www.maturin.rs/).
Maturin was made for all Rust python packages.
How mixed packages work is mentioned [in the README](https://github.com/PyO3/maturin/tree/main#mixed-rustpython-projects).
Some fiddling has to be done with the project structure, [Cargo.toml](./Cargo.toml), [pyproject.toml](./pyproject.toml)
to get everything right.
It should be possible to:
1. test the package locally (after building the Rust part)
2. buid the package with both Rust and Python

## Development Setup

Install all dependencies including [Maturin](https://www.maturin.rs/).

```
# using conda environments here
conda env create -f environment.yml
conda activate lutz
```

There is a python package [python/lutz/](./python/lutz/)
and a Rust library [rust/lib.rs](./rust/lib.rs).
In [lib.rs](./rust/lib.rs) a python module is implemented which is referenced in
[Cargo.toml](./Cargo.toml) in `lib.name`.

```
# build rust library
maturin develop
```

The library is build and a resulting `_lib.*.so` file is placed in [python/lutz](./python/lutz/).
This is defined in [pyproject.toml](./pyproject.toml) under `[tool.maturin]`.
From now on rust functions can be imported as private `_lib`.
I wrote a wrapper in [python/lutz/rust.py](./python/lutz/rust.py).

Both [Cargo.toml](./Cargo.toml) and [pyproject.toml](./pyproject.toml) define package name
and version number but [pyproject.toml](./pyproject.toml) takes precendence.

> Note [.vscode/settings.json](./.vscode/settings.json) and [vscode.env](./vscode.env)
> is setup for being able to import *lutz* from the integrated python terminal
> and Jupyter notebooks, as well as tell pylint how to import *lutz*.

## Tests

Using [pytest](https://docs.pytest.org/) python test suite.
`_lib.*.so` in *python/lutz/* must have been built before
(`maturin develop`).

```
pytest tests
```

## Build and release

Maturin can build and publish the package wheel and source distribution.
By default the `--release` flag is used for building the rust library (performance optimizations)
and files are uploaded to pypi.org.

```
maturin publish
```

The above will only create a wheel for this architecture, platform, and python version.
More generic releases are explained in the [Maturin tutorial](https://www.maturin.rs/distribution.html).
There are some caveats with each platform.
To make things simple, Maturin offers a command to generate a CI workflow for different platforms.
Here, I am generating a github workflow for publishing.

```
mkdir -p .github/workflows
maturin generate-ci --pytest github > .github/workflows/CI.yml
```

It uses [github/maturin-action](https://github.com/PyO3/maturin-action).
Per default it will push to pipy.org and use token authentication.
Create API token on pypi.org and add it as secret to the github repository.
As you can see in the [CI.yml](./github/workflows/CI.yml) the name of this secret should be `PYPI_API_TOKEN`.
I edited the trigger to `tags: ['v*']` to not run on every push.
Trigger with e.g.:

```
TAG='v0.1.1'
git tag "$TAG" && git push origin "$TAG"
```