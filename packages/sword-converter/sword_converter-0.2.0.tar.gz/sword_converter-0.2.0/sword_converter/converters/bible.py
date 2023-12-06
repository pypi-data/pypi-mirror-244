import concurrent.futures
import json
from pathlib import Path
from threading import Event

from pysword.modules import SwordModules

from sword_converter.utils.progress import Progress


class Bible(object):
    def __init__(self, source, module):
        modules = SwordModules(source)
        parsed_modules = modules.parse_modules()
        self._name = parsed_modules[module]["description"]
        self._abbreviation = module
        self.sword_bible = modules.get_bible_from_module(module)
        self._output_file = f"{Path(source).resolve().parent / '_'.join(self._name.split())}.{{extension}}"

    def to_json(self):
        data = {
            "name": self._name,
            "abbreviation": self._abbreviation,
            "books": {}
        }

        for testament, books in self.sword_bible.get_structure().get_books().items():
            data["books"][testament] = []
            for number, book in enumerate(books, start=sum([len(v) for v in data["books"].values()]) + 1):
                progress = Progress(book.name, book.num_chapters)
                _book = {
                    "number": number,
                    "name": book.name,
                    "abbreviation": book.preferred_abbreviation,
                    "chapters": []
                }
                for chapter in range(1, book.num_chapters + 1):
                    _book["chapters"].append({
                        "number": chapter,
                        "verses": [{
                            "number": verse,
                            "text": self.sword_bible.get(
                                books=book.name,
                                chapters=chapter,
                                verses=verse,
                                join=""
                            )
                        } for verse in range(1, book.chapter_lengths[chapter - 1] + 1)]})
                    progress.update(chapter)
                data["books"][testament].append(_book)

        with open(self._output_file.format(extension="json"), "w") as fp:
            self._save(json.dump, obj=data, fp=fp)
            return fp.name

    @staticmethod
    def _save(fn, **kwargs):
        progress = Progress(title=f"Saving to {kwargs['fp'].name}")
        event = Event()
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(progress.infinite, event)
        fn(**kwargs)
        event.set()
