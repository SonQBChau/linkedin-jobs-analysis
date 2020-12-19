# Scraping LinkedIn

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
