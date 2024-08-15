import os
import glob
from directories import fixtures, upload
from tqdm import tqdm
import pymupdf4llm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def pdf2md(pdf_path, write_images=True):
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

    return True


if __name__ == "__main__":
    pdf_list = glob.glob((fixtures / "*.pdf").__str__())

    # for pdf_path in tqdm(pdf_list):
    #     filename = os.path.basename(pdf_path)
    #     preprocess(pdf_path)
    #     print("Complete to save pdf to markdown: ", filename)

    with ProcessPoolExecutor(
        max_workers=2
    ) as executor:  # ProcessPoolExecutor or ThreadPoolExecutor
        results = list(
            tqdm(
                executor.map(pdf2md, [pdf_path for pdf_path in pdf_list]),
                total=len(pdf_list),
            )
        )
