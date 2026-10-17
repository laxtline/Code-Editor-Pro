from .common import course,lesson

def build():
 c=course('dsa','DSA with Python','Placement foundations','Learn invariants and patterns, then solve explicit judged tasks instead of memorising a solution list.','Foundation: 2-3 months; deeper practice is ongoing','Keep a topic notebook with a brute-force approach, improved invariant, complexity and regression cases for every solved pattern.',['dsa','python'])
 lesson(c,'dsa-complexity','Big-O, input contracts and a solving method',r'''
## Complexity describes growth
Time complexity counts how work grows with input size; space complexity counts relevant storage growth. Big-O is an asymptotic upper bound, not an exact runtime in milliseconds. State whether the analysis is worst-case, expected or amortised, and whether output/input storage is included.

A scan is O(n), a pair of nested full scans is O(n²), binary search is O(log n) under its ordering/random-access assumptions and comparison sorting commonly needs O(n log n). Two consecutive scans add to O(n), while a loop that halves a search region is not linear merely because it contains a loop.

## Solve from a contract
1. Restate input/output, indexing, empty cases and numeric limits.
2. Produce a correct small brute-force method and explicit examples.
3. Identify repeated work or structure: sorting, a monotone predicate, frequencies, overlapping subproblems or graph connectivity.
4. State an invariant for the improved method and trace a boundary case.
5. Analyse time/space and test against a small independent oracle.

Python can express most interview algorithms clearly. Language runtime and constants still matter under a particular time limit, so do not assume one language is universally required or sufficient for every platform.

The existing PDF roadmap targets are practice suggestions, not a claim that every company asks the same stages/questions. Use the staged judged tasks and reference library as resources while building actual topic coverage.
''','Compare an O(n²) pair-sum scan with a hash-based solution. State the duplicate/index policy, expected versus worst-case assumptions and explicit empty/no-answer cases.',[
 ('How do expected and worst-case complexity differ?','Expected complexity depends on a distribution/randomness or data-structure assumptions; worst-case bounds the most expensive valid input. State the assumption instead of labelling every hash lookup universally O(1).'),
 ('Why keep a brute-force solution?','It supplies a simple correctness baseline for small inputs and can serve as an independent oracle when testing the more complex optimised implementation.')],
 ('Two separate O(n) scans have which total asymptotic time?',['O(n)','O(n²)','O(log n)','O(1)'],0,'Adding 2n linear work still grows linearly after constant factors are ignored.'),
 ('python','def pair_sum(nums, target):\n    seen = set()\n    for value in nums:\n        if target-value in seen:\n            return True\n        seen.add(value)\n    return False\nprint(pair_sum([2, 7, 11], 9))\nprint(pair_sum([], 9))','True\nFalse'))
 lesson(c,'dsa-search-sort','Linear/binary search and five sorting methods',r'''
## Search the right structure
Linear search inspects candidates one by one. Binary search repeatedly discards half an ordered search space or uses a monotone predicate. Define a half-open or closed interval invariant and update it consistently; many errors come from mixing conventions.

For lower_bound, keep `[left,right)` with every index before left known smaller than the target and every index from right known not smaller. On termination, left is the first candidate position. A binary search on an answer needs a proved monotone feasibility predicate, not merely a numeric input.

## Sorting comparison
| Method | Typical/worst teaching bound | Key idea |
|---|---|---|
| Bubble | O(n²), with possible early exit | Swap adjacent inversions |
| Selection | O(n²) | Select the next minimum |
| Insertion | O(n²), useful on nearly sorted small data | Insert into a sorted prefix |
| Merge | O(n log n), extra merge storage | Sort halves and merge |
| Quick | Average O(n log n), worst O(n²) | Partition around a pivot |

Python's sort/sorted provide a stable library sort; a key function maps values to comparison keys. Stable means equal keys preserve relative order. In-place mutation and extra space are separate properties from stability.

Counting inversions extends merge sort: when a right-half value is taken before remaining larger left values, count those cross inversions. Keep the original comparison contract clear for equal values.
''','Implement lower_bound and test empty input, repeated targets and insertion at either end. Then count inversions with both a pair scan and a merge-based method on small random arrays.',[
 ('What does a stable sort preserve?','The relative order of items with equal sort keys. It does not mean the sort uses constant memory or that it is always the fastest choice.'),
 ('What must be true for binary search on an answer?','The feasibility predicate must be monotone over the search domain, with defined boundary behaviour. Without that property, discarding half the domain can remove a valid answer.')],
 ('What does lower_bound return?',['The first position whose value is not less than the target','Always the last equal element','The array maximum','Only an existing exact match'],0,'It is an insertion/candidate position, which may equal the array length.'),
 ('python','from bisect import bisect_left\nnums = [1, 2, 2, 5]\nprint(bisect_left(nums, 2))\nprint(bisect_left(nums, 4))','1\n3'))
 lesson(c,'dsa-array-patterns','Hashing, prefix sums, two pointers and windows',r'''
## Match the invariant to the input
A frequency map avoids repeated scans for counts or complements. A prefix sum turns a range sum into a difference of cumulative totals; seed the empty prefix correctly. For counting subarrays with a target sum, count earlier prefix frequencies instead of assuming a positive-only sliding window.

Two pointers can move inward on a sorted pair-sum problem or maintain a read/write boundary for in-place compaction. Explain why moving one pointer cannot discard a needed answer. Sorting first may change original indices, so preserve them when output requires original positions.

## Sliding windows
A fixed-size window updates by adding one value and removing the outgoing value. A variable window needs a condition under which extending/shrinking changes validity predictably. Negative numbers break several sum-based monotonic assumptions. A longest-substring-without-repeats window tracks the last occurrence/frequency and never moves its left boundary backwards.

Prefix XOR uses an analogous relation for XOR-range problems, but do not substitute arithmetic sum reasoning blindly. For exact pattern search, KMP keeps a prefix-function state so mismatches avoid rescanning already understood characters; overlapping matches require falling back to the proper prefix after a match.

Test duplicates, all-zero values, negative values where allowed, empty strings and overlapping patterns. Write the window's valid state before writing its update order.
''','Solve target-sum subarray counting with a frequency map and compare with a brute-force oracle. Give a counterexample to a positive-only sum window when negatives are allowed.',[
 ('Why seed a prefix frequency with zero once?','It represents the empty prefix before the array. A subarray beginning at index zero is counted by matching the current prefix against that initial zero.'),
 ('When can a sliding-window sum method fail?','When its validity is not monotone under extension/shrinking, such as several target-sum problems with negative values. Choose a prefix-map or another method that matches the actual contract.')],
 ('Which method naturally handles negative values for counting subarrays with sum k?',['Prefix sums with a frequency map','Always shrink only when the sum exceeds k','Sort the array and ignore positions','Use only the maximum element'],0,'Earlier prefix differences identify valid contiguous sums without a positive-only monotonicity assumption.'),
 ('python','nums, k = [1, -1, 0], 0\nfreq, prefix, answer = {0:1}, 0, 0\nfor value in nums:\n    prefix += value\n    answer += freq.get(prefix-k, 0)\n    freq[prefix] = freq.get(prefix, 0)+1\nprint(answer)','3'))
 lesson(c,'dsa-linear-structures','Linked lists, stacks, queues, deques and heaps',r'''
## Choose operations and ownership
A singly linked node points to a next node; a doubly linked node also tracks a previous link. Reversal must save the next link before overwriting it. A dummy node can simplify head deletion/merge cases. Floyd's slow/fast pointers detect a cycle under the linked traversal model; finding its entry needs the second phase, not only the meeting point.

A stack is LIFO and supports nested matching, DFS and monotonic patterns. A queue is FIFO and supports BFS. Use collections.deque for efficient end operations instead of repeated list.pop(0). A monotonic stack/deque discards dominated candidates while preserving the invariant needed by later queries.

## Heaps order candidates
Python heapq is a min-heap interface. Keep a size-k heap for selected streaming top-k tasks or merge sorted streams by the next available element. A heap is not a fully sorted list, and removing an arbitrary value is not automatically constant time.

For streaming median, balance a max-oriented lower half and min-oriented upper half with explicit size/order invariants. For sliding-window maximum, store indices in a decreasing deque so expired values can be removed by position.

Trace empty/single-node lists, deletion at the head, repeated equal values and an expired maximum. Separate object identity from equality when reasoning about a cycle.
''','Reverse a linked list with three pointers, then solve next-greater-element using a monotonic stack. Explain why each element is pushed/popped only a bounded number of times.',[
 ('Why does a monotonic stack often give linear time?','Although one iteration can pop several values, each value is pushed once and popped at most once. The total number of stack operations across the full scan is linear.'),
 ('Why store indices rather than only values in a sliding-window deque?','Indices identify expiry and preserve the relationship to positions, including duplicates. Values alone cannot always distinguish an old equal maximum from a current one.')],
 ('Which is the usual Python queue choice for BFS?',['collections.deque','Repeated list.pop(0)','A sorted copy on every step','A string with concatenated node IDs'],0,'deque supports efficient appends and removals at opposite ends.'),
 ('python','from collections import deque\nqueue = deque([1, 2])\nqueue.append(3)\nprint(queue.popleft())\nprint(list(queue))','1\n[2, 3]'))
 lesson(c,'dsa-trees','Trees, BSTs, tries and ancestor queries',r'''
## A traversal defines processing order
DFS traversals of a binary tree include preorder (node/left/right), inorder (left/node/right) and postorder (left/right/node). BFS visits levels using a queue. Define whether height/diameter counts edges or nodes before implementing it; a one-node tree exposes that convention immediately.

A strict BST has all keys in a left subtree below the node and all in a right subtree above it. Checking only immediate children is insufficient; propagate allowed bounds. Deletion and duplicate policies need explicit contracts.

## Common tree patterns
Postorder can return a useful summary, such as subtree height, while updating a global/returned diameter. LCA reasoning depends on whether the tree is a general binary tree, a BST or a rooted parent array. Binary lifting precomputes 2^j ancestors to answer kth-ancestor queries in logarithmic steps.

A trie stores prefixes along character edges and supports prefix membership/counts with a clear terminal-marker/count policy. Empty words, duplicate insertions and deletion counts need explicit handling.

Recursion depth can exceed a runtime limit on a long chain. An iterative stack can be appropriate even when the recursive invariant is easiest to explain. Test a balanced tree, a chain, missing children, repeated labels where allowed and a query above the root.
''','Explain why checking only each BST node\'s direct children fails, then create a counterexample. Build a small ancestor table and answer k=0, k=1 and above-root queries.',[
 ('Why do BST validation bounds need to come from ancestors?','A node can satisfy its parent comparison while violating a higher ancestor\'s range. Propagating lower/upper bounds enforces the property across the entire subtree.'),
 ('How does binary lifting help ancestor queries?','It precomputes jumps of lengths 1,2,4,... and decomposes k into binary bits. Queries then follow only logarithmically many jumps, with a defined missing-ancestor value.')],
 ('For a diameter measured in edges, what is a single-node tree\'s diameter?',['0','1','2','Undefined for every valid tree'],0,'There are no edges on its longest path.'),
 ('python','def inorder(tree):\n    if tree is None:\n        return []\n    value, left, right = tree\n    return inorder(left) + [value] + inorder(right)\nprint(inorder((2, (1,None,None), (3,None,None))))','[1, 2, 3]'))
 lesson(c,'dsa-graphs','BFS, DFS, shortest paths, DSU and graph structure',r'''
## State the graph contract
Define directed/undirected edges, weights, self-loops, parallel edges and unreachable vertices. An adjacency list is often appropriate for sparse graphs. Mark visited at the correct point so cycles do not create unbounded repeated work.

BFS finds shortest edge-count paths in an unweighted graph. DFS explores components and supports ordering/low-link reasoning. Dijkstra assumes nonnegative weights; Bellman-Ford can handle negative edges and detect a reachable negative cycle. Floyd-Warshall considers intermediate vertices for all-pairs shortest paths and needs a separate policy for negative cycles.

## Other useful structures
DSU maintains connectivity through representative roots, usually with path compression and size/rank heuristics. Topological sorting applies to directed acyclic graphs; a cycle means no valid full order. A lexicographically smallest topological order needs an ordered candidate structure.

Strongly connected components group mutually reachable directed vertices. Undirected bridges need low-link reasoning and correct edge identity for parallel edges. Bipartite matching can use augmenting paths; a failed greedy pair choice does not prove that no larger matching exists.

For every algorithm, write its assumptions and complexity in terms of V/E. Test disconnected graphs, isolated vertices, a self-loop where permitted, duplicate/parallel edges and an unreachable negative cycle. A graph picture alone is not an input specification.
''','Choose algorithms for unweighted routes, nonnegative weighted routes and graphs with negative edges. Explain a duplicate-edge bridge case and a greedy matching counterexample.',[
 ('Why is Dijkstra not generally valid with negative edges?','Its finalisation argument depends on nonnegative extension costs. A later path through a negative edge can invalidate an already treated shortest distance.'),
 ('Why must a bridge algorithm distinguish parallel edge IDs?','One edge to the parent is the DFS tree edge, but another parallel edge is a valid back connection. Treating every parent-neighbour edge as the same can falsely report a bridge.')],
 ('Which algorithm directly finds shortest edge-count paths in an unweighted graph?',['BFS','Arbitrary DFS order','Selection sort','A stack that ignores visited vertices'],0,'BFS explores increasing distance layers in the unweighted setting.'),
 ('python','from collections import deque\ngraph = [[1,2],[3],[3],[]]\ndistance = [-1]*len(graph); distance[0]=0\nqueue=deque([0])\nwhile queue:\n    node=queue.popleft()\n    for nxt in graph[node]:\n        if distance[nxt] == -1:\n            distance[nxt]=distance[node]+1;queue.append(nxt)\nprint(distance)','[0, 1, 1, 2]'))
 lesson(c,'dsa-dp','Dynamic programming: state, transitions and order',r'''
## Store the repeated subproblem
Dynamic programming is useful when a problem has overlapping subproblems and an appropriate optimal/substructure relation. Define exactly what one state means before writing a table. Then specify base cases, transitions, evaluation order and how the final answer is extracted.

Memoisation computes states on demand through recursion; tabulation chooses an explicit order. Space optimisation is valid only when old values are no longer needed. For 0/1 knapsack, iterating capacity in the wrong direction can accidentally reuse an item and turn it into a different problem.

## Recognise families
Grid DP moves among cells, string DP compares prefixes/substrings and tree DP combines child summaries. LIS needs a precise subsequence-versus-substring distinction. LCS and edit distance have different transitions and objectives. Interval DP chooses a split or last action inside a range, as in matrix-chain cost or burst balloons.

Digit DP processes a numeric bound with position, tightness, leading-zero and relevant history state. Define how zero itself is counted. A missing leading-zero policy often double-counts shorter numbers or imposes a false adjacency constraint.

Test a small brute-force oracle, boundary dimensions and an impossible state. Use a suitable infinity/sentinel and avoid treating an unreachable state as a valid zero-cost solution. Reconstructing one solution requires predecessor/choice information beyond merely returning the optimal value.
''','Define the state and transition for 0/1 knapsack and for palindrome minimum cuts. Explain iteration direction and test against exhaustive subsets/partitions on small inputs.',[
 ('Why does state meaning come before code?','It determines which information is sufficient for a subproblem and which transitions are valid. A table with an unclear meaning is difficult to initialise, order or prove correct.'),
 ('Why can a one-dimensional knapsack loop direction change the problem?','Updating capacities upward can reuse a value written for the same item, allowing that item multiple times. Descending capacity preserves the previous-item dependency for 0/1 selection.')],
 ('Which is a subsequence property?',['Elements keep relative order but need not be contiguous','Elements must occupy adjacent positions','Elements must be sorted by original index and value automatically','Every character must be unique'],0,'A subsequence preserves order; a substring/subarray is contiguous.'),
 ('python','weights, values, capacity = [2,3], [4,5], 3\ndp = [0]*(capacity+1)\nfor weight,value in zip(weights,values):\n    for cap in range(capacity,weight-1,-1):\n        dp[cap] = max(dp[cap], dp[cap-weight]+value)\nprint(dp[capacity])','5'))
 lesson(c,'dsa-design','Backtracking, greedy proof, bits and range-query structures',r'''
## Explore and undo
Backtracking maintains a partial solution, chooses a candidate, checks/prunes constraints, recurses and restores state. Subsets, permutations, N-Queens and word search differ in candidate/duplicate rules. A prune must be proved safe; an aggressive guess can discard a valid answer.

Greedy algorithms make a locally chosen step whose global correctness needs an argument, often an exchange argument or a maintained frontier invariant. Choosing the earliest finish works for maximum count of nonoverlapping intervals, but weighted interval profit needs a different method such as DP with compatible predecessors.

## Bit reasoning
Use shifts/masks for flags and binary states, with clear integer-width/sign assumptions. `x & (x-1)` clears one set bit for a positive integer. XOR has useful cancellation properties but does not sort values or preserve ordinary addition semantics.

## Dynamic range queries
A prefix sum is excellent for static ranges but costly to rebuild after every update. A Fenwick tree supports prefix sums and point additions in O(log n); range sums are differences of prefixes. A segment tree combines an associative summary over intervals and can support different queries/updates with a defined identity. Do not mix point-update and lazy range-update contracts accidentally.

Explain the invariant and compare with a simple list scan on small random operation sequences. A complex data structure earns its place when the query/update workload requires it.
''','Generate subsets without duplicates, give a greedy exchange argument for unweighted interval scheduling and compare Fenwick versus segment-tree operations on one update/query workload.',[
 ('What makes a greedy solution convincing?','A correctness argument showing the local choice preserves an optimal solution or invariant. Passing a few examples does not establish that the choice is always safe.'),
 ('When is a Fenwick tree useful?','For workloads such as point additions and prefix/range sum queries where both updates and queries need logarithmic time. It is not a universal replacement for every range aggregate or update type.')],
 ('For positive x, what does x & (x-1) do?',['Clears the lowest set bit','Always doubles x','Sorts the bits','Always returns x+1'],0,'Subtracting one flips the lowest set bit and lower zeros; AND removes that one set bit.'),
 ('python','x, count = 13, 0\nwhile x:\n    x &= x-1\n    count += 1\nprint(count)','3'))

 c=course('native-languages','C, C++ & Java','Compiled language basics','Use the normal editor with a real installed compiler and explicit stdin/stdout contracts.','Choose one language, then practise daily','Write and test a small command-line program; use local compilers only for code you intend to run on your computer.',['c','cpp','java','dsa'])
 lesson(c,'c-basics','C: values, arrays, pointers and safe input',r'''
## Compile before execution
C source is translated and linked into a native program. Learn compiler diagnostics separately from runtime errors and wrong output. This site's local launcher detects GCC/Clang when installed; GitHub Pages itself cannot run the computer's compiler.

## Storage and bounds
Declare suitable types and match format specifiers. A C array has a fixed bound in its declared storage; passing it to many functions decays to a pointer, so its length often needs a separate argument. A pointer is an address-like reference under the language's rules, not a guarantee that dereferencing it is valid.

Avoid out-of-bounds access, use-after-free and uninitialised reads. Allocate dynamically with a clear ownership/free policy, check allocation failure and keep size arithmetic within range. Undefined behaviour can appear to work in one build and fail in another; a successful sample run is not proof of safety.

## Input/output contract
Check scanf conversion counts for a small numeric exercise, or read bounded lines and parse with a deliberate error policy. Never use an unbounded string read into a fixed array. Print exactly the requested result; extra prompts break automated judging.

For JSON-I/O tasks, C needs a real parser or an explicitly implemented supported subset; the generic starter intentionally does not pretend arbitrary JSON is one scanf away. Choose a plain-input task or implement the contract fully.
''','Write a C program that reads two integers, checks the conversion count and prints their sum. Test invalid input and explain the valid numeric range.',[
 ('Why pass array length to a C function?','A pointer parameter does not generally carry the original array bound. The function needs an explicit valid length or another well-defined termination contract to avoid reading outside the object.'),
 ('What is undefined behaviour?','The language does not prescribe the program\'s behaviour for that operation. Apparent success on one compiler/input is not a guarantee and can change with optimisation or environment.')],
 ('What should a judged program print?',['Exactly the specified output','Extra friendly input prompts by default','The whole source code','A success claim before reading input'],0,'Automated judging compares the required output contract, so extra prompts can make an otherwise correct calculation fail.'),
 ('c','#include <stdio.h>\nint main(void) {\n    long long a, b;\n    if (scanf("%lld %lld", &a, &b) != 2) return 1;\n    printf("%lld\\n", a + b);\n    return 0;\n}','42','20 22\n'))
 lesson(c,'cpp-basics','C++: STL containers, references and RAII',r'''
## Use ownership-aware library types
C++ offers native performance and a rich standard library. vector manages a dynamic contiguous array, string manages text, unordered_map offers expected hash-based lookup and map offers ordered-key operations. Choose by the required access/ordering contract and state the complexity assumptions.

References alias existing objects. Pass a large read-only input by const reference where appropriate; copying can be intentional when the algorithm needs independent ownership. Iterator/reference invalidation depends on the container and operation, so do not retain a vector element reference across arbitrary reallocating pushes.

## RAII
An object's lifetime owns cleanup through its destructor. Standard containers, smart pointers and lock guards reduce scattered manual resource management. RAII is not a substitute for a sensible ownership graph, and shared ownership can still create cycles.

Use long long or another suitable type when sums exceed int range and verify multiplication/overflow assumptions before computing. A comparator must define a valid ordering, not a random or contradictory rule. Standard sort is not a stable sort unless the selected operation provides that property.

The local runner uses a C++17 contract with detected GCC/Clang. The example uses only standard headers; platform-specific headers and external JSON libraries are not automatically installed by the app.
''','Read n integers into a vector, compute their sum and sort a copy. Explain ownership, overflow assumptions and which operations can invalidate references.',[
 ('What does RAII achieve?','It ties resource acquisition/release to object lifetime so destructors perform cleanup on normal scope exit and exception unwinding. Clear ownership still matters.'),
 ('Why use const reference for a read-only vector parameter?','It avoids copying a potentially large container while expressing that the function should not mutate it through that reference. The caller must keep the referenced object alive.')],
 ('Which container is a usual dynamic contiguous sequence?',['std::vector','A raw pointer with no length contract','std::mutex','A stream error code'],0,'vector manages a contiguous dynamic sequence with defined size/capacity semantics.'),
 ('cpp','#include <iostream>\n#include <vector>\n#include <numeric>\nint main() {\n    int n; if (!(std::cin >> n) || n < 0) return 1;\n    std::vector<long long> a(n);\n    for (auto &x : a) if (!(std::cin >> x)) return 1;\n    std::cout << std::accumulate(a.begin(), a.end(), 0LL) << "\\n";\n}','42','3\n10 12 20\n'))
 lesson(c,'java-basics','Java: classes, collections and the JDK',r'''
## The JDK includes development tools
javac compiles source to class files and java runs a suitable entry point on the JVM. A JRE-only installation may not include the compiler. This app's local runner expects a Main class in Main.java and detects a JDK; it does not download one silently.

## Values and object references
Primitive values and object references have different semantics. Strings are immutable and value comparison normally uses equals rather than reference identity with ==. Use generics for typed collections such as List<Integer> and Map<String,Integer>, while remembering boxing and null-related cases.

ArrayList supports a dynamic indexed sequence; HashMap/HashSet provide expected hash-based operations. A Queue/Deque implementation can suit BFS/stack use. Do not assume every collection operation is constant time or that a hash container has sorted iteration order.

## Input and errors
Scanner is convenient for small exercises; buffered input/parsing can be appropriate for large contest data. Validate the expected input and choose int/long according to constraints. Handle exceptions at a useful boundary instead of catching everything and printing a fake result.

Use classes/interfaces to model contracts and composition for collaborators. Garbage collection reclaims unreachable memory but does not close every external resource at the correct business time; use try-with-resources for suitable closeable objects.
''','Write a Main program that reads two long values and prints their sum. Then compare two independently created equal strings with == and equals and explain the result.',[
 ('How do JDK and a runtime-only installation differ?','A JDK includes development tools such as javac as well as runtime capabilities. Native local judging needs a compiler, not only a java executable.'),
 ('Why use equals for string contents?','== compares reference identity for objects. equals expresses value/content equality according to the class contract, so independently created equal strings can compare equal by contents.')],
 ('Which tool compiles Java source?',['javac','Only a CSS bundler','git push','A browser title tag'],0,'javac is the JDK compiler that produces class files from source.'),
 ('java','import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner input = new Scanner(System.in);\n        long a = input.nextLong(), b = input.nextLong();\n        System.out.println(a + b);\n    }\n}','42','20 22\n'))
