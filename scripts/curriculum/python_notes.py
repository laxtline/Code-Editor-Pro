from .common import course,lesson

def build():
 c=course('python','Python','Language foundations','Build programming logic, then write typed, tested automation and backend code.','Beginner path: 4-6 weeks','Build a command-line task tracker with JSON persistence, validation, tests and a short README.',['python'])
 lesson(c,'py-setup','Setup, modules and environments',r'''
## What runs a Python program?
An interpreter reads your Python source and executes it. The editor helps you write the file; it is not the interpreter. Save a script as `main.py`, open its folder in a terminal, and run `python main.py` (or `py -3 main.py` on Windows).

## Set up a repeatable project
1. Create a folder for one project, not one folder shared by every experiment.
2. Run `python -m venv .venv`. Activate `.venv\Scripts\Activate.ps1` on Windows or `source .venv/bin/activate` on Unix. Activation changes the shell's Python search path; it does not install a second operating system.
3. Select that interpreter in VS Code. Use `python -m pip install package_name` so pip belongs to the same interpreter.
4. Record dependencies in `pyproject.toml` or a requirements file; keep `.venv/` out of Git. A lockfile adds reproducible resolved versions. `uv` is an alternative environment/package tool.

## Organise code before it grows
A module is one `.py` file. A package groups modules. Import useful definitions, keep side effects out of imports, and put CLI startup behind `if __name__ == "__main__":`. Run a package entry point with `python -m package_name` when relative imports require package context.

Ruff can lint/format code; pre-commit runs selected checks before a commit. These tools catch mechanical issues, while tests check behaviour. Inside this site's browser Python engine, standard-library examples work without installing Python locally; project package installation belongs to your local environment.
''','Create `math_tools.py` with an `add` function and a separate `main.py` that imports it. Add a `.gitignore` and explain how another person creates the environment.',[
 ('Why use a virtual environment?','It gives each project its own installed Python packages. Two projects can depend on different versions without overwriting each other. Recreate it from dependency metadata instead of committing the environment directory.'),
 ('Why use the __main__ guard?','Importing a module should make its definitions available without unexpectedly starting a CLI, network request or server. The guard runs startup code only when that module is the entry point.')],
 ('Which command installs into the interpreter currently selected by python?',['python -m pip install requests','copy requests into every folder','git install requests','python main.py --pip'],0,'The -m form asks that interpreter to run its pip module.'),
 ('python','import sys\nfrom pathlib import Path\nprint(sys.version_info.major)\nprint(Path("notes.txt").suffix)','3\n.txt'),skills=[7,10,24])
 lesson(c,'py-values','Values, variables, input and mutability',r'''
## Names point to objects
`age = 21` binds a name to an integer object. A name can later reference a different type because Python checks types at runtime. Learn `int`, `float`, `str`, `bool` and `None` before adding libraries. `type(value)` helps inspect a value; it does not replace a well-designed input contract.

`input()` returns text, even when the user types digits. Convert explicitly with `int()` or `float()`, and handle invalid input. `print()` writes output. Comments begin with `#`; meaningful names explain more than a comment that merely repeats the next statement.

## Operators and conditions
`/` performs true division, `//` floor division, `%` remainder and `**` exponentiation. Floor division rounds down: `-3 // 2` is `-2`. Compare with `==`, `!=`, `<`, `<=`, `>` and `>=`. `=` assigns; it does not compare. `and`, `or` and `not` combine conditions; `and` and `or` return operands, so they are not always booleans.

## Mutable versus immutable
Integers, strings and tuples are immutable; lists and dictionaries are mutable. Assignment does not copy an object. If `b = a` and both names reference a list, `b.append(3)` changes the list seen by `a`. A shallow copy duplicates the outer list, not every nested object. Use `is` for identity, especially `value is None`; use `==` for value equality.

Empty containers, zero, `None` and empty strings are false in conditions. Do not confuse `0` with a missing value when zero is valid input. Prefer an explicit `is None` check in that situation.
''','Read two integers and print their sum, integer quotient and remainder. Then demonstrate an alias bug with a nested list and repair it.',[
 ('What is the difference between == and is?','== asks whether two values compare equal. is asks whether both references point to the same object. Two independently created lists can be equal while having different identities.'),
 ('Does assigning a list copy it?','No. Both names reference the same list. list.copy() creates a new outer list, while nested mutable objects can still be shared; use a deliberate deep copy only when that ownership is required.')],
 ('After a=[1]; b=a; b.append(2), what is a?',['[1, 2]','[1]','[2]','None'],0,'Assignment creates an alias; append mutates the shared list.'),
 ('python','a = [1]\nb = a\nb.append(2)\nprint(a)\nprint(-3 // 2)','[1, 2]\n-2'),skills=[1,2])
 lesson(c,'py-control','Conditions, loops and tracing',r'''
## Turn a requirement into branches
Use `if`, `elif` and `else` for mutually ordered decisions. Python uses indentation to define a block, so inconsistent indentation changes meaning or produces an error. Start with a small decision table: valid input, boundary input and invalid input. For a grade classifier, decide whether the top boundary includes equality before writing comparisons.

## Repeat safely
`for item in iterable` visits items. `range(start, stop, step)` excludes `stop`. `while condition` repeats until its condition becomes false; ensure some state changes towards termination. `break` exits the nearest loop; `continue` skips to its next iteration. A loop's `else` runs when it finishes without `break`, which can express a search that found nothing.

## A tracing method that works in interviews
1. Write the variable values before the first iteration.
2. Record the current item, condition result and updated variables for each step.
3. Check a loop invariant: for a running sum, the accumulator equals the sum of the items already processed.
4. Check termination and the final output separately.

Avoid changing a list's size while iterating over that same list. Build a new result, iterate over a copy, or use a comprehension. Do not hide an infinite loop behind a broad exception handler. An empty iterable is a useful test: a correct accumulator often needs to produce its identity value, such as zero for a sum.
''','Write a prime checker using a loop through possible divisors. Test 1, 2, a square and a prime. Explain why checking only through the square root is enough.',[
 ('How do break and continue differ?','break terminates the nearest loop immediately. continue moves to that loop\'s next iteration; the loop itself remains active. In a while loop, update the control variable before a possible continue to avoid getting stuck.'),
 ('What is a loop invariant?','It is a statement that holds before and after every iteration. Proving initialisation, preservation and the final consequence gives a structured argument for correctness.')],
 ('How many values are in range(2, 8, 2)?',['3','4','2','6'],0,'The values are 2, 4 and 6; the stop value 8 is excluded.'),
 ('python','total = 0\nfor n in range(1, 6):\n    if n % 2 == 0:\n        continue\n    total += n\nprint(total)','9'))
 lesson(c,'py-strings','Strings, slicing and text handling',r'''
## Text is a sequence
Strings support indexing, slicing and iteration. Index zero is the first character, negative indices count from the end, and `s[a:b]` excludes `b`. A slice creates a string; it does not mutate the original. Python strings contain Unicode characters, so do not assume every character is one byte or every visible symbol is one code point.

## Useful transformations
`strip()` removes leading/trailing whitespace; `split()` without an argument collapses runs of whitespace. `separator.join(parts)` joins strings efficiently. Use `lower()` or `casefold()` deliberately for case-insensitive matching, and f-strings for readable formatting. A `replace()` call returns a new string. Save that result if you need it later.

## Parse before processing
For a comma-separated pair, split, trim and validate the expected field count before conversion. For real CSV files, use the `csv` module rather than splitting on commas: quoted fields can themselves contain commas or newlines. For JSON, use `json.loads()` and `json.dumps()` instead of string concatenation.

Repeatedly building a long string with concatenation can create many intermediate objects. Collect fragments and join once when processing large inputs. For a palindrome, define whether punctuation and case count before choosing a two-pointer or reverse-and-compare implementation. Good text algorithms begin with a precise character and normalisation contract.
''','Normalise a sentence by collapsing whitespace and reversing its word order. Then write a separate palindrome checker that ignores only ASCII spaces and case; document that exact contract.',[
 ('Why is join useful?','It combines a sequence of text fragments with a chosen separator in one operation. It communicates intent clearly and avoids repeatedly rebuilding a growing string inside a loop.'),
 ('Why not parse CSV with split(",")?','CSV quoting allows a field to contain commas, quotes and line breaks. A CSV parser understands those rules; a plain split does not.')],
 ('What does "  a   b  ".split() return?',['["a", "b"]','["", "a", "", "", "b", ""]','"a b"','["a   b"]'],0,'split() without a separator treats runs of whitespace as delimiters.'),
 ('python','text = "  learn   one concept  "\nwords = text.split()\nprint(" ".join(reversed(words)))','concept one learn'))
 lesson(c,'py-collections','Lists, tuples, sets, dictionaries and comprehensions',r'''
## Choose by the operation
Use a list for ordered items with duplicates, a tuple for a fixed record, a set for uniqueness/membership and a dictionary for key-to-value lookup. Modern Python dictionaries preserve insertion order; sets do not provide a sorted sequence. Dictionary keys must be hashable. An immutable tuple is hashable only when its contents are hashable too.

List indexing is constant time; searching an unsorted list is linear. Appending is amortised constant time, while inserting at the front moves existing elements. Dictionary/set membership is expected constant time, with a worst case that is not guaranteed constant. `collections.deque` is usually a better queue than repeated `list.pop(0)`.

## Build a frequency table
Start an empty dictionary. For each value, increment `counts[value]` using a default of zero, or use `collections.Counter`. This replaces repeated rescans with one pass. Keep the distinction between a missing key and a key whose value is zero.

## Comprehensions
`[expression for item in source if condition]` transforms and filters. Dictionary and set comprehensions use the same idea. A generator expression produces values lazily rather than materialising every result. Prefer an ordinary loop when nested conditions or side effects make a comprehension hard to read.

The common grid trap is `[[0]*3]*3`: every row references the same list. Build each row independently with a comprehension. Copying containers without understanding which nested objects remain shared causes subtle state bugs.
''','Count word frequencies without repeated list.count() calls. Build a 3-by-3 independent grid and prove that changing one cell leaves the other rows unchanged.',[
 ('When should a set replace a list?','When the operation is uniqueness or repeated membership checks and you do not need duplicates or positional indexing. A set changes the data contract, so it is not a drop-in replacement for every list.'),
 ('Why can a tuple contain a mutable list?','Tuple immutability prevents rebinding its element slots. It does not freeze the objects referenced by those slots; a contained list can still change.')],
 ('Which creates three independent rows?',['[[0]*3 for _ in range(3)]','[[0]*3]*3','[0]*9','tuple([0]*3)'],0,'The comprehension evaluates a new inner list for every row.'),
 ('python','from collections import Counter\nwords = "code test code learn".split()\nprint(dict(Counter(words)))\nprint([n*n for n in range(5) if n % 2 == 0])',"{'code': 2, 'test': 1, 'learn': 1}\n[0, 4, 16]"),skills=[3,4])
 lesson(c,'py-functions','Functions, arguments, closures and type hints',r'''
## Give a function one contract
A function receives inputs, performs a small responsibility and returns a result. `print()` displays something; `return` passes a value to the caller. A function without an explicit return produces `None`. Keep calculation separate from input/output so the calculation is easy to test.

Positional arguments are matched by order; keyword arguments make call sites explicit. `*args` collects positional arguments and `**kwargs` collects keyword arguments. Default values are evaluated once when the function is defined. A default list is therefore shared across calls: use `None` and create a new list inside the function when you need fresh state.

## Scope and closures
Python looks up names through local, enclosing, global and built-in scopes. A closure retains access to an enclosing function's variables. Use `nonlocal` when rebinding a name in that enclosing scope. Prefer explicit arguments and return values over hidden mutable globals.

## Types help readers and tools
`def total(values: list[int]) -> int:` expresses an input/output contract. `int | None` represents an optional value on supported Python versions. Generics keep the relationship between input and output types. A static checker such as mypy or pyright can catch mismatches before runtime, but annotations alone do not validate network or file input.

Use runtime checks or a validation library at external boundaries. Avoid annotating everything as `Any`: that removes the checker precisely where you wanted help. Document what errors a function raises and whether it mutates its input.
''','Implement a typed function that returns the average of a nonempty numeric list and raises ValueError for an empty list. Test that it never mutates the input.',[
 ('What is the mutable-default-argument bug?','A default object is created once at function definition. Mutating a default list can leak data between calls. Use a None default and construct the list inside the function.'),
 ('Do type hints make input safe at runtime?','No. Static checkers analyse annotated code, but untrusted JSON can still have the wrong shape. Validate it when it enters the system and convert it to a trusted internal model.')],
 ('What does a function with no return statement return?',['None','0','False','An empty string'],0,'Python returns None when execution reaches the end of a function.'),
 ('python','def add_item(item, items=None):\n    if items is None:\n        items = []\n    items.append(item)\n    return items\nprint(add_item("a"))\nprint(add_item("b"))',"['a']\n['b']"),skills=[5,6])
 lesson(c,'py-oop','Classes, composition and dataclasses',r'''
## Model state with behaviour
A class defines how objects are constructed and what operations they support. `self` refers to the current instance. `__init__` initialises its state; it does not itself allocate the object. Put per-object lists on `self`, not in a shared class attribute unless sharing is intentional.

Encapsulation means callers use a clear interface instead of depending on internal representation. Python's `_name` convention signals an internal detail; it is not an access-control boundary. A property can validate access while keeping a simple attribute-like interface.

## Inheritance or composition?
Inheritance expresses substitutability: a specialised object should honour the base class's contract. Composition gives an object a collaborator, such as a report service that receives an email sender. Composition often makes tests easier because a small fake collaborator can replace a real network service.

Polymorphism means callers can use the same operation across compatible objects. It does not require a large inheritance tree. Duck typing asks whether an object supports the required behaviour. Use abstract base classes or protocols when an explicit contract adds value.

## Dataclasses
A dataclass generates record conveniences such as an initializer, representation and value equality. Use `field(default_factory=list)` for a new list per instance. A frozen dataclass prevents ordinary attribute rebinding, but nested mutable values can still change. Useful dunder methods include `__repr__`, `__eq__`, `__len__` and iteration methods; implement only meaningful contracts.
''','Create a Task dataclass and a TaskRepository interface. Implement an in-memory repository and test a service with it before adding JSON persistence.',[
 ('Why prefer composition for a payment service?','Payment processing, storage and notification are separate responsibilities. Passing collaborators into a service avoids inheriting unrelated behaviour and lets tests replace each external dependency.'),
 ('What does default_factory solve?','It creates a fresh default value for each instance. A shared mutable default would let one task or account accidentally modify another instance\'s list.')],
 ('Where should an independent cart item list be created?',['In each instance, or with default_factory','As one shared class-level list','In a module-level global for all users','As a cached mutable default argument'],0,'Each cart needs its own list unless sharing is deliberately part of the design.'),
 ('python','from dataclasses import dataclass, field\n@dataclass\nclass Task:\n    title: str\n    tags: list[str] = field(default_factory=list)\na, b = Task("Learn"), Task("Build")\na.tags.append("python")\nprint(a.tags, b.tags)',"['python'] []"),skills=[8,9])
 lesson(c,'py-errors','Exceptions and context managers',r'''
## Handle the failure you understand
An exception interrupts ordinary control flow until a matching handler catches it. Catch specific exception types near the point where you can recover or add useful context. A broad `except: pass` hides programming errors and can make corrupt output look successful.

`try` contains the risky operation, `except` handles selected failures, `else` runs when the try block succeeds, and `finally` runs during cleanup whether success or failure occurred. Raise a meaningful domain error when a caller needs to react differently, and use `raise NewError(...) from original` to preserve the cause.

## Resource lifetime
A file, lock or database transaction has a beginning and an end. A context manager expresses that lifetime with a `with` block. Its exit logic runs even if the body raises. `with open(path, encoding="utf-8") as file:` closes the file reliably; manually scattering close calls across branches is fragile.

A custom context manager implements `__enter__` and `__exit__`, or uses `contextlib.contextmanager` with a yield. Returning true from `__exit__` suppresses the exception, which should be a deliberate choice, not a default.

For retries, separate transient failures from invalid input. Do not retry a validation error or an operation with unsafe duplicate side effects. In web applications, log internal context securely but return a stable public error contract without stack traces or secrets.
''','Read JSON from a file and report missing-file and invalid-JSON errors separately. Keep parsing in a function so a unit test can pass invalid text without creating a real file.',[
 ('Why is catching Exception everywhere harmful?','It makes unrelated failures look recoverable and can hide broken invariants. Catch a specific failure where you can recover, translate it at an application boundary, and let unexpected faults reach monitoring.'),
 ('Why use a context manager?','It gives a resource a visible lifetime and guarantees exit logic when the block ends, including through exceptions. This is useful for files, locks, transactions and client sessions.')],
 ('Which block is intended for cleanup on both success and failure?',['finally','else','elif','match'],0,'finally runs when control leaves the try statement, including during exception propagation.'),
 ('python','import json\ntry:\n    json.loads("not JSON")\nexcept json.JSONDecodeError:\n    print("Invalid JSON")\nfinally:\n    print("Cleanup complete")','Invalid JSON\nCleanup complete'),skills=[11,12])
 lesson(c,'py-lazy','Iterators, generators and decorators',r'''
## Separate a sequence from iteration
An iterable can provide an iterator. An iterator returns successive values through `next()` and raises `StopIteration` when exhausted. A list can produce fresh iterators; a generator object is normally consumed once. This matters when a pipeline is accidentally traversed a second time.

A function containing `yield` creates a generator. Its local state is suspended between yielded values. That lets you process a large file one record at a time rather than loading the entire file. Laziness saves memory only when later stages also avoid collecting everything into a list.

## Decorators wrap behaviour
A decorator receives a function and returns a replacement callable. `@log_call` above a function is equivalent to rebinding it as `function = log_call(function)`. A wrapper can time execution, apply a cache or enforce a policy, but the caller's contract should remain clear.

Use `functools.wraps` to preserve useful metadata. Handle arbitrary positional and keyword arguments if the wrapper promises to be general. Decorator order matters because each wrapper receives the result of the previous wrapping step. Framework route and fixture decorators are ordinary applications of this mechanism.

Avoid caching functions that depend on hidden mutable state, current permissions or side effects without a carefully chosen key and invalidation rule. A faster wrong answer is still wrong.
''','Write a generator that yields nonempty cleaned lines from text. Wrap a pure function with a decorator that counts calls, and verify that its return value is unchanged.',[
 ('Can a consumed generator be iterated again?','The same generator object continues from its current state and stays exhausted after completion. Call the generator function again to create a fresh iterator.'),
 ('What does a decorator actually change?','It replaces the function name with another callable, usually a wrapper that delegates to the original. That wrapper can add behaviour before or after the call while preserving its public contract.')],
 ('Which expression is lazy?',['(x*x for x in range(100))','[x*x for x in range(100)]','list(range(100))','sorted(range(100))'],0,'A generator expression produces values on demand.'),
 ('python','def squares(n):\n    for i in range(n):\n        yield i*i\ng = squares(3)\nprint(next(g))\nprint(list(g))\nprint(list(g))','0\n[1, 4]\n[]'),skills=[13,14])
 lesson(c,'py-async','Async work, HTTP clients and concurrency',r'''
## Choose concurrency for the workload
Concurrency overlaps progress; parallelism executes work simultaneously. Asyncio is useful when tasks spend time waiting for network or other awaitable I/O. CPU-heavy Python code does not become faster merely because its function is declared async. Use an appropriate process pool or native library for CPU-heavy work; threads can help with blocking I/O.

In a conventional GIL-enabled CPython build, the global interpreter lock limits simultaneous Python bytecode execution by threads. Free-threaded builds change that assumption, so state the interpreter/build when discussing it. Either way, shared mutable state still needs a concurrency design.

## Async step by step
1. Define an `async def` function that awaits nonblocking operations.
2. Start independent tasks with `asyncio.gather` or a task group.
3. Bound concurrency with a semaphore; launching ten thousand external calls is not a free optimisation.
4. Apply deadlines, propagate cancellation and close clients using an async context manager.

HTTPX supports async HTTP requests. Requests is a common synchronous HTTP client. Set explicit connection/read timeouts, validate status and response shape, and retry only appropriate transient failures with backoff and jitter. Never run a blocking requests call directly inside an async endpoint's event loop.

For a batch report, validate each result and keep a deterministic fallback. A temporary model-provider outage should become a visible partial result, not an unbounded retry storm.
''','Simulate three slow jobs with asyncio.sleep and gather them. Then limit concurrent jobs with a semaphore. Explain how you would add a timeout and handle one failed API call.',[
 ('Does async mean parallel CPU execution?','No. Async tasks cooperate around await points, usually to overlap I/O waits. CPU-bound code that does not yield blocks that event loop; use a suitable worker strategy for it.'),
 ('Why reuse an HTTP client?','A client can pool connections and share configuration such as timeouts and headers. Reuse reduces repeated connection setup, while a context manager gives the pool a clear shutdown point.')],
 ('What is the best reason to add a semaphore to API calls?',['Bound concurrent requests and resource use','Make CPU instructions execute on every core','Remove the need for timeouts','Guarantee every response is valid'],0,'Concurrency limits protect both your process and the downstream service.'),
 ('python','import asyncio\nasync def job(n):\n    await asyncio.sleep(0)\n    return n*n\nasync def main():\n    print(await asyncio.gather(job(2), job(3)))\n# This browser already runs an event loop: use top-level await.\n# In a normal .py script, replace this line with asyncio.run(main()).\nawait main()','[4, 9]'),skills=[15,17,20])
 lesson(c,'py-files','Files, formats, logging and CLIs',r'''
## Treat file data as an external boundary
Use pathlib for paths rather than manually joining separators. Choose an encoding, usually UTF-8, when reading or writing text. Text mode decodes characters; binary mode preserves bytes. Parse JSON and CSV with their standard modules. YAML needs an additional parser; use its safe-loading interface for untrusted input.

For a task tracker, read the old state, validate it, write the new content to a temporary file in the same directory, then replace the destination. This reduces partial-write corruption. Concurrent writers still need a lock or a stronger storage model. A successful write is not automatically a guarantee against sudden power loss; durability may require flushing and filesystem synchronisation.

## Make useful operational output
Logging records events with severity, time and context. DEBUG supports diagnosis, INFO records normal lifecycle events, WARNING marks an unusual condition and ERROR records a failed operation. Do not log passwords, tokens or entire private documents. A request or job identifier lets you connect related events.

## A command-line interface
argparse gives you named options, help text and type conversion. Parse arguments at the program entry point and pass explicit values into your logic. Environment variables are useful for deployment configuration, but defaults and validation still matter. Distinguish a missing secret from a non-secret default setting.

Automate a bounded task first: a file renamer with a dry-run preview, a JSON summary generator or a CSV cleaner. Print a useful result and choose a nonzero exit code when the operation fails.
''','Design a JSON task tracker with add/list/complete commands. Include a dry-run option for migrations and recover cleanly from an invalid state file without silently overwriting it.',[
 ('Why write a temporary file before replacement?','It keeps readers from seeing a half-written destination during a normal successful replacement. It does not by itself solve concurrent updates, backups or every crash-durability requirement.'),
 ('Why avoid print for server diagnostics?','A logging system can add severity, timestamps and structured context and route records to monitoring. print remains useful for CLI output that is deliberately part of the program\'s result.')],
 ('Which should never be written to ordinary logs?',['A full API secret','An operation name','A non-sensitive request ID','An error category'],0,'Logs are copied and retained widely; secrets belong in protected configuration.'),
 ('python','import csv, io, json\nrows = list(csv.DictReader(io.StringIO("name,score\\nAsha,80\\nRavi,90\\n")))\nprint(json.dumps({r["name"]: int(r["score"]) for r in rows}))','{"Asha": 80, "Ravi": 90}'),skills=[16,18,25])
 lesson(c,'py-validation','Validate data with clear boundary models',r'''
## Static types and runtime data are different
A JSON object can have missing fields, incorrect types or values outside the allowed range. Type hints describe what your Python code expects; they do not prove that a network response satisfies it. Validate data once at the boundary, then pass a well-defined internal model to the rest of the application.

Pydantic models declare fields, defaults and constraints and produce structured validation errors. A response model can also restrict which fields leave your service. Treat coercion rules deliberately: an API accepting the text "12" as an integer may be convenient, while a finance or identifier contract may require strict types.

## A report input contract
Require a nonempty project ID, a list of tasks with enumerated statuses, nonnegative durations and a recognised report date. Reject impossible values with a message tied to the relevant field. Separate syntactic validation (the field is a date) from business validation (the caller can access that project).

Keep settings validation separate from request validation. Read environment configuration at startup so missing required configuration fails clearly, rather than halfway through a user's request. Avoid including secret values in formatted validation errors or logs.

The example below uses only the standard library so it runs offline here. A project using Pydantic would express the same input contract in a model. Install that third-party package in the project's own environment; it is not bundled into the browser Python engine.
''','Specify a ProjectSummary input model with project_id, completed_tasks and total_tasks. Reject completed counts larger than total, and return field-specific error information.',[
 ('Where should runtime validation happen?','At trust boundaries such as HTTP bodies, environment settings, file imports and model responses. Validate before business logic relies on the data; avoid scattering inconsistent checks throughout every function.'),
 ('Does schema validation enforce tenant permissions?','No. A well-formed project ID can still belong to another tenant. Authorisation must verify the authenticated user\'s relationship to the requested object.')],
 ('A request passes schema validation. What still needs checking?',['Whether the caller can access the requested object','Whether JSON uses braces','Whether strings exist in Python','Whether the editor has syntax colours'],0,'Data shape and access rights are separate concerns.'),
 ('python','def validate_report(data):\n    if not isinstance(data.get("project_id"), str) or not data["project_id"].strip():\n        raise ValueError("project_id is required")\n    done, total = data["done"], data["total"]\n    if type(done) is not int or type(total) is not int or not 0 <= done <= total:\n        raise ValueError("expected 0 <= done <= total")\n    return data\nprint(validate_report({"project_id":"p1", "done":2, "total":3}))',"{'project_id': 'p1', 'done': 2, 'total': 3}"),skills=[19])
 lesson(c,'py-tests','Test behaviour with pytest and small fakes',r'''
## What a useful test proves
A test chooses inputs, performs an operation and asserts an observable result. Start with a normal case, a boundary and a failure case. For a payment calculation, test zero items, a rounding boundary and invalid quantities, rather than only repeating the implementation's arithmetic inside the assertion.

pytest discovers test functions and uses ordinary assert statements. Parametrisation runs the same behaviour contract across explicit input/expected-output pairs. Fixtures provide setup and cleanup, such as a temporary directory or a reusable repository. A fixture should have a clear scope and avoid sharing mutable data accidentally across tests.

## Isolate external work
Replace an HTTP client with a fake that returns a known response or raises a timeout. Assert the feature's fallback, retry limit or returned error. Do not make a unit test depend on a live model provider, current network conditions or a real payment.

Use integration tests for real boundaries such as database transactions, migrations and HTTP routing. A small end-to-end suite checks critical user journeys across components. Coverage counts executed code, not correctness: one assertion can still miss an important business invariant.

For async tests, use a compatible async test setup and test cancellation/timeouts explicitly. Keep tests deterministic by controlling randomness, clocks and external responses. When a bug is found, preserve a minimal case that would fail before the fix.
''','Write explicit tests for your average function, including empty input and a negative value. Add a fake report provider that times out and assert the deterministic fallback text.',[
 ('What should be mocked in a unit test?','Usually external boundaries such as network calls, email, clocks or nondeterministic providers. Avoid mocking every internal function, because that can make tests describe an implementation instead of its behaviour.'),
 ('Why can 100% line coverage still miss a bug?','It proves the lines were executed, not that meaningful cases and assertions were chosen. Different inputs, concurrency interleavings and business invariants may remain untested.')],
 ('Which test is most deterministic?',['A fake provider returning a fixed timeout','A call to a live paid API','A test depending on today\'s exchange rate','A test waiting for a random email'],0,'A controlled fake removes network, billing and external-state variability.'),
 ('python','def average(values):\n    if not values:\n        raise ValueError("empty input")\n    return sum(values) / len(values)\nassert average([2, 4]) == 3\ntry:\n    average([])\nexcept ValueError:\n    print("Both explicit cases passed")','Both explicit cases passed'),skills=[23])
