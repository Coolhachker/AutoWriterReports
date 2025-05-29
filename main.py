import asyncio
from src.tools_for_proces_of_word_document.Engine_of_processor import WordProcessor
import pathlib

import sys


if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Пути нет, пиши -h'
    if sys.argv[1] == '-h':
        print('Напиши после исполняемого файла путь к файлу WORD.')
    else:
        processor = WordProcessor(pathlib.Path(sys.argv[1]))
        processor.run_case()