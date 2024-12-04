import re

test_mode = False

input_file = "input03_test2.txt" if test_mode else "input03.txt"

data = []
with open(input_file,'r') as file:
    for line in file:
        data.append(line.strip())

def parse(line):
    tokens = re.findall('mul\(\d{1,3},\d{1,3}\)',line)
    return tokens

def get_product(token):
    matches = re.findall(r'\d+', token)
    matches = [int(i) for i in matches]
    return matches[0] * matches[1]

def prob1():
    products = []
    for line in data:
        tokens = parse(line)
        print(len(tokens))
        for token in tokens:
            products.append(get_product(token))
            # print(products, products[0]*products[1])

    return sum(products)

def parse_do_blocks(memory):
    do_splits = re.split("do\(\)",memory)
    # the first element is part of the preceding dont block
    do_splits = do_splits[1:] 
    muls = []
    for _split in do_splits:
        muls = muls + parse(_split)

    return muls


# Didnt work
def _prob2():
    # find the first don't
    # print(line)
    # initial_dont = re.search(r"don't",line)
    # start,_ = initial_dont.span()
    # tokens = parse(data[0][:start])
    # print(tokens)
    
    muls = []
    products = []
    enabled = True

    for line in data:
        dont_splits = re.split(r"don't\(\)", line)

        # the first element is with the initial do block
        # that precedes the first dont block
        if enabled:
            muls += parse(dont_splits[0])
            dont_splits = dont_splits[1:]
        # print(muls)
        # take the rest of the dont splits
        for idx,dont_block in enumerate(dont_splits):
            # print(f"dont block: {dont_block}")
            do_block_muls = parse_do_blocks(dont_block) 
            muls += do_block_muls

            #update enabled flag
            if idx == len(dont_splits) - 1:
                if len(do_block_muls) == 0:
                    enabled = False
                    print(f"setting enabled false for last dont block in line {line[:30]}")
                else:
                    enabled = True

        # print(muls)
        for token in muls:
            products.append(get_product(token))

        # print(products)
    return sum(products)


def prob2():
    _input = "".join(data)
    enabled_flag = re.findall(r"don't\(\)|do\(\)",_input)
    flags = ["do()"] + enabled_flag
    instructions = re.split(r"don't\(\)|do\(\)",_input)
    instr_flags = list(zip(instructions,flags))
    do_instr = [instr for instr,flag in instr_flags if flag == "do()"]
    do_mul = [ parse(instr) for instr in do_instr]
    prods = []
    for muls in do_mul:
        prods.append([ get_product(mul) for mul in muls])

    totals = [sum(ps) for ps in prods]
    return sum(totals)


# result = prob1()
result = prob2()
print(result)


#352708266