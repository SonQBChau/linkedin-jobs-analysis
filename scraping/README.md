# Scraping LinkedIn

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


## Setting up Scrapy

This project uses Poetry for environment and dependency management. See the parent directory's README.md for instructions on setting it up.

## Commands used for final crawl:

`cd` into scraping (this directory) and enter `poetry shell`. Then execute the following commands, in any order, with 30 minutes to an hour between each one.

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=data scientist&location=new york, united states' --pipelines --depth 2 -o dsny.json --logfile dsny.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=data scientist&location=california, united states' --pipelines --depth 2 -o dsca.json --logfile dsca.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=data scientist&location=texas, united states' --pipelines --depth 2 -o dstx.json --logfile dstx.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=data engineer&location=new york, united states' --pipelines --depth 2 -o deny.json --logfile deny.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=data engineer&location=california, united states' --pipelines --depth 2 -o deca.json --logfile deca.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=data engineer&location=texas, united states' --pipelines --depth 2 -o detx.json --logfile detx.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=mobile application developer&location=new york, united states' --pipelines --depth 2 -o madny.json --logfile madny.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=mobile application developer&location=california, united states' --pipelines --depth 2 -o madca.json --logfile madca.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=mobile application developer&location=texas, united states' --pipelines --depth 2 -o madtx.json --logfile madtx.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=web developer&location=new york, united states' --pipelines --depth 2 -o wdny.json --logfile wdny.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=web developer&location=california, united states' --pipelines --depth 2 -o wdca.json --logfile wdca.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=web developer&location=texas, united states' --pipelines --depth 2 -o wdtx.json --logfile wdtx.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=machine learning engineer&location=new york, united states' --pipelines --depth 2 -o mleny.json --logfile mleny.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=machine learning engineer&location=california, united states' --pipelines --depth 2 -o mleca.json --logfile mleca.txt
```

```bash
scrapy parse 'https://www.linkedin.com/jobs/search/?keywords=machine learning engineer&location=texas, united states' --pipelines --depth 2 -o mletx.json --logfile mletx.txt
```
