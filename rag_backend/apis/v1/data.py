import logging
from typing import Annotated, Union, Dict, List, Optional
from fastapi import APIRouter, UploadFile, File
import aiofiles
import pymupdf4llm
from directories import upload
import os
import uuid
import re
from rag_backend.database.chroma import mydata_other_docs_chroma
from langchain.text_splitter import MarkdownHeaderTextSplitter, MarkdownTextSplitter

router = APIRouter(prefix="/v1/data", tags=["data"])

logger = logging.getLogger(__name__)


@router.post("/upload/pdf")
async def upload_pdf(
    pdf_file: Annotated[UploadFile, File(description="A PDF file")],
    replace_list: Optional[List] = None,
):
    """pdf file to vector store"""
    if replace_list is None:
        replace_list = []

    ### async read
    pdf_data = await pdf_file.read()

    pdf_folder = upload / pdf_file.filename[:-4]
    if os.path.exists(pdf_folder):
        return "File already exists"

    async with aiofiles.open(pdf_folder / pdf_file.filename, "wb") as out_file:
        await out_file.write(pdf_data)

    ### pdf to markdown
    md_text = pymupdf4llm.to_markdown(
        upload / pdf_file.filename,
        write_images=True,
        image_path=(pdf_folder / "images").__str__(),
    )

    ### remove words
    for replace_word in replace_list:
        md_text = re.sub(replace_word, "", md_text)

    ### Markdown splits
    headers_to_split_on = [
        # ("#", "header_1"),
        # ("##", "header_2"),
        # ("###", "header_3"),
        ("####", "header_4"),
        ("#####", "header_5"),
        ("######", "header_6"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=False
    )
    md_header_splits = markdown_splitter.split_text(md_text)

    ### Text splits
    chunk_size = 300
    chunk_overlap = 50
    text_splitter = MarkdownTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    ### Split docs
    docs = text_splitter.split_documents(md_header_splits)
    print("Number of documents: ", len(docs))

    for idx, doc in enumerate(docs):
        doc.id = idx + 1
        doc.metadata["filename"] = pdf_file.filename

        header_list = [header_tuple[1] for header_tuple in headers_to_split_on]
        for header in header_list:
            if header in doc.metadata.keys():
                doc.page_content = doc.metadata[header] + "\n" + doc.page_content

    print(
        "Top 5 length of docs content: ",
        sorted([len(doc.page_content) for doc in docs], reverse=True)[:5],
    )

    # mydata_other_docs_chroma.aadd_documents(documents=docs, ids=[str(uuid.uuid4()) for _ in range(len(docs))])

    return "Completed"
