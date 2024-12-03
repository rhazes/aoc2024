import functools
import re

rec = []

# with open("data01_2_test.txt","r") as file:
with open("input02.txt","r") as file:
    for line in file:
        __rec = [ int(x) for x in re.split(r'\s+',line.strip()) ] 
        rec.append(__rec)

def remove(lst,i):
    return lst[:i] + lst[i+1:]

def test_increasing(lst):
    diff_data = [ lst[i+1] - lst[i] for i in range(0,len(lst)-1) ] 
    # print(f"lst: {lst}\ndif:{diff_data}")

    # check all adjacents for positive difference in acceptable range
    positive = [ x >= 1 and x <= 3 for x in diff_data]
    # print(positive)
    all_positive = functools.reduce( lambda a,b: a and b, positive, True)

    if all_positive:
        return True
    else: # return data about the fail
        return list(zip(positive,diff_data))
    # return all_positive
 
def test_decreasing(lst):
    diff_data = [ lst[i] - lst[i+1] for i in range(0,len(lst)-1)] 
    
    # check all adjacents for positive difference in acceptable range
    positive = [ x >= 1 and x <= 3 for x in diff_data]
    all_positive = functools.reduce( lambda a,b: a and b, positive, True)
    # return all_positive
 
    if all_positive:
        return True
    else:
        return list(zip(positive,diff_data))

def can_be_dampened(levels,deltas):
    # check to see if removing an item make it true
    failed_count = 0
    failed_idx = 0
    for (idx,(is_safe,delta)) in enumerate(deltas):
        if not is_safe:
            failed_count += 1
            failed_idx = idx

    if failed_count == 1:
        # find the index of the false
        # whatever the index test removing it and the one after it
        idx_to_remove = 0
        for i in [failed_idx, failed_idx + 1]:
            dampened_levels = remove(levels,i)
            incr = test_increasing(dampened_levels)
            decr = test_decreasing(dampened_levels)
            if incr == True or decr == True:
                return True #"dampened"

        # return f" might be able to be dampened; failed_idx = {failed_idx} {levels[failed_idx]-levels[failed_idx + 1]}"
    # else:
    return False #" No dampening"

def prob1():
    safe_count = 0
    for r in rec:
        # print(r)
        decreasing_levels = test_decreasing(r)
        increasing_levels = test_increasing(r)
        # print(r,decreasing_levels,increasing_levels)

        if decreasing_levels == True:
            safe_count += 1
            continue
            # print("\tsafe")

        if increasing_levels == True:
            safe_count += 1
            continue
            # print("\tsafe")

        # Try removing 1 value at a time and testing for safe
        # if you find one increment the safe_count and break out
        for i in range(len(r)):
            dampened = remove(r,i)
            decreasing_levels = test_decreasing(dampened)
            increasing_levels = test_increasing(dampened)
            
            if decreasing_levels == True or increasing_levels == True:
                safe_count += 1
                break


        # The below is just testing the bad value for dampening
        # Now try to remove all of them and test 
        # if not (decreasing_levels==True or increasing_levels==True):
        #     if can_be_dampened(r,decreasing_levels):
        #         safe_count += 1
        #         continue

        #     if can_be_dampened(r,increasing_levels):
        #         safe_count += 1
        #         continue
            
            # print("\t",decreasing_levels, can_be_dampened(r,decreasing_levels))
            # print("\t",increasing_levels, can_be_dampened(r,increasing_levels))
        
        # print()

    # result = [test_increasing(r) or test_decreasing(r) for r in rec]
    # print(result)
    print(safe_count)
    
def safe(lst):
    # get the diff between adjacent elements
    diff_data = [ lst[i-1] - lst[i] for i in range(1,len(lst))] 
    
    # check all adjacents for positive difference in acceptable range
    positive = [ x >= 1 and x <= 3 for x in diff_data]
    # check all adjacents for negative difference in acceptable range
    negative = [ x <= -1 and x >= -3 for x in diff_data]


    # check for positive and negative all safe
    all_positive = functools.reduce( lambda a,b: a and b, positive, True)
    all_negative = functools.reduce( lambda a,b: a and b, negative, True)

    if all_negative or all_positive:
        # print(f"returning {all_positive} // {all_negative}")
        return True
    # solution for problem one
    # else:
        # return False
    
    # problem 2 try to find 1 edit solutions
    count = 0
    reset_safe = False

    for errors in [positive,negative]:
        # print("restesting ",count)
        count += 1
        idx_positive_errors = []
        for i,val in enumerate(errors):
            if not val:
                idx_positive_errors.append(i)
    
        # print(f"{idx_positive_errors}")

        # see if removing this error would result in a safe test
        if len(idx_positive_errors) == 1:
            # print(f"1 error...trying to retest {errors}")
            # store the index of the error and the one just ahead of it
            # test to see if removing either one of them results in a safe
            idxs = [idx_positive_errors[0],idx_positive_errors[0]+1 ]
            # make sure that we are not checking negative indices
            assert(idx_positive_errors[0]+1 >= 0)

            for idx in idxs:
                retest = lst[:idx] + lst[idx+1:]

                diff_data = [ retest[i-1] - retest[i] for i in range(1,len(retest))] 
                # print(f"\tdiff_data{diff_data}")

                positive = [ x >= 1 and x <= 3 for x in diff_data]
                # check all adjacents for negative difference in acceptable range
                negative = [ x <= -1 and x >= -3 for x in diff_data]

                # check for positive and negative all safe
                all_positive = functools.reduce( lambda a,b: a and b, positive, True)
                all_negative = functools.reduce( lambda a,b: a and b, negative, True)

                retest_safe = reset_safe or all_positive or all_negative
                # print(f"\trtest_safe {retest_safe}")
            if retest_safe:
                # print("Restest is safe")
                return True

    return False
    # print(lst)
    # print(f"positive: {positive}")
    # print(f"negative: {negative}")

# result = [ safe(r) for r in rec]
# print(result)
# count = 0
# for r in result:
    # if r:
        # count += 1

# print(f"safe count = {count}")
# safe([1,3,2,4,5])

prob1()

part1 = False
if part1:
    result = [ safe(r) for r in rec]
    safe_count = 0
    for r in result:
        if r:
            safe_count += 1

    print(safe_count)

# data = diff_all(foo)
# print(data)
# print(safe(data))