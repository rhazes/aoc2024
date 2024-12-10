# from input05_test import *

TESTING = False

def make_rule_base(rules):
    rule_base = {}
    for rule in rules.split("\n"):
        # print(rule.strip().split("|"))

        [preceding_page, following_page] = [int(x) for x in rule.strip().split("|")]

        if preceding_page in rule_base:
            rule_base[preceding_page].add(following_page)
        else:
            rule_base[preceding_page] = {following_page}

    return rule_base

def make_update_orders(orderings):
    updates = []
    for nums in orderings.split("\n"):
        # nums = nums.strip()
        nums = [ int(n) for n in nums.strip().split(",")]
        updates.append(nums)

    return updates

def validate_order(update_list,rb):
    # make sure no pages before you are in your rule base set
    for idx,update in enumerate(update_list):
        updated_before = set(update_list[:idx])
        if not update in rb:
            continue
        must_come_after = rb[update]

        # if there is nothing before then 
        # this is a valid update
        if not bool(updated_before):
            continue

        intersection = updated_before & must_come_after

        if bool(intersection): 
            out_of_order_update = intersection.pop()
            if TESTING:
                print(f"not a valid order for {update}:\n\
                       intersection {out_of_order_update}\n\
                        @index{update_list.index(out_of_order_update)}.\n\
                        updated_before:{updated_before}{update}\n\
                        update_list:{update_list}")
                    #   \n\tmust precede{must_come_after}\
                    # \n\treceded by:{updated_before}")
            return (False,(update_list,idx,update,update_list.index(out_of_order_update),out_of_order_update))
    
    return (True, update_list[ len(update_list)//2 ])

def parse_input():
    rules = []
    orders = []
    with open(['input05.txt','input05_test.txt'][TESTING],'r') as FILE:
        for line in FILE:
            if '|' in line:
                rules.append(line.strip())
            if ',' in line:
                orders.append(line.strip())
        return ("\n".join(rules), "\n".join(orders))

rules,ordering = parse_input()
rules = make_rule_base(rules)
orders = make_update_orders(ordering)


def correct_updates(orders):
    test_result,context = validate_order(orders,rules)
    if test_result:
        return orders
    else:
        lst,idx_error,_,idx_fix,_ = context
        #swap
        lst[idx_error], lst[idx_fix] = lst[idx_fix], lst[idx_error]
        return correct_updates(lst)


def prob1():
    result = [validate_order(order,rules) for order in orders]
    result = [mid_update for valid,mid_update in result if valid]
    return sum(result)

# print(f"prob 1: {prob1()}")

def prob2():
    result = [validate_order(order,rules) for order in orders]
    fails = [ error for valid,error in result if not valid]
    
    corrected = [correct_updates(orders) for orders,_,_,_,_ in fails]
    print(corrected)
    return sum([updates[len(updates) // 2] for updates in corrected])
    # failed = 
    pass