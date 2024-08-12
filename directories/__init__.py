import os

from pathlib import Path

root = Path(os.path.dirname(__file__)).parent

home = root.joinpath("rag_backend")

static = home.joinpath("static")

upload = static.joinpath("upload")

logging = root.joinpath("logging.yaml")

sqlite3 = root.joinpath("sqlite3.db")

fixtures = root.joinpath("fixtures")

chroma = root.joinpath("chroma")

mydata_api_docs_chromadb = chroma.joinpath("mydata_api_docs")

mydata_guideline_docs_chromadb = chroma.joinpath("mydata_guideline_docs")

mydata_other_docs_chromadb = chroma.joinpath("mydata_other_docs")

# pdf_file = fixtures.joinpath("upload_test.pdf")
#
# csv_file = fixtures.joinpath("upload_test.csv")
