# Neo4j Test - arXiv dataset

A python project using uv for interacting with a Neo4j database.

## Prerequisites

- Git
- Python >= 3.12 (prefer using [asdf](https://asdf-vm.com/), [pyenv](https://github.com/pyenv/pyenv) or [uv managed versions](https://docs.astral.sh/uv/concepts/python-versions/) to system python)
- [uv](https://docs.astral.sh/uv/)
  
  ```console
  > curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## Installation

```console
> git clone git@github.com:eriksf/neo4j-arxiv.git
> cd neo4j-arxiv
> uv venv --seed --python 3.13
> uv pip install -r requirements.txt
```

## Download dataset

```console
> uv run kaggle datasets download Cornell-University/arxiv
> unzip arxiv.zip
```

Should produce a file name `arxiv-metadata-oai-snapshot.json`.
