import time

from docx import Document
from docx.text.paragraph import Paragraph
import pathlib
import tqdm


class WordProcessor:
    def __init__(self, path_to_document: pathlib.Path):
        self.path_to_document = path_to_document
        assert path_to_document.exists()

        self.document = Document(self.path_to_document.__str__())
        self.count_of_paragraphs_to_modify = self.get_count_of_caption_text()
        assert self.count_of_paragraphs_to_modify != 0

    def get_count_of_caption_text(self) -> int:
        count: int = 0

        for i, paragraph in enumerate(self.document.paragraphs):
            count += 1 if self.check_paragraph_on_suitability(paragraph, i) else 0
        return count

    @staticmethod
    def check_paragraph_on_image(paragraph: Paragraph) -> bool:
        return paragraph.runs and any(run._element.xpath('.//pic:pic') for run in paragraph.runs)

    def check_paragraph_on_suitability(self, paragraph: Paragraph, i: int) -> bool:
        if self.check_paragraph_on_image(paragraph):
            if i + 2 < len(self.document.paragraphs):
                if not self.check_paragraph_on_image(self.document.paragraphs[i + 2]):
                    return True
        return False

    def process_paragraphs(self):
        with tqdm.tqdm(total=self.count_of_paragraphs_to_modify) as t:
            t.set_description('Количество параграфов')
            for i, paragraph in enumerate(self.document.paragraphs):
                if self.check_paragraph_on_suitability(paragraph, i):
                    t.update()


processor = WordProcessor(pathlib.Path('/Users/egor/PycharmProjects/AutoWriterReports/USMT.docx'))
processor.process_paragraphs()
