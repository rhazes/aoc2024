import operator
from input07 import data

def to_ternary(n):
    if n < 3:
        return str(n)
    else:
        return to_ternary(n//3) + str(n % 3)

def check_with_mul_add(target,operands):
    # print(f"seeking Target: {target}")
    operands_count = len(operands)-1
    opcodes = [ format(o, f"0{operands_count}b") for o in range(pow(2,operands_count))]

    comp_str = [operands[0]]
    for opcode in opcodes:
        expression = [operands[0]]
        for op,num in zip(opcode,operands[1:]):
            expression.append(int(op))
            expression.append(num)
        # print(opcode,f" expression:{expression}")
        total = 0
        for i,x in enumerate(expression):
            if i == len(expression) - 1:
                break
            if i == 0:
                total = x
                continue
            if i % 2 == 1:
                op = [operator.iadd,operator.imul][x]
                total = op(total,expression[i+1])
        if total == target:
            # print(f"**found** {total} ") #expr:{''.join([str(e) for e in expression])}")
            return total
    return False

def check_with_3_ops(target,operands):
    # print(f"seeking Target: {target}")
    operands_count = len(operands)-1
    expression_permutations = pow(3,operands_count)
    opcodes = [to_ternary(n).zfill(operands_count) for n in range(expression_permutations)] 

    comp_str = [operands[0]]
    for opcode in opcodes:
        expression = [operands[0]]
        for op,num in zip(opcode,operands[1:]):
            expression.append(int(op))
            expression.append(num)
        # print(opcode,f" expression:{expression}")
        total = 0
        for i,x in enumerate(expression):
            if i == len(expression) - 1:
                break
            if i == 0: 
                total = x
                continue
            if i % 2 == 1: # x is an operator else operand
                op = [operator.iadd,operator.imul,concatenate_nums][x]
                # print(f"\t calc with {i}({op})...",end= ' ')
                total = op(total,expression[i+1])
                # print(f" = {total}")

        if total == target:
            # print(f"**found** {total} ") #expr:{''.join([str(e) for e in expression])}")
            return total
    return False

def concatenate_nums(a,b):
    return int(str(a) + str(b))

if __name__ == '__main__':
    passed_total = 0

    for target,operands in data:
        # value = check_with_mul_add(target,operands)
        value = check_with_3_ops(target,operands)
        if value:
            passed_total += value
    
    print(passed_total)
    exit()

    # data = [(3267,[81,40,27])]
    # Prob 2
    passed_total = 0

    # for target,operands in data: 
    #     # print(f"seeking Target: {target}")
    #     operands_count = len(operands)-1
    #     expression_permutations = pow(3,operands_count)
    #     opcodes = [to_ternary(n).zfill(operands_count) for n in expression_permutations] 

    #     comp_str = [operands[0]]
    #     for opcode in opcodes:
    #         expression = [operands[0]]
    #         for op,num in zip(opcode,operands[1:]):
    #             expression.append(int(op))
    #             expression.append(num)
    #         # print(opcode,f" expression:{expression}")
    #         total = 0
    #         for i,x in enumerate(expression):
    #             if i == len(expression) - 1:
    #                 break
    #             if i == 0:
    #                 total = x
    #                 continue
    #             if i % 2 == 1:
    #                 op = [operator.iadd,operator.imul][x]
    #                 total = op(total,expression[i+1])
    #         if total == target:
    #             passed_total += total
    #             print(f"**found** {total} ") #expr:{''.join([str(e) for e in expression])}")
    #             break

            
    # print(f"answer: {passed_total}")
    # exit()


    # PROB 1
    passed_total = 0
    for target,operands in data: 
        # print(f"seeking Target: {target}")
        operands_count = len(operands)-1
        opcodes = [ format(o, f"0{operands_count}b") for o in range(pow(2,operands_count))]

        comp_str = [operands[0]]
        for opcode in opcodes:
            expression = [operands[0]]
            for op,num in zip(opcode,operands[1:]):
                expression.append(int(op))
                expression.append(num)
            # print(opcode,f" expression:{expression}")
            total = 0
            for i,x in enumerate(expression):
                if i == len(expression) - 1:
                    break
                if i == 0:
                    total = x
                    continue
                if i % 2 == 1:
                    op = [operator.iadd,operator.imul][x]
                    total = op(total,expression[i+1])
            if total == target:
                passed_total += total
                print(f"**found** {total} ") #expr:{''.join([str(e) for e in expression])}")
                break

            
    print(f"answer: {passed_total}")