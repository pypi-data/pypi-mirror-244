import json

def read_lines(file:str, parse_json = False, skip_empty=True):
    with open(file , 'r') as f:
        for line in f:
            if skip_empty:
                if line.strip()=="":
                    continue
            if parse_json:
                yield json.loads(line)
            else:
                yield line.strip()
