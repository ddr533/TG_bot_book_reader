BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    ch=',.!:;?'
    ssize=size
    if len(text)<=size+start:
        ssize=len(text)-start
    else:
        for i in range (size+start-1,start,-1):
            if text[i] in ch and text[i+1] not in ch:
                break
            ssize-=1
    return text[start: start + ssize], ssize

def prepare_book(path: str) -> None:
    '''Функция, формирующая словарь книги.'''
    with open(path, 'r', encoding='UTF-8') as file:
        text = file.read()
        start, page_number = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size
        book[page_number] = page_text.strip()
        page_number += 1

prepare_book(BOOK_PATH)
