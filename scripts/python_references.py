"""Original Python references for the added JSON-I/O DSA tasks."""
from collections import Counter, defaultdict, deque
from bisect import bisect_left, bisect_right
from itertools import combinations
import heapq
import inspect
import json
import math
from pathlib import Path

SOLUTIONS = {}
def solution(title):
    def decorate(fn):
        SOLUTIONS[title] = fn
        return fn
    return decorate

@solution('Perfect number check')
def perfect(n):
    if n <= 1:
        return False
    total = 1
    for d in range(2, math.isqrt(n)+1):
        if n % d == 0:
            total += d
            if d*d != n:
                total += n//d
    return total == n

@solution('Run-length string compression')
def compression(s):
    out, i = [], 0
    while i < len(s):
        j = i+1
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(s[i]+str(j-i))
        i = j
    return ''.join(out)

@solution('Two Sum indices')
def two_sum(data):
    seen = {}
    for i, value in enumerate(data['nums']):
        needed = data['target']-value
        if needed in seen:
            return [seen[needed], i]
        seen.setdefault(value, i)
    return []

@solution('Product except self without division')
def products(a):
    result, product = [1]*len(a), 1
    for i, value in enumerate(a):
        result[i] = product
        product *= value
    product = 1
    for i in range(len(a)-1, -1, -1):
        result[i] *= product
        product *= a[i]
    return result

@solution('Count subarrays summing to K')
def subarrays(data):
    counts, total, result = Counter({0:1}), 0, 0
    for value in data['nums']:
        total += value
        result += counts[total-data['k']]
        counts[total] += 1
    return result

@solution('Longest substring without repeats')
def unique_window(s):
    last, left, best = {}, 0, 0
    for right, c in enumerate(s):
        left = max(left, last.get(c, -1)+1)
        last[c] = right
        best = max(best, right-left+1)
    return best

@solution('First and last sorted occurrence')
def sorted_occurrences(data):
    a, target = data['nums'], data['target']
    left, right = bisect_left(a, target), bisect_right(a, target)
    return [left, right-1] if left < right else [-1, -1]

@solution('Merge two sorted arrays')
def merge_arrays(data):
    a, b = data
    i, j, result = 0, 0, []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result+a[i:]+b[j:]

@solution('Merge overlapping closed intervals')
def merge_intervals(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start,end])
    return result

@solution('Minimum meeting rooms')
def meeting_rooms(intervals):
    events = sorted([(s,1) for s,e in intervals]+[(e,-1) for s,e in intervals])
    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best

@solution('Balanced bracket validation')
def balanced(s):
    stack, pairs = [], {')':'(',']':'[','}':'{'}
    for c in s:
        if c in '([{':
            stack.append(c)
        elif not stack or stack.pop() != pairs[c]:
            return False
    return not stack

@solution('Next greater value on the right')
def next_greater(a):
    stack, result = [], [-1]*len(a)
    for i in range(len(a)-1,-1,-1):
        while stack and stack[-1] <= a[i]:
            stack.pop()
        if stack:
            result[i] = stack[-1]
        stack.append(a[i])
    return result

@solution('Sliding window maximum')
def window_max(data):
    a,k = data['nums'],data['k']
    queue, result = deque(), []
    for i,value in enumerate(a):
        while queue and queue[0] <= i-k:
            queue.popleft()
        while queue and a[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if i >= k-1:
            result.append(a[queue[0]])
    return result

@solution('Largest rectangle in histogram')
def histogram(heights):
    stack, best = [], 0
    a = heights+[0]
    for i,height in enumerate(a):
        while stack and a[stack[-1]] > height:
            h = a[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best,h*(i-left-1))
        stack.append(i)
    return best

@solution('Kth largest with duplicate values')
def kth(data):
    return sorted(data['nums'],reverse=True)[data['k']-1]

@solution('Top K frequent values')
def top_k(data):
    counts = Counter(data['nums'])
    return sorted(counts,key=lambda x:(-counts[x],x))[:data['k']]

@solution('Binary tree level order')
def tree_levels(a):
    if not a or a[0] is None:
        return []
    queue, result = [0], []
    while queue:
        result.append([a[i] for i in queue])
        queue = [j for i in queue for j in (2*i+1,2*i+2) if j < len(a) and a[j] is not None]
    return result

@solution('Binary tree maximum depth')
def tree_depth(a):
    def visit(i):
        if i >= len(a) or a[i] is None:
            return 0
        return 1+max(visit(2*i+1),visit(2*i+2))
    return visit(0)

@solution('Validate strict binary search tree')
def valid_bst(a):
    def visit(i,lo,hi):
        if i >= len(a) or a[i] is None:
            return True
        return lo < a[i] < hi and visit(2*i+1,lo,a[i]) and visit(2*i+2,a[i],hi)
    return visit(0,-math.inf,math.inf)

@solution('Undirected graph BFS order')
def bfs(data):
    adj = [[] for _ in range(data['n'])]
    for u,v in data['edges']:
        adj[u].append(v); adj[v].append(u)
    for neighbours in adj:
        neighbours.sort()
    queue, seen = [data['start']], {data['start']}
    for u in queue:
        for v in adj[u]:
            if v not in seen:
                seen.add(v); queue.append(v)
    return queue

@solution('Count four-connected islands')
def islands(grid):
    if not grid:
        return 0
    rows,cols = len(grid),len(grid[0])
    seen, result = set(), 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 1 or (i,j) in seen:
                continue
            result += 1
            stack = [(i,j)]; seen.add((i,j))
            while stack:
                x,y = stack.pop()
                for a,b in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                    if 0 <= a < rows and 0 <= b < cols and grid[a][b] == 1 and (a,b) not in seen:
                        seen.add((a,b)); stack.append((a,b))
    return result

@solution('Connected components with DSU')
def components(data):
    parent, size, count = list(range(data['n'])), [1]*data['n'], data['n']
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for u,v in data['edges']:
        u,v = find(u),find(v)
        if u != v:
            if size[u] < size[v]:
                u,v = v,u
            parent[v] = u; size[u] += size[v]; count -= 1
    return count

@solution('Bipartite graph check')
def bipartite(data):
    n = data['n']; adj = [[] for _ in range(n)]; colour = [-1]*n
    for u,v in data['edges']:
        adj[u].append(v); adj[v].append(u)
    for start in range(n):
        if colour[start] >= 0:
            continue
        queue = [start]; colour[start] = 0
        for u in queue:
            for v in adj[u]:
                if colour[v] == colour[u]:
                    return False
                if colour[v] < 0:
                    colour[v] = 1-colour[u]; queue.append(v)
    return True

@solution('Shortest unweighted path length')
def shortest_path(data):
    adj = [[] for _ in range(data['n'])]
    for u,v in data['edges']:
        adj[u].append(v); adj[v].append(u)
    distance = [-1]*data['n']; distance[data['start']] = 0
    queue = [data['start']]
    for u in queue:
        for v in adj[u]:
            if distance[v] < 0:
                distance[v] = distance[u]+1; queue.append(v)
    return distance[data['end']]

@solution('Dijkstra shortest distances')
def dijkstra(data):
    adj = [[] for _ in range(data['n'])]
    for u,v,w in data['edges']:
        adj[u].append((v,w))
    distance = [math.inf]*data['n']; distance[data['start']] = 0
    queue = [(0,data['start'])]
    while queue:
        d,u = heapq.heappop(queue)
        if d != distance[u]:
            continue
        for v,w in adj[u]:
            if d+w < distance[v]:
                distance[v] = d+w; heapq.heappush(queue,(d+w,v))
    return [None if d == math.inf else d for d in distance]

@solution('Directed acyclic graph detection')
def dag(data):
    adj = [[] for _ in range(data['n'])]; indegree = [0]*data['n']
    for u,v in data['edges']:
        adj[u].append(v); indegree[v] += 1
    queue = [i for i,d in enumerate(indegree) if d == 0]
    for u in queue:
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return len(queue) == data['n']

@solution('Generate subsets in lexicographic order')
def subsets(a):
    a = sorted(a)
    return sorted([list(c) for length in range(len(a)+1) for c in combinations(a,length)])

@solution('Count N-Queens solutions')
def queens(n):
    cols,diag1,diag2 = set(),set(),set()
    def visit(row):
        if row == n:
            return 1
        result = 0
        for col in range(n):
            if col in cols or row-col in diag1 or row+col in diag2:
                continue
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            result += visit(row+1)
            cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)
        return result
    return visit(0)

@solution('Coin change minimum coins')
def coin_change(data):
    amount = data['amount']; dp = [0]+[math.inf]*amount
    for value in range(1,amount+1):
        for coin in data['coins']:
            if coin <= value:
                dp[value] = min(dp[value],dp[value-coin]+1)
    return -1 if dp[amount] == math.inf else dp[amount]

