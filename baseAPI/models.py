from dataclasses import dataclass
from gspread.worksheet import Worksheet
from baseAPI.base import LIST_FREQ, LIST_CREQ, LIST_KEYW

@dataclass
class SheetList:
    _sheet: Worksheet
    start_row: int


@dataclass
class KeyWord:
    id: int
    word: str

    def __post_init__(self):
        self.id = int(self.id)


class FreqList(SheetList):
    start_row = 2
    _sheet = LIST_FREQ

    @classmethod
    def _get_row(cls):
        row = cls._sheet.row_values(cls.start_row)     
        if any(row):
            return row     
        return None
    
    @classmethod
    def pop(cls) -> list[str] | None:
        row = cls._get_row()
        if row:
            cls._sheet.delete_row(cls.start_row)
            return row
        return None


class CreqList(SheetList):
    start_row = 2
    _sheet = LIST_CREQ

    @classmethod
    def add(cls, values: list[str]) -> None:
        cls._sheet.append_row(values)


class KeyWList(SheetList):
    start_row = 1
    _sheet = LIST_KEYW

    @classmethod
    def getKeyW(cls, ids: list[str]) -> list[KeyWord]:
        table = cls._sheet.get_all_values()
        result = []
        for key, id in table:
            if id in ids:
                result.append(KeyWord(int(id), key))
        return result


@dataclass
class RequestGroup:
    body: str
    ids_str: str

    def __post_init__(self):
        self.ids = []
        splits = [id.strip() for id in self.ids_str.split(',')]
        for split in splits:
            if '-' in split:
                start, end = map(int, split.split('-'))
                ids_range = [str(id) for id in range(start, end + 1)]
                self.ids += ids_range
            else:
                self.ids.append(split)
        self.ids = list(set(self.ids))
        keywords = KeyWList.getKeyW(self.ids)
        self.requests = [self.body.format(keyword.word) for keyword in keywords]

    def to_row(self) -> list[str]:
        return [self.body, self.ids_str]
    