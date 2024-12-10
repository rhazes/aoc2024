import re
import heapq

spaces_pattern = re.compile(r'\s+')
list_1 = []
list_2 = []
foo = []



# with open("input01.txt","r") as FILE:
with open("input01_test.txt","r") as FILE:
    for line in FILE:
        # l = line.strip()
        print(line)
        a,b = re.split(spaces_pattern,line.strip())
        heapq.heappush(list_1,int(a))
        heapq.heappush(list_2,int(b))

        # foo.append([int(a),int(b)])
        # print(line.strip())

sorted_1 = [ heapq.heappop(list_1) for i in range(len(list_1))]
sorted_2 = [ heapq.heappop(list_2) for i in range(len(list_2))]

print(sorted_1)

# solution to part 
diffs = [ abs(a - b) for a,b in zip(sorted_1,sorted_2)]
print(sum(diffs))

# --------
# PART 2
# --------

# dictionary of counts for sorted_2
counts = {}
for x in sorted_2:
    if x in counts:
        counts[x] += 1
    else:
        counts[x] = 1

# sorted_1 as a set of unique keys to index into sorted_2
sim_score = 0
for x in sorted_1:
    print(x,end=': ')
    if x in counts:
        print(counts[x],end=' ')
        sim_score += x * counts[x]

    print()
print(sim_score)