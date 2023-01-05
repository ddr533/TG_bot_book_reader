BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    symbols = ',.!:;?'
    end = start + size
    if text[start:end][-1] not in symbols:
        return _get_part_text(text, start, size - 1)
    if text[start:end + 1][-1] in symbols:
        if text[start:end + 1] != text[start:end]:
            return _get_part_text(text, start, size - 1)
        return text[start:end], len(text[start:end])
    return text[start:end], size


def prepare_book(path: str) -> None:
    '''Функция, формирующая словарь книги.'''
    with open(path, 'r') as file:
        text = file.read()
        start, page_number = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size
        book[page_number] = page_text.strip()
        page_number += 1


prepare_book(BOOK_PATH)
