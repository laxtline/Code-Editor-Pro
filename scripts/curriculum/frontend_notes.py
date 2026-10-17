from .common import course,lesson

def build():
 c=course('react','React','Frontend engineering','Build component-based interfaces with explicit state, accessible forms and tested data flows.','4-6 weeks after JavaScript','Build a notes dashboard with search, routing, validation, loading/error states and three end-to-end tests.',['react','mdn'])
 lesson(c,'react-components','JSX, props, composition and list keys',r'''
## A component describes UI from inputs
A React component is a function that returns a description of an interface. JSX is syntax transformed by a build tool; the browser does not interpret raw JSX as ordinary JavaScript. Begin in a configured React project, such as one created with a compatible Vite setup.

Props are inputs passed by a parent. Treat them as read-only and derive output from them. Compose a page from small components with clear responsibilities: a TaskCard displays one task, a TaskList maps tasks and a dashboard owns relevant state. children allows a component to wrap content without knowing every detail of that content.

## Render lists with stable identity
Use a stable data ID as a key among siblings. A key helps React match an item across renders; it is not automatically passed as a normal prop. Array indices become unsafe when items can be inserted, deleted or reordered because identity can move to a different item.

Render conditional UI deliberately. A loading state, an empty list and a failed request are different states. Avoid mixing an accidental numeric zero into JSX through a loose `count && ...` expression.

Composition normally scales better than a component with dozens of flags. Extract a component for meaningful repeated structure or behaviour, while keeping simple local markup readable. Do not copy props into state unless there is a specific lifecycle reason and a clear update policy.
''','Build NoteCard and NoteList components. Insert a new note at the start and verify that each note keeps its own editing state through a stable key.',[
 ('Why are stable keys important?','They let React preserve the intended identity of sibling elements across insertions and reordering. An index key can make state follow a position rather than the actual data item.'),
 ('What is composition in React?','Combining focused components through props and children instead of inheriting large component classes or adding unrelated flags. It keeps responsibilities and reusable structure explicit.')],
 ('Which is the best list key when notes can be reordered?',['note.id','The current array index','Math.random() on every render','The note card colour'],0,'A stable unique data ID preserves the intended item identity.'),
 ('jsx','function NoteCard({ note, children }) {\n  return <article><h2>{note.title}</h2><p>{note.body}</p>{children}</article>;\n}\nfunction NoteList({ notes }) {\n  return <section>{notes.map(note => <NoteCard key={note.id} note={note} />)}</section>;\n}','In a React project, each note renders with stable sibling identity.'),skills=[47,50])
 lesson(c,'react-state','State, events, reducers and context',r'''
## State is a snapshot for a render
useState stores a value across renders. Calling its setter schedules a new render; it does not mutate the variable already captured by the current render. When the next value depends on the previous one, a functional update such as `setCount(c => c + 1)` avoids relying on a stale captured value.

Update objects and arrays immutably at the level being changed. Copy the relevant container and replace the changed item. A spread is shallow, so nested objects need their own deliberate update. Derive a filtered list or total from existing state instead of maintaining duplicate state that can disagree.

## Put state where it belongs
Keep state local until another component genuinely needs to coordinate with it. Lift shared state to the nearest useful owner. Context distributes a value to a subtree; it does not automatically optimise every consumer. Split unrelated concerns if changes cause excessive rerenders.

useReducer expresses related transitions through actions, which can make a complex form or workflow easier to test. Redux Toolkit is useful when shared client state needs consistent reducers, tooling and explicit transitions; it is not required for every small page. Server data caching has a different lifecycle from local UI state.

Event handlers should perform the user's action and update state predictably. Avoid an effect that simply copies one derivable state value into another; it creates extra renders and synchronisation bugs.
''','Build a task filter with local search state and derived visible tasks. Then model a three-step form with reducer actions and explain which state, if any, needs context.',[
 ('Why use a functional state update?','It computes the next state from the current queued state, which is useful when multiple updates or callbacks depend on a previous value rather than the render\'s captured snapshot.'),
 ('When should state become global?','When a meaningful set of distant consumers needs coordinated ownership. Start with local state and lift it deliberately; global state adds coupling and should not become a default dumping ground.')],
 ('Which is best for a filtered list?',['Derive it from tasks and filter state','Store independent copies for every filter','Mutate the original list during render','Refetch all tasks on every keystroke without cancellation'],0,'Derived output avoids several state copies drifting apart.'),
 ('jsx','import { useState } from "react";\nexport function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>;\n}','Each activation increments the component state and rerenders the label.'),skills=[61])
 lesson(c,'react-effects','Effects, refs, custom hooks and cleanup',r'''
## Effects synchronise with external systems
An effect is appropriate for a subscription, timer, external widget or other system outside React's render calculation. It is usually unnecessary for deriving a value from props/state or handling a specific button action. Keep render logic pure so React can call it safely.

Dependencies describe reactive values used by the effect. Omitting a dependency can retain a stale closure; adding unrelated unstable objects can rerun the effect repeatedly. Fix the design rather than suppressing the linter without understanding the relationship.

## Cleanup is part of the contract
Return cleanup that disconnects the subscription, clears the timer or cancels/invalidates pending work. Development checks can intentionally run an extra setup/cleanup cycle; code should behave correctly through it rather than assuming setup occurs only once.

useRef keeps a mutable value without causing a render and can reference a DOM node. A ref is not a replacement for state when the displayed UI must update. Custom hooks extract reusable stateful logic with the same hook rules; call hooks consistently at the top level of a component or another hook.

Memoisation can reduce repeated calculations or stabilise identities where it matters, but it is not a correctness tool. Measure the expensive path first. A stale value caused by incorrect dependencies remains wrong even when useMemo makes it fast.
''','Create a custom hook that subscribes to the browser online/offline events and cleans up both listeners. Test mounting, unmounting and remounting without duplicate notifications.',[
 ('When is useEffect unnecessary?','When the value can be calculated from current props/state or when the work belongs directly to a user action handler. Effects are for synchronising with external systems, not every update.'),
 ('Why does an effect need cleanup?','The component can rerun its effect or unmount. Without cleanup, old listeners, requests or timers remain active and can duplicate work or update stale state.')],
 ('Which value should normally be state rather than a ref?',['A counter displayed in the UI','An interval handle used only for cleanup','A DOM element reference','A mutable diagnostic flag not rendered'],0,'Displayed reactive data needs a render update when it changes.'),
 ('jsx','import { useEffect, useState } from "react";\nfunction useOnline() {\n  const [online, setOnline] = useState(navigator.onLine);\n  useEffect(() => {\n    const update = () => setOnline(navigator.onLine);\n    addEventListener("online", update); addEventListener("offline", update);\n    return () => { removeEventListener("online", update); removeEventListener("offline", update); };\n  }, []);\n  return online;\n}','A reusable hook tracks connection hints without leaving duplicate listeners.'),skills=[48,49])
 lesson(c,'react-data','Server state, queries and optimistic updates',r'''
## Remote data has its own lifecycle
An API result can be loading, stale, fresh, failed or invalidated. A query library such as TanStack Query or SWR manages caching, deduplication and refetching around a query key. A query key must include the meaningful inputs, such as tenant ID, filters and page cursor, without exposing private secrets.

Choose freshness rules deliberately. Refetching on focus can be useful for a dashboard but does not replace an access-control check on the server. A mutation should invalidate or update relevant cached data after success. Do not maintain a second unsynchronised copy of the same server list in global client state.

## Optimistic does not mean guaranteed
An optimistic update shows an expected result before the server confirms it. Keep enough previous state to roll back and handle a conflicting server response. For a payment or stock decision, the server remains authoritative; a frontend animation cannot prove success.

## Merge realtime events carefully
Socket.io can deliver updates to a connected client, but reconnects and duplicates require a policy. Include stable event/object IDs, apply idempotent updates, and reconcile with a fresh snapshot after a gap. Do not simply append every received event forever.

Axios is an HTTP client convenience; it does not replace data ownership or cache design. Whether using it or fetch, centralise base URL/error handling and apply request cancellation when the user moves to a different resource.
''','Design query keys for tasks filtered by tenant, status and page. Describe an optimistic rename, including the rollback and how a later realtime event is merged.',[
 ('How is server state different from UI state?','Server state is owned remotely and can change independently; it needs freshness, invalidation and request coordination. A local open-dialog flag has a different ownership and lifecycle.'),
 ('Why refetch after a socket reconnect?','Events may have been missed while disconnected. A snapshot or replay protocol reestablishes a known state; assuming that every past event arrived can leave a silently incomplete cache.')],
 ('What must a task-list query key include when results vary by tenant?',['The tenant identity and relevant filters','Only the component colour','Only a constant word tasks','A private API secret'],0,'The cache identity must distinguish different result sets without exposing secrets.'),skills=[62,64])
 lesson(c,'react-forms','Forms, validation, error boundaries and loading UI',r'''
## Treat a form as a workflow
Controlled inputs render from state and update it through events. An uncontrolled input keeps its current value in the DOM and can be read through form APIs or refs. Either approach needs labels, constraints, helpful errors and a clear submit state.

For larger forms, React Hook Form can manage field registration and validation with a schema such as Zod. Keep server errors separate from basic client validation. On failure, retain entered data and focus or link to a useful error summary. Prevent accidental duplicate submission, and still make the backend operation idempotent where required.

## Isolate different kinds of failure
An error boundary catches supported render-time descendant errors and shows a fallback region. It does not automatically catch every event-handler error or every asynchronous rejection. Handle those at their own boundaries. Place error boundaries where one failed panel should not destroy the entire dashboard.

Suspense coordinates loading for supported data/code sources. It is not a universal replacement for every loading boolean around an arbitrary effect fetch. Design loading, empty, error and retry states explicitly.

An optimistic UI should announce progress accessibly and provide a recovery path. Do not hide a failed save behind a permanent success toast or erase the draft just because a request started. A useful form acknowledges the server's final outcome.
''','Design a note editor that preserves its draft on a failed save. Specify client validation, server errors, duplicate-submit prevention and a panel-level render fallback.',[
 ('Does an error boundary catch every async error?','No. Its main role is supported errors in descendant rendering/lifecycles. Event handlers and arbitrary async work need explicit error handling in their own control flow.'),
 ('Why keep form data after a failed request?',"The user's work remains valuable even if the network or server fails. Preserve it, show the failure clearly and allow a deliberate retry rather than forcing the user to retype.")],
 ('What should a failed save do?',['Preserve the draft and offer a useful retry','Erase the form and claim success','Hide every error permanently','Trust that disabling a button prevents all server duplicates'],0,'A recoverable interface retains user work and reports the actual outcome.'),skills=[51,52])
 lesson(c,'react-design','Design systems, charts, drag-and-drop and localisation',r'''
## Reuse interaction contracts
A design system combines tokens, accessible primitives, component variants and documentation. Radix-style primitives or shadcn/ui can provide a starting point, but the application still owns labels, focus management, semantics and tested composition. Do not assume a copied component is automatically accessible in every configuration.

## Make dashboards answer a question
Choose a chart by the comparison: bars compare categories, lines show ordered trends and a table provides exact values. Recharts can render a React dashboard, but you must supply meaningful axes, units, legends and an accessible data alternative. Distinguish revenue from payment count and label the period/time zone.

Drag-and-drop, for example with dnd-kit, needs a non-drag alternative and keyboard support. When a Kanban task moves, update both the visible state and the server contract, handle failure and avoid allowing a client to bypass a permission or invalid status transition.

## Localisation is more than translation
Use Intl formatting for dates, numbers and currencies rather than concatenating a symbol onto an arbitrary number. Decide where time zones matter; a due date and an exact event timestamp have different meanings. Text length, plural forms and right-to-left layout can affect component design.

Keep visual variants focused: size, emphasis, state and density should have documented meanings. A shared component should not become a collection of unrelated exceptions to avoid creating a second component.
''','Design an invoice dashboard with a labelled revenue trend, an exact data table and an INR amount formatted with Intl. Specify a keyboard alternative for moving a task between columns.',[
 ('How would you make a chart usable without colour perception?','Use labels, distinguishable series styles and an exact data alternative. Colour can reinforce meaning, but it should not be the only channel carrying that meaning.'),
 ('What is needed for accessible drag-and-drop?','A keyboard/non-drag way to perform the same move, meaningful announcements and predictable focus. The server must still validate the action and permissions.')],
 ('Which is the best way to format a currency amount?',['Intl.NumberFormat with an explicit locale/currency','Always prepend a dollar sign','Round every number to an integer','Store the formatted text as the only numeric value'],0,'Locale-aware formatting separates numeric data from its presentation.'),
 ('javascript','const money = new Intl.NumberFormat("en-IN", {style:"currency", currency:"INR"});\nconsole.log(money.format(123456.5));','An INR amount using Indian digit grouping; the exact currency glyph/spacing can vary by locale data.'),skills=[65,66,69])
 lesson(c,'react-quality','Component tests, end-to-end tests and performance',r'''
## Test what the user can do
Testing Library encourages querying by accessible role/label and asserting observable behaviour. Test a form submission, validation error or keyboard action rather than a private state variable. A test that passes while the user cannot perform the action is not useful evidence.

Playwright checks a real browser journey across routing, persistence and rendering. Choose a few critical journeys: create a task, recover from a failed save, and resume a saved exam. Use deterministic test data and controlled network responses. Prefer locator conditions over arbitrary fixed sleeps.

## Performance starts with measurement
Inspect Core Web Vitals and the relevant interaction. Use bundle analysis to identify large optional dependencies, code splitting to defer them and appropriate image sizes to reduce transfer/decoding cost. Avoid rerender optimisation until you know which component or calculation is expensive.

Memoisation can help, but incorrect dependencies or unstable identities can remove the benefit. Rendering a very large list may need pagination or virtualisation rather than one useMemo. Record a baseline and retest the same path after changing it.

Run lint, types, component tests and selected browser tests in CI. A green suite does not prove complete correctness, so keep the tests focused on meaningful contracts and add a regression case when a real bug is found. Include loading, empty, failed and permission-denied states.
''','Write acceptance criteria for three notes-app journeys and identify which checks belong in component tests versus browser tests. Profile one slow interaction and propose a measurable fix.',[
 ('Why query a button by role/name in a UI test?','It follows the interface a user or assistive technology can identify. It also exposes missing accessible names and is usually less coupled to decorative DOM details than a long CSS selector.'),
 ('Why can useMemo fail to solve a slow page?','The bottleneck may be a large DOM, a network request or another component. Memoisation only avoids selected recalculations when dependencies remain stable; measure the actual expensive path first.')],
 ('Which browser assertion best describes user behaviour?',['A saved draft survives reload','An internal helper has a particular private name','A CSS class contains exactly seven characters','A timeout of three seconds elapsed'],0,'Persistence across reload is a real observable contract.'),skills=[53,67,68])

 c=course('next','Next.js','Frontend architecture','Choose where code runs, how data is cached and how each route fails or loads.','2-3 weeks after React','Build a small product catalog with server-rendered product pages, a client cart and explicit cache/revalidation behaviour.',['next','react'])
 lesson(c,'next-routing','App Router, layouts and route states',r'''
## Routes are an architecture
The App Router organises route segments and their UI boundaries. A page represents a route's content, a layout provides shared structure, and nested segments express hierarchy. Route groups can organise files without becoming a visible URL segment. Dynamic segments represent data-dependent paths.

Define loading, not-found and error states at useful boundaries. A product page should distinguish a missing product from a provider outage; an error page should offer a meaningful recovery action. A shared layout should not depend on a fragile assumption that every child route loads successfully.

## Server and client components
Server Components can access server-side resources and keep server-only dependencies out of the client bundle. Client Components enable browser interaction, state and relevant hooks. A client boundary does not mean every byte renders only in the browser; understand the framework's rendering/hydration model instead of equating the label with a complete deployment strategy.

Values crossing the server/client boundary must satisfy supported serialisation rules. Never pass private keys or unrestricted database objects into client props. Keep the interactive boundary as small as practical so a static product description does not require a large client bundle.

Framework conventions evolve. The exact file/API names for request interception and runtime behaviour should be checked against the installed major version; the invariant is to make routing, trust boundaries and fallback UI explicit.
''','Sketch a catalog route tree with a shared layout, product detail page, loading state, not-found state and a small interactive Add to cart component. Mark which code needs browser APIs.',[
 ('Why keep a client boundary small?','Only the parts that need browser interaction should bring their client-side dependencies and state. Keeping static/data-access work server-side can reduce shipped JavaScript and avoid exposing server-only details.'),
 ('What should not cross into client props?','Secrets, privileged credentials and unrestricted internal records. Select a public, serialisable view model and enforce access before constructing it.')],
 ('Which usually requires a client component boundary?',['A button using local React state','Reading a private database password into a server-only function','A static heading with no interaction','A server-side access check'],0,'Interactive state and browser-specific behaviour belong on the client side of an appropriate boundary.'),skills=[54,55,60])
 lesson(c,'next-rendering','SSR, SSG, ISR and data caching',r'''
## Choose by freshness and audience
Static generation prepares content ahead of requests. Server rendering produces content for a request. Incremental regeneration/revalidation can refresh cached generated content. Client rendering fetches/updates data in the browser. One application can use several strategies for different routes.

A public product description can benefit from pre-rendering and controlled revalidation; a private account dashboard needs request-appropriate access and freshness. Do not cache tenant-specific content under a public shared key. Avoid assuming that a framework version's default fetch caching matches another version's defaults.

## Design invalidation before mutation
Name what is cached, where it is cached, how long it is valid and what event invalidates it. A product edit might invalidate a product tag and a category listing. The browser, framework server, CDN and database cache can each have separate lifecycles.

## Prevent stale and duplicate work
Fetch at the layer that owns the data contract. Avoid request waterfalls when independent requests can run together. Keep error/loading handling attached to the route or component that needs it. Measure which cache actually served a response before guessing why stale data appeared.

Use a before/after test: publish a product change, inspect the detail page and listing through the actual deployed cache path, and verify the documented freshness policy. A local development refresh is not proof of production invalidation correctness.
''','Choose rendering and caching policies for a public product page, search results and a private order history. For each, name its invalidation event and the data that must never be publicly cached.',[
 ('How is ISR different from rebuilding every page on every request?','It allows generated/cached content to be refreshed according to a revalidation policy. The exact behaviour depends on the framework version and cache configuration, so define and test the intended freshness contract.'),
 ('What is the main danger of caching a private dashboard by URL alone?','Different users or tenants may share that URL but have different permitted data. An insufficient cache key or an inappropriate shared cache can expose one user\'s information to another.')],
 ('What must a cache policy specify?',['Key, scope, freshness and invalidation','Only the colour of a loading spinner','Only the repository owner','A claim that all data is permanent'],0,'A useful policy identifies what is cached, for whom and how it becomes fresh again.'),skills=[56,57])
 lesson(c,'next-mutations','Server actions, route handlers and streaming',r'''
## Every mutation is a trust boundary
A server action or route handler executes on the server, but client-provided arguments remain untrusted. Authenticate the caller, authorise the exact object, validate input and enforce business rules. Hiding a button in the interface does not enforce those rules.

Use a route handler/API when non-browser clients, webhooks or a stable HTTP contract need it. A server action can simplify a tightly coupled UI mutation. Both need a consistent error strategy, duplicate-request handling and a post-success cache update/invalidation policy.

## Stream useful parts early
Streaming lets a response deliver ready content before slower regions finish. Suspense boundaries can isolate delayed regions in supported rendering flows. Design a meaningful skeleton or partial state; do not show a success message before the operation is committed.

For AI token streaming, account for connection closure, buffering proxies and cancellation. The browser should distinguish a partial answer from a completed answer and preserve the useful partial text if the connection fails.

Keep long-running jobs outside a short request when the runtime's limits make completion unreliable. Return a job identifier, persist status and let the interface observe progress. Choose runtime capabilities deliberately; a restricted edge environment may not support every Node package or database driver.
''','Design a product edit action that checks tenant ownership and validates price. Specify cache invalidation, duplicate submission behaviour and the UI shown if a later report-generation job fails.',[
 ('Are server-action arguments trusted because the function runs on the server?','No. They come from a caller and must be validated and authorised like any other request. Server execution location does not prove caller permission.'),
 ('When is a separate HTTP route useful?','When webhooks, mobile apps or other clients need a stable endpoint, or when an explicit HTTP resource contract makes the boundary clearer than a UI-specific action.')],
 ('What should happen before updating an object?',['Authenticate, authorise and validate on the server','Only hide the Edit button','Trust a role sent in a hidden field','Mark the UI successful before receiving any result'],0,'Server-side enforcement is required regardless of the frontend workflow.'),skills=[58,59])
 lesson(c,'next-url-state','URL state, navigation and shareable filters',r'''
## Some state belongs in the address
Search terms, sort order, page/cursor and selected categories often belong in URL parameters so a view can be refreshed, bookmarked and shared. A temporary open tooltip normally does not. Private drafts and secrets should not be put into the URL because URLs appear in history, logs and shared links.

## Back and forward must mean something
Push a history entry for a meaningful navigation change; replace one for a correction that should not add another step. Preserve enough state to render the route from its URL rather than depending on a previous page's in-memory object. Validate parameters and provide defaults for unknown values.

When a filter changes, reset or reconcile pagination so a cursor from an unrelated result set is not reused. For search-as-you-type, debounce network work and cancel stale requests. Debouncing a remote request does not require delaying a local draft save.

## Preserve user work
Before leaving an editor, save its current draft and show a clear restore path. For an assessment, save answers and keep the original deadline; navigating away should not secretly grant more time. A submitted section should remain locked when returning through history.

Test direct deep links, reload, browser Back, browser Forward and opening a new tab. A route that works only after a sequence of clicks is an incomplete navigation contract.
''','Design a catalog URL with category, sort and search parameters. Define when to push versus replace history, then test a direct link and Back/Forward after changing filters.',[
 ('Why keep filters in the URL?','It makes the view reproducible through refresh, sharing and browser history. The renderer can reconstruct the relevant query instead of relying on a previous screen\'s memory.'),
 ('What must stay out of query parameters?','Private credentials and sensitive drafts. URLs can be copied, logged and stored in history, so they are not an appropriate secret store.')],
 ('Which state is usually suitable for a shareable URL?',['A public category filter','A password reset secret copied into unrelated links','An unsaved private invoice note','A private server API key'],0,'A non-sensitive filter helps reconstruct a view without leaking private data.'),skills=[63])

 c=course('data-science','Data Science Basics','Python applied skills','Understand array shapes, clean tables and evaluate data before adding models.','2-3 weeks after Python','Clean a small sales CSV, produce a grouped summary and keep the transformation in a tested script.',['numpy','pandas','sklearn'])
 lesson(c,'data-numpy','NumPy arrays, shapes and vectorised operations',r'''
## Arrays describe shape and type
A NumPy ndarray stores a regular collection with a shape and dtype. A vector has one dimension, a table commonly has two and a batch can add more. The number of axes is not the same as the number of elements. Shape mistakes are common in ML and embedding code.

Vectorised operations express work over arrays and can use efficient native implementations. They do not make an algorithm with an unnecessarily huge intermediate array memory-free. Inspect both time and allocation size.

## Broadcasting
Broadcasting aligns dimensions from the trailing side; compatible dimensions are equal or one of them is one. A per-column mean can therefore be subtracted from a table without writing a Python loop. Confirm which axis represents rows, features or batches before reducing with mean/sum.

Slicing can return a view sharing storage with the original. A mutation through a view may change the source; make an explicit copy when independent ownership is required. Dtype conversion also matters: integer arithmetic, floating precision and missing-value representation have different rules.

For embeddings, a common matrix is number-of-documents by embedding-dimensions. Validate dimensions, normalisation and finite numeric values before similarity calculations. The runnable example below demonstrates the arithmetic with standard Python because NumPy is not bundled into this browser's core Python runtime.
''','Represent three documents with two features each. Compute per-column means, subtract them and explain the expected array shapes. Then describe when a NumPy slice needs copy().',[
 ('Why inspect array shape before a model call?','It establishes which axis represents batch/items and which represents features. Incorrect shapes can fail immediately or, worse, broadcast into a plausible but meaningless computation.'),
 ('Does vectorisation always reduce memory?','No. It can speed computation while creating large temporary arrays. Estimate intermediate shapes and use chunking or a different algorithm when memory use becomes excessive.')],
 ('What does shape (100, 8) commonly represent for embeddings?',['100 items with 8 dimensions each','8 items with 100 dimensions by definition','A scalar value','A guarantee of 100% accuracy'],0,'The meaning is a contract, but rows-as-items and columns-as-dimensions is a common layout.'),
 ('python','rows = [[2, 4], [4, 8], [6, 12]]\nmeans = [sum(row[i] for row in rows)/len(rows) for i in range(2)]\ncentered = [[value-means[i] for i,value in enumerate(row)] for row in rows]\nprint(means)\nprint(centered)','[4.0, 8.0]\n[[-2.0, -4.0], [0.0, 0.0], [2.0, 4.0]]'),skills=[21])
 lesson(c,'data-pandas','DataFrames, cleaning, grouping and joins',r'''
## A table has a schema, not just rows
A DataFrame associates labelled columns and rows with typed values. Begin by inspecting column names, dtypes, missing values and row counts. Preserve a raw input copy or reproducible source so cleaning does not destroy the evidence needed to diagnose a mistake.

## A deliberate cleaning pipeline
Parse dates and numeric values explicitly, standardise category labels and decide how to handle missing values. Dropping every incomplete row may bias the dataset. Distinguish an unknown value from a real zero, and record the policy used.

Filtering selects rows; groupby splits rows by key and computes aggregates. A join/merge combines tables through keys and has the same cardinality risks as SQL joins. If one customer key matches several rows on both sides, the output can multiply. Check expected uniqueness and before/after row counts.

Separate data validation from presentation. Keep monetary values and timestamps in suitable internal forms, then format for the report. Test transformation functions on tiny explicit examples including duplicates, missing fields and unexpected categories.

Pandas is a third-party project dependency, not included in this app's core browser engine. The example uses standard-library records to show the grouping logic; apply the same contract in a DataFrame inside your local project environment.
''','Design a sales-cleaning pipeline that validates order IDs, parses amounts and groups revenue by category. Specify how refunds, missing categories and duplicate order rows should affect the report.',[
 ('Why can a merge unexpectedly increase row count?','The join key may not be unique on one or both sides. A many-to-many match produces combinations, so inspect cardinality and validate the intended key relationship.'),
 ('Should missing numeric values always become zero?','No. Missing can mean unknown, unrecorded or inapplicable. Replacing it with zero changes the meaning and can bias totals or averages; choose a documented policy.')],
 ('What should be checked before joining customer and order tables?',['Key meaning, uniqueness and expected cardinality','Only the font of the CSV','Only the current theme','Whether every missing value can be guessed'],0,'The join contract determines whether matches and row multiplication are correct.'),
 ('python','sales = [{"category":"books","amount":100}, {"category":"tools","amount":70}, {"category":"books","amount":50}]\ntotals = {}\nfor row in sales:\n    totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]\nprint(totals)',"{'books': 150, 'tools': 70}"),skills=[22])
 lesson(c,'data-notebooks','Notebooks, reproducibility and useful plots',r'''
## Explore without hiding execution order
A notebook combines code, results and explanation, which is useful for exploration. Its state can become misleading if cells are run out of order or depend on values created in a deleted cell. Restart the kernel and run all cells to verify that the notebook is reproducible from its visible contents.

Move reusable transformations into tested modules as the work stabilises. Keep a notebook as a readable investigation or report rather than the only place where production logic exists. Pin important dependencies and record input data versions, random seeds and assumptions.

## Choose a plot by the question
Use a bar chart for category comparison, a line for an ordered trend, a scatter plot for a relationship and a histogram for a distribution. Label units and population/time range. A truncated axis or an inappropriate aggregation can exaggerate an effect even when every plotted value is real.

Matplotlib provides a flexible plotting foundation; higher-level tools can simplify common charts. Include exact values or an accessible table when the chart alone is insufficient. Avoid using a beautiful chart to conceal missing data, a tiny sample or an unsuitable comparison.

For a job portfolio, show the question, cleaning decisions, results and limitations. A clear, reproducible small analysis is more defensible in an interview than a large notebook whose outputs cannot be regenerated.
''','Plan a notebook that analyses a week of study activity. Include the input schema, a restart-and-run-all check, one useful plot and two limitations of the data.',[
 ('What is hidden notebook state?','A result depends on the kernel\'s past execution rather than only the visible top-to-bottom code. Restarting and running all cells exposes missing steps and order dependencies.'),
 ('Why move stable logic into modules?','Modules make reusable functions easier to test, import and run outside the notebook. The notebook can then explain the analysis without becoming an unstructured production codebase.')],
 ('Which is a good reproducibility check?',['Restart the kernel and run all cells in order','Keep only screenshots of outputs','Delete the input data description','Rely on variables from yesterday\'s session'],0,'A clean run verifies that visible code and recorded inputs can recreate the results.'),skills=[26])
