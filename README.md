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

Should produce a file name `arxiv-metadata-oai-snapshot.json`. It contains a JSON entry per line.

## Usage

1. Copy `.env.sample` to `.env` and fill in the variables.

2. Run the `insert.py` to insert data. Specify the input file (JSON file from above), start line to
   start reading records, and end line to stop reading records.

```console
> uv run insert.py --help
Usage: insert.py [OPTIONS] INPUT_FILE START_LINE END_LINE

Options:
  --version                       Show the version and exit.
  --insert-data / --no-insert-data
                                  Insert the data.  [default: insert-data]
  --help                          Show this message and exit.
```

3. Run the `query.py` script to get some summary data back from the inserted data.

```console
> uv run query.py
```
