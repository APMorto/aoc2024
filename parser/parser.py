from typing import List

def read_grid(fp: str) -> List[str]:
    with open(fp, 'r') as f:
        lines = f.readlines()
    return [l for line in lines if len(l:=line.strip()) > 0]