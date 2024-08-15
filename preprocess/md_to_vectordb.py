import os
import glob
import re
from uuid import uuid4
from directories import fixtures, root, upload
from tqdm import tqdm

import dotenv
dotenv.load_dotenv(root / ".env")

from mydata_chatbot.database.chroma import (
    mydata_guideline_docs_chroma,
    mydata_api_docs_chroma,
    mydata_other_docs_chroma,
)
from langchain.text_splitter import MarkdownHeaderTextSplitter, MarkdownTextSplitter

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def md2chroma(md_path):
    md_filename = os.path.basename(md_path)

    md_text = open(md_path).read()

    replace_list = []
    if (
            md_filename
            == "(수정게시) 금융분야 마이데이터 표준 API 규격 v1.md"
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

    # Insert only existing images into metadata. (You have to remove the images yourself and leave only the images you need.)
    for idx, doc in enumerate(md_header_splits):
        image_list = [line for line in doc.page_content.split('\n') if line.startswith('![]')]
        for image_path in image_list:
            if not os.path.exists(image_path.strip()[4:-1]):
                doc.page_content = doc.page_content.replace(image_path, "")
            elif os.path.getsize(image_path.strip()[4:-1]) < 150 * 1024:
                doc.page_content = doc.page_content.replace(image_path, "")
                os.remove(image_path.strip()[4:-1])

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
        doc.metadata["document_name"] = os.path.basename(md_path.replace("md", "pdf"))

        header_list = [header_tuple[1] for header_tuple in headers_to_split_on]
        for header in header_list:
            if header in doc.metadata.keys():
                doc.page_content = doc.metadata[header] + "\n" + doc.page_content

        image_list = [line.strip()[4:-1] for line in doc.page_content.split('\n') if line.startswith('![]')]
        if len(image_list) > 0:
            doc.metadata["images"] = str(image_list)

    print(
        "Top 5 length of docs content: ",
        sorted([len(doc.page_content) for doc in docs], reverse=True)[:10],
    )

    if (
            md_filename
            == "(수정게시) 금융분야 마이데이터 표준 API 규격 v1.md"
    ):
        vectordb = mydata_api_docs_chroma
    elif (
            md_filename
            == "(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.md"
    ):
        vectordb = mydata_guideline_docs_chroma
    else:
        vectordb = mydata_other_docs_chroma

    # add to vector db
    vectordb.add_documents(documents=docs, ids=[str(uuid4()) for _ in range(len(docs))])

    print("Complete to save file into vector db: ", md_filename)


if __name__ == "__main__":
    md_list = glob.glob((upload / "**/*.md").__str__())

    # ProcessPoolExecutor or ThreadPoolExecutor
    with ProcessPoolExecutor(
        max_workers=2
    ) as executor:
        results = list(
            tqdm(
                executor.map(md2chroma, [md_path for md_path in md_list]),
                total=len(md_list),
            )
        )