@solution('Longest increasing subsequence length')
def lis(a):
    tails = []
    for value in a:
        index = bisect_left(tails,value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value
    return len(tails)

@solution('Longest common subsequence length')
def lcs(data):
    a,b = data; dp = [0]*(len(b)+1)
    for x in a:
        previous = 0
        for j,y in enumerate(b,1):
            old = dp[j]
            dp[j] = previous+1 if x == y else max(dp[j],dp[j-1])
            previous = old
    return dp[-1]

@solution('Edit distance with unit operations')
def edit_distance(data):
    a,b = data; dp = list(range(len(b)+1))
    for i,x in enumerate(a,1):
        previous = dp[0]; dp[0] = i
        for j,y in enumerate(b,1):
            old = dp[j]
            dp[j] = previous if x == y else 1+min(previous,dp[j],dp[j-1])
            previous = old
    return dp[-1]

@solution('0/1 knapsack maximum value')
def knapsack(data):
    capacity = data['capacity']; dp = [0]*(capacity+1)
    for w,v in zip(data['weights'],data['values']):
        for c in range(capacity,w-1,-1):
            dp[c] = max(dp[c],dp[c-w]+v)
    return dp[-1]

@solution('Unique grid paths')
def grid_paths(data):
    m,n = data; dp = [1]*n
    for _ in range(1,m):
        for j in range(1,n):
            dp[j] += dp[j-1]
    return dp[-1]

@solution('Word break feasibility')
def word_break(data):
    text,words = data['text'],set(data['words'])
    dp = [True]+[False]*len(text)
    for i in range(1,len(text)+1):
        dp[i] = any(dp[j] and text[j:i] in words for j in range(i))
    return dp[-1]

@solution('Minimum window containing a multiset')
def minimum_window(data):
    text,target = data
    if not target:
        return ''
    need,missing,left,best = Counter(target),len(target),0,''
    for right,c in enumerate(text):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if not best or right-left+1 < len(best):
                best = text[left:right+1]
            c = text[left]; left += 1; need[c] += 1
            if need[c] > 0:
                missing += 1
    return best

@solution('Range sum queries')
def range_sums(data):
    prefix = [0]
    for value in data['nums']:
        prefix.append(prefix[-1]+value)
    return [prefix[right+1]-prefix[left] for left,right in data['queries']]

@solution('Trie prefix counts')
def prefixes(data):
    root = {'count':0,'next':{}}
    for word in data['words']:
        node = root; node['count'] += 1
        for c in word:
            node = node['next'].setdefault(c,{'count':0,'next':{}})
            node['count'] += 1
    result = []
    for prefix in data['prefixes']:
        node = root
        for c in prefix:
            node = node['next'].get(c)
            if node is None:
                break
        result.append(node['count'] if node is not None else 0)
    return result

@solution('Reverse a singly linked list')
def reverse_linked(values):
    class Node:
        def __init__(self, value, next_node=None):
            self.value, self.next = value, next_node
    head = None
    for value in reversed(values):
        head = Node(value, head)
    previous = None
    while head is not None:
        following = head.next
        head.next = previous
        previous, head = head, following
    result = []
    while previous is not None:
        result.append(previous.value)
        previous = previous.next
    return result

@solution('Remove nth linked node from the end')
def remove_nth(data):
    class Node:
        def __init__(self, value=None):
            self.value, self.next = value, None
    dummy = Node()
    tail = dummy
    for value in data['values']:
        tail.next = Node(value)
        tail = tail.next
    fast = slow = dummy
    for _ in range(data['n']):
        fast = fast.next
    while fast.next is not None:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    result, node = [], dummy.next
    while node is not None:
        result.append(node.value)
        node = node.next
    return result

@solution('Find linked-list cycle entry')
def linked_cycle(data):
    class Node:
        def __init__(self, index):
            self.index, self.next = index, None
    nodes = [Node(i) for i in range(len(data['values']))]
    for i, node in enumerate(nodes):
        node.next = nodes[i+1] if i+1 < len(nodes) else nodes[data['pos']] if data['pos'] >= 0 else None
    slow = fast = nodes[0] if nodes else None
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = nodes[0]
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow.index
    return -1

@solution('Merge two sorted linked lists')
def merge_linked(data):
    class Node:
        def __init__(self, value=None, next_node=None):
            self.value, self.next = value, next_node
    def build(values):
        head = None
        for value in reversed(values):
            head = Node(value, head)
        return head
    left, right = map(build, data)
    dummy = Node()
    tail = dummy
    while left is not None and right is not None:
        if left.value <= right.value:
            tail.next, left = left, left.next
        else:
            tail.next, right = right, right.next
        tail = tail.next
    tail.next = left if left is not None else right
    result, node = [], dummy.next
    while node is not None:
        result.append(node.value)
        node = node.next
    return result

@solution('Merge K sorted streams with a heap')
def merge_streams(data):
    heads = [(stream[0], i, 0) for i, stream in enumerate(data) if stream]
    heapq.heapify(heads)
    result = []
    while heads:
        value, stream, index = heapq.heappop(heads)
        result.append(value)
        if index+1 < len(data[stream]):
            heapq.heappush(heads, (data[stream][index+1], stream, index+1))
    return result

@solution('Median after each stream insertion')
def prefix_medians(values):
    lower, upper, result = [], [], []
    for value in values:
        if not lower or value <= -lower[0]:
            heapq.heappush(lower, -value)
        else:
            heapq.heappush(upper, value)
        if len(lower) > len(upper)+1:
            heapq.heappush(upper, -heapq.heappop(lower))
        elif len(upper) > len(lower):
            heapq.heappush(lower, -heapq.heappop(upper))
        result.append((-lower[0]+upper[0])/2 if len(lower) == len(upper) else -lower[0])
    return result

@solution('Partition into two equal-sum subsets')
def equal_partition(values):
    total = sum(values)
    if total % 2:
        return False
    target = total//2
    possible = [False]*(target+1)
    possible[0] = True
    for value in values:
        for amount in range(target, value-1, -1):
            possible[amount] |= possible[amount-value]
    return possible[target]

@solution('Lowest common ancestor in a binary tree')
def lowest_ancestor(data):
    tree, p, q = data['tree'], data['p'], data['q']
    def visit(index):
        if index >= len(tree) or tree[index] is None:
            return None
        if tree[index] in (p,q):
            return tree[index]
        left, right = visit(index*2+1), visit(index*2+2)
        if left is not None and right is not None:
            return tree[index]
        return left if left is not None else right
    return visit(0)

@solution('Binary tree diameter in edges')
def tree_diameter(tree):
    best = 0
    def depth(index):
        nonlocal best
        if index >= len(tree) or tree[index] is None:
            return 0
        left, right = depth(index*2+1), depth(index*2+2)
        best = max(best, left+right)
        return 1+max(left,right)
    depth(0)
    return best

@solution('Longest palindromic substring')
def longest_palindrome(text):
    start = length = 0
    for centre in range(len(text)):
        for gap in (0,1):
            left, right = centre, centre+gap
            while left >= 0 and right < len(text) and text[left] == text[right]:
                if right-left+1 > length:
                    start, length = left, right-left+1
                left, right = left-1, right+1
    return text[start:start+length]

@solution('Lexicographically smallest course order')
def course_order(data):
    n = data['n']
    graph, indegree = [[] for _ in range(n)], [0]*n
    for u,v in data['edges']:
        graph[u].append(v)
        indegree[v] += 1
    ready = [i for i in range(n) if indegree[i] == 0]
    heapq.heapify(ready)
    result = []
    while ready:
        node = heapq.heappop(ready)
        result.append(node)
        for other in graph[node]:
            indegree[other] -= 1
            if indegree[other] == 0:
                heapq.heappush(ready,other)
    return result if len(result) == n else []

@solution('Minimum spanning forest weight')
def forest_weight(data):
    parent, size = list(range(data['n'])), [1]*data['n']
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node
    total = 0
    for u,v,weight in sorted(data['edges'], key=lambda edge:edge[2]):
        u,v = find(u),find(v)
        if u == v:
            continue
        if size[u] < size[v]:
            u,v = v,u
        parent[v] = u
        size[u] += size[v]
        total += weight
    return total

if __name__ == '__main__':
    sources = {}
    header = 'import json, sys, math, heapq\nfrom collections import Counter, deque\nfrom bisect import bisect_left, bisect_right\nfrom itertools import combinations\n\n'
    for title,fn in SOLUTIONS.items():
        source = inspect.getsource(fn).split('\n',1)[1]
        sources[title] = header+source+'\ndata = json.loads(sys.stdin.readline())\nprint(json.dumps('+fn.__name__+'(data), separators=(",", ":")))\n'
    output = Path(__file__).resolve().parents[1]/'assets/python-data.js'
    output.write_text('window.CODELAB_PYTHON='+json.dumps(sources,ensure_ascii=False,separators=(',',':'))+';\nfor (const q of window.CODELAB_CODING) { if(window.CODELAB_PYTHON[q.title]) q.referenceCode.python=window.CODELAB_PYTHON[q.title]; }\n',encoding='utf-8')
    print('Built',len(sources),'additional Python references.')
