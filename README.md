# csce-5214-p3

Scraping LinkedIn job posts and doing things with them.

### Python Environment

This project uses [Poetry](https://python-poetry.org/) to manage its Python environment. Install it with the following command taken from its docs:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

The current Poetry environment requires Python 3.8 or above. If you have difficulty satisfying that requirement, I highly recommend [pyenv](https://github.com/pyenv/pyenv) for managing your various system Python installations:

```bash
curl https://pyenv.run | bash
```

See [here](https://github.com/pyenv/pyenv/wiki/Common-build-problems) for pyenv's prerequisites if the above command does not work, as well as [the installer docs](https://github.com/pyenv/pyenv-installer) for additional configuration steps.

Once Poetry and/or pyenv are working, you can set up a Poetry environment for this project by executing

```bash
poetry install
```

inside your local repo directory (the one that contains pyproject.toml).

If and when you need to add or remove packages, the commands are `poetry add <package-name>` and `poetry remove <package-name>`. See Poetry's docs or `poetry --help` or `poetry COMMAND --help` for further info.

If `poetry install` gets as far as installing orjson (one of FastAPI's optional dependencies) but fails with Rust errors, try the following:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh # if you really don't have Rust installed
rustup default nightly # if it complains about stable rustc not having the -Z flag
```
