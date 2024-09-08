import logging
from typing import Annotated, Union, Dict, List, Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles
import pymupdf4llm
from directories import upload
import os
import uuid

from langchain.text_splitter import MarkdownHeaderTextSplitter, MarkdownTextSplitter
from mydata_chatbot.database.chroma import mydata_other_docs_chroma
from mydata_chatbot.database import get_session
from mydata_chatbot.crud.document import document
from mydata_chatbot.schemas.document import DocumentCreate


router = APIRouter(prefix="/v1/data", tags=["data"])

logger = logging.getLogger(__name__)


@router.post("/upload/pdf")
async def upload_pdf(
    pdf_file: Annotated[UploadFile, File(description="A PDF file")],
    db: AsyncSession = Depends(get_session),
    write_images: bool = False,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
):
    """pdf file to vector store"""

    ### async read
    pdf_data = await pdf_file.read()

    pdf_folder = upload / pdf_file.filename[:-4]
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    pdf_path = pdf_folder / pdf_file.filename
    # if os.path.exists(pdf_folder / pdf_file.filename):
    #     return "File already exists"

    async with aiofiles.open(pdf_path, "wb") as out_pdf_file:
        await out_pdf_file.write(pdf_data)
    logger.info("Save pdf")

    ### pdf to markdown
    md_text = pymupdf4llm.to_markdown(
        pdf_path,
        write_images=write_images,
        image_path=(pdf_folder / "images").__str__(),
    )
    logger.info("Reformat pdf to markdown")

    md_path = pdf_path.__str__()[:-3] + "md"
    async with aiofiles.open(md_path, "w") as out_md_file:
        await out_md_file.write(md_text)
    logger.info("Save markdown")

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
    text_splitter = MarkdownTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    logger.info("Split text into chunks")

    ### Split docs
    docs = text_splitter.split_documents(md_header_splits)
    logger.info(f"Number of documents: {len(docs)}")

    for idx, doc in enumerate(docs):
        doc.id = idx + 1
        doc.metadata["filename"] = pdf_file.filename

        header_list = [header_tuple[1] for header_tuple in headers_to_split_on]
        for header in header_list:
            if header in doc.metadata.keys():
                doc.page_content = doc.metadata[header] + "\n" + doc.page_content

    logger.info(
        f"Top 5 length of docs content: {sorted([len(doc.page_content) for doc in docs], reverse=True)[:5]}",
    )

    if len(await document.get_by_filename(db=db, filename=pdf_file.filename)) > 0:
        raise HTTPException(
            status_code=404, detail=f"{pdf_file.filename} is already in db."
        )

    logger.info("Adding to ChromaDB...")
    await mydata_other_docs_chroma.aadd_documents(
        documents=docs, ids=[str(uuid.uuid4()) for _ in range(len(docs))]
    )

    logger.info("Adding to RDB...")
    await document.create(db=db, obj_in=DocumentCreate(filename=pdf_file.filename))

    return {"status": "completed"}
