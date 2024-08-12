import os
import glob
import re
from uuid import uuid4
from directories import fixtures, root, upload
from tqdm import tqdm
import dotenv

dotenv.load_dotenv(root / ".env")

from rag_backend.database.chroma import (
    mydata_guideline_docs_chroma,
    mydata_api_docs_chroma,
    mydata_other_docs_chroma,
)
from langchain.text_splitter import MarkdownHeaderTextSplitter, MarkdownTextSplitter
import pymupdf4llm

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def preprocess(pdf_path, write_images=False):
    pdf_filename = os.path.basename(pdf_path)
    save_folder = upload / pdf_filename[:-4]
    save_path = save_folder / pdf_filename
    if not save_folder.exists():
        save_folder.mkdir(exist_ok=True)

    md_text = pymupdf4llm.to_markdown(
        pdf_path,
        write_images=write_images,
        image_path=(save_folder / "images").__str__(),
    )

    with open(save_path.__str__()[:-4] + ".md", "w") as f:
        f.write(md_text)

    replace_list = []
    if (
        pdf_filename
        == "(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf"
    ):
        replace_list.append(r"금융분야 마이데이터 표준API 규격")
        replace_list.append(r"\n금융보안원www fsec or kr \*\*\d+\*\*\n")

    for sub_str in replace_list:
        md_text = re.sub(sub_str, "", md_text)

    # MD splits
    headers_to_split_on = [
        # ("#", "Header 1"),
        # ("##", "Header 2"),
        # ("###", "header_3"),
        ("####", "header_4"),
        ("#####", "header_5"),
        ("######", "header_6"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=False
    )
    md_header_splits = markdown_splitter.split_text(md_text)

    # Text splits
    # chunk_size = 500
    # chunk_overlap = 100
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=chunk_size, chunk_overlap=chunk_overlap
    # )
    chunk_size = 300
    chunk_overlap = 50
    text_splitter = MarkdownTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split
    docs = text_splitter.split_documents(md_header_splits)
    print("Number of documents: ", len(docs))

    # update metadata
    for idx, doc in enumerate(docs):
        doc.id = idx + 1
        doc.metadata["document_name"] = os.path.basename(pdf_path)

        header_list = [header_tuple[1] for header_tuple in headers_to_split_on]
        for header in header_list:
            if header in doc.metadata.keys():
                doc.page_content = doc.metadata[header] + "\n" + doc.page_content

    print(
        "Top 5 length of docs content: ",
        sorted([len(doc.page_content) for doc in docs], reverse=True)[:10],
    )

    if (
        pdf_filename
        == "(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf"
    ):
        vectordb = mydata_api_docs_chroma
    elif (
        pdf_filename
        == "(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf"
    ):
        vectordb = mydata_guideline_docs_chroma
    else:
        vectordb = mydata_other_docs_chroma

    # add to vector db
    vectordb.add_documents(documents=docs, ids=[str(uuid4()) for _ in range(len(docs))])

    print("Complete to save file into vector db: ", pdf_filename)

    return True


if __name__ == "__main__":
    pdf_list = glob.glob((fixtures / "*.pdf").__str__())

    # for pdf_path in tqdm(pdf_list):
    #     filename = os.path.basename(pdf_path)
    #     preprocess(pdf_path)
    #     print("Complete to save to vector db: ", filename)

    with ProcessPoolExecutor(
        max_workers=2
    ) as executor:  # ProcessPoolExecutor or ThreadPoolExecutor
        results = list(
            tqdm(
                executor.map(preprocess, [pdf_path for pdf_path in pdf_list]),
                total=len(pdf_list),
            )
        )
