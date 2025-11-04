import json
import os
import sys

import click
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

from db import Neo4jConnection, add_authors, add_categories, add_papers
from version import __version__

load_dotenv()

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_CONNECTION_URI = os.getenv("NEO4J_CONNECTION_URI")

def get_author_list(line):
    # Cleans author dataframe column, creating a list of authors in the row.
    
    return [e[1] + ' ' + e[0] for e in line]


def get_category_list(line):
    # Cleans category dataframe column, creating a list of categories in the
    # row.
    
    return list(line.split(" "))


@click.command()
@click.version_option(__version__)
@click.argument("input_file", type=click.Path(readable=True), required=True)
@click.argument("start_line", type=click.INT, required=True)
@click.argument("end_line", type=click.INT, required=True)
@click.option("--insert-data/--no-insert-data", default=True, help="Insert the data.", show_default=True)
def main(input_file, start_line, end_line, insert_data):
    # grab data
    metadata = []
    
    print(f"Grabbing lines of {input_file} from line {start_line} to {end_line}...")
    if start_line < 1  or end_line < start_line:
        print("Invalid start of end line numbers.")
        sys.exit(1)

    total_lines = end_line - start_line + 1
    print(f"Total lines = {total_lines}")

    with open(input_file) as f:
        # skip lines before the start_line
        for _ in range(start_line - 1):
            next(f, None)

        # iterate through the desired lines with tqdm
        for i, line in enumerate(tqdm(f, total=total_lines, desc="Reading file")):
            current_line_number = start_line + i
            if current_line_number > end_line:
                break
            # process line
            metadata.append(json.loads(line))

    df = pd.DataFrame(metadata)
    print(df.head())

    if insert_data:
        # clean data
        df['cleaned_authors_list'] = df['authors_parsed'].map(get_author_list)
        df['category_list'] = df['categories'].map(get_category_list)
        df = df.drop(['submitter', 'authors', 'comments', 'journal-ref', 'doi', 'report-no', 'license', 'versions', 'update_date', 'abstract', 'authors_parsed', 'categories'], axis=1)
        print(df.head())

        # prepare category nodes
        categories = pd.DataFrame(df[['category_list']])
        categories.rename(columns={'category_list':'category'}, inplace=True)
        categories = categories.explode('category').drop_duplicates(subset=['category'])
        print('Categories:', categories.size)

        # prepare author nodes
        authors = pd.DataFrame(df[['cleaned_authors_list']])
        authors.rename(columns={'cleaned_authors_list':'author'}, inplace=True)
        authors = authors.explode('author').drop_duplicates(subset=['author'])
        print('Authors:', authors.size)

        conn = Neo4jConnection(uri=NEO4J_CONNECTION_URI, user=NEO4J_USERNAME, pwd=NEO4J_PASSWORD)

        # create the constraints
        conn.query('CREATE CONSTRAINT papers IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE')
        conn.query('CREATE CONSTRAINT authors IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE')
        conn.query('CREATE CONSTRAINT categories IF NOT EXISTS FOR (c:Category) REQUIRE c.category IS UNIQUE')

        # add categories
        print("Adding categories...")
        add_categories(conn, categories)

        # add authors
        print("Adding authors...")
        add_authors(conn, authors)


        # add papers and relationships
        print("Adding papers and relationships...")
        add_papers(conn, df)

        conn.close()


if __name__ == "__main__":
    main()
