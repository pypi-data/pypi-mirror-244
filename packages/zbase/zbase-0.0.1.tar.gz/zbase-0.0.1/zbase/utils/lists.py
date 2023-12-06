from typing import Iterable,List,List

def paging(objs:Iterable,page_size:int)->List:
    if not objs:
        return objs
    buf = []
    count = 0
    for i in objs:
        buf.append(i)
        count += 1
        if count == page_size:
            yield buf
            buf = []
            count = 0
    if buf:
        yield buf


def calc_pages(total:int, page_size:int)->int:
    if page_size==0:
        return 0
    if total%page_size==0:
        return total//page_size
    else:
        return total//page_size+1