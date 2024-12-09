from typing import List

def read_line(fp: str) -> str:
    with open(fp, 'r') as f:
        return f.read().strip()

def read_grid(fp: str) -> List[str]:
    with open(fp, 'r') as f:
        lines = f.readlines()
    return [l for line in lines if len(l:=line.strip()) > 0]

def read_lines(fp: str) -> List[str]:
    return read_grid(fp)

def read_list_grid(fp: str) -> List[List[str]]:
    with open(fp, 'r') as f:
        lines = f.readlines()
    return [list(l) for line in lines if len(l := line.strip()) > 0]

def read_line_blocks(fp: str) -> List[List[str]]:
    """
    Parses groups of non-blank lines into a list of lists of those groups.

    75|13
    53|13               ---->    [["75|13", "53|13"], ["75,47,61,53,29"]]

    75,47,61,53,29
    """
    out = []
    cur_block = []
    with open(fp, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                if len(cur_block) > 0:
                    out.append(cur_block)
                    cur_block = []

            else:
                cur_block.append(line)

    if len(cur_block) > 0:
        out.append(cur_block)

    return out

