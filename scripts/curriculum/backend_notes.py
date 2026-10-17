from .common import course,lesson

def build():
 c=course('node','Node.js & APIs','Backend engineering','Design resource APIs, secure their boundaries and make retries and failures predictable.','4-6 weeks','Build a tenant-scoped project API with login, validated requests, payment events and a background report job.',['node','express','owasp','payment'])
 lesson(c,'api-resources','Servers, REST resources and pagination',r'''
## A server owns a request boundary
Node runs JavaScript outside the browser. Express layers routing and middleware over HTTP handling. A route matches a method and path; route parameters identify resources, query parameters refine a request and a request body carries structured input. Validate all three.

## Design resources instead of random action names
For tasks, use a collection such as `/projects/:projectId/tasks` and a specific resource such as `/tasks/:taskId`. GET reads, POST commonly creates or requests a non-idempotent operation, PUT expresses replacement semantics, PATCH a partial update and DELETE removal. Choose status codes and error shapes consistently. Method semantics do not replace permission checks.

Filtering and sorting must have bounded, documented choices. Limit page size and include a deterministic tie-breaker. Offset pagination is simple but can become expensive and inconsistent as rows move. Cursor pagination continues after a stable ordering key, often a tuple of timestamp and unique ID; encode the required sort/filter context so a cursor is not reused for a different query.

## Make the contract reviewable
OpenAPI describes paths, schemas and responses and can generate clients. Document nullable fields, limits, auth requirements and error responses. Define a versioning policy for breaking changes. A published type is only one part of the contract; test actual serialisation and deployed compatibility.

Do not return an unbounded database collection. Even a small dataset grows, and a public endpoint must control memory, latency and response size.
''','Design list/create/read/update/delete endpoints for project tasks. Specify a maximum page size, sort order, cursor shape and three error responses.',[
 ('When is cursor pagination preferable to offset?','It is useful for large or changing ordered datasets, where continuing after a stable key avoids scanning a large offset and reduces some shifting-page anomalies. It still needs a deterministic ordering and clear consistency expectations.'),
 ('Does a REST-looking URL make an API secure?','No. Resource naming improves the contract, but the server must still authenticate, authorise the exact object, validate input and enforce quotas/business rules.')],
 ('What should a list endpoint always define?',['Bounded page size and deterministic order','An unlimited response by default','A private database password in the URL','A random order with no continuation contract'],0,'Bounds protect resources and a stable order makes pagination meaningful.'),
 ('node','app.get("/tasks", requireUser, async (req, res, next) => {\n  try {\n    const limit = Math.min(100, Math.max(1, Number(req.query.limit) || 20));\n    const rows = await taskService.list({tenantId:req.user.tenantId, limit});\n    res.json({items:rows});\n  } catch (error) { next(error); }\n});','Project snippet: the authenticated tenant is server-derived and the result size is bounded.'),skills=[70,73,74])
 lesson(c,'api-middleware','Middleware, validation and stable errors',r'''
## Middleware order is behaviour
An Express application passes a request through ordered middleware and matching routes. Typical layers attach a request ID, apply relevant body parsing and security limits, authenticate, validate, authorise and execute a handler. An error handler translates unexpected faults into a stable public response while logging safe diagnostic context.

Body parsing has limits and content-type expectations. A webhook requiring a raw-body signature must preserve the exact bytes at the correct route; parsing and reserialising JSON first can invalidate the signature. Middleware that is useful for one route is not automatically correct for every route.

## Give clients one error contract
Use a consistent structure with a machine-readable type/code, human-readable summary and suitable status. RFC 9457 problem details is one standard format. Field errors can identify invalid input, while a request ID links a public response to protected logs. Never return stack traces, database credentials or raw secret-bearing provider responses to users.

## Harden without confusing controls
Validate supported fields, constrain request sizes and rate-limit sensitive operations. Helmet-style headers, a deliberate CORS policy and route-level quotas address different risks. CORS controls browser response access; it does not authenticate every possible HTTP caller.

Async failures must reach the application's error boundary according to the installed Express version and handler style. Test a rejected database call and malformed JSON, not only the happy route.
''','Specify middleware order for a login endpoint and a payment webhook. Define one public error JSON shape and explain which diagnostic fields stay only in server logs.',[
 ('Why does middleware order matter?','Each layer observes or changes the request before later layers run. Parsing, authentication or signature verification in the wrong order can change semantics or remove the bytes required for a security check.'),
 ('Why not return a stack trace in an API error?','It can reveal internal paths, query details and implementation information. Return a stable public error and a request identifier while keeping sensitive diagnostic context in protected logs.')],
 ('What must a raw-body webhook verifier use?',['The original request bytes','Pretty-printed JSON created later','The frontend success message','Only the request path'],0,'Signatures depend on the exact bytes defined by the provider contract.'),skills=[71,75,76,78])
 lesson(c,'api-idempotency','Idempotency and retry-safe operations',r'''
## Retries are normal
A network timeout does not prove that an operation failed. The server may have committed the change while the response was lost. Retrying a payment or order creation blindly can therefore duplicate a side effect.

An idempotent operation has the same intended effect when repeated with the same relevant input. An idempotency key lets a server recognise a retried request. Scope the key to the authenticated actor/tenant and operation, store the request fingerprint and result, and define a retention policy. Reusing a key with different input should not silently create an unrelated operation.

## Make the key effective under concurrency
1. Enforce uniqueness at the database boundary.
2. Acquire/insert the key record and perform the business change in a suitable transaction or coordinated workflow.
3. Store the committed result so a retry can receive the same outcome.
4. Handle in-progress, failed and expired records explicitly.

A frontend disabled button reduces accidental clicks but does not solve retried HTTP requests, multiple tabs or duplicated provider events. Likewise, a process-local Set is not enough when several server instances handle the same key.

For external services, use their idempotency support where available and still track your own business operation. Exactly-once delivery is a strong claim; practical systems often combine at-least-once delivery with idempotent processing and reconciliation.
''','Design retry-safe invoice payment creation. Include key scope, request fingerprint, database uniqueness and behaviour when two identical requests arrive concurrently.',[
 ('Why can a timeout be ambiguous?','The request may have completed on the server even though the client did not receive its response. The client must not infer that no side effect occurred merely from a transport failure.'),
 ('Why is an in-memory idempotency map insufficient?','It disappears on restart and is not shared across server instances. A durable uniqueness/transaction mechanism is needed to coordinate the operation across concurrency and failures.')],
 ('What should happen when one idempotency key is reused with different input?',['Reject or explicitly handle the contract violation','Silently charge again','Ignore all authentication','Use the newest body without any record'],0,'The key identifies one operation; a different request fingerprint must not be treated as the same successful retry.'),skills=[72])
 lesson(c,'node-runtime','Event-loop work, streams and memory',r'''
## Fast I/O does not make CPU work free
Node can coordinate many I/O operations through its event-loop architecture. A large synchronous JSON transformation, compression step or loop can still block request progress. An async function that performs a CPU-heavy loop without yielding remains blocking work.

Use worker threads for appropriate CPU-heavy JavaScript tasks and job workers for operations that can complete outside the request. Bound concurrency instead of starting every task immediately. Keep cancellation, timeouts and shutdown part of the worker contract.

## Stream with backpressure
A stream processes data in chunks. A producer must respect the consumer's ability to accept more data; otherwise buffering grows until memory is exhausted. Use supported stream piping/pipeline patterns and propagate errors rather than manually appending every chunk into one huge string.

## Diagnose memory behaviour
Distinguish temporary allocations, retained objects and operating-system/container limits. A cache without eviction, an ever-growing event listener collection or a request reference stored globally can retain data. Heap snapshots and runtime metrics help locate the retaining path.

Set appropriate request/body limits and keep large uploads off the main process when object storage is more suitable. A larger heap can delay a failure but does not repair an unbounded data structure. Measure latency percentiles, active work and memory under a realistic load, including slow consumers.
''','Plan a CSV export for a large table without loading all rows into one array. Specify pagination/cursor use, streaming, backpressure, cancellation and an error path.',[
 ('Why can a Node API stall despite no slow database query?','Synchronous CPU work or heavy garbage collection can occupy the event loop. Profile the process and inspect long tasks instead of assuming every delay is a network problem.'),
 ('What is backpressure?','A mechanism that makes a producer respect downstream capacity. Without it, a fast source can buffer an unbounded amount while a slow consumer reads, exhausting memory.')],
 ('Which is a likely memory leak?',['An unbounded map retaining completed requests','A bounded temporary array that becomes unreachable','A correctly removed event listener','A closed stream with no remaining references'],0,'Retaining completed request objects indefinitely prevents their memory from being reclaimed.'),skills=[79])
 lesson(c,'api-tests','API tests, fakes, Postman and database evidence',r'''
## Test at the boundary that owns the risk
A unit test can exercise a service with a fake mail or model provider. An HTTP integration test verifies routing, parsing, authentication and serialised responses. A database integration test checks actual constraints, transactions and queries. An end-to-end test checks a small critical user journey across those parts.

Vitest and Jest are test runners with different project ecosystems/configurations. Choose the one used by the actual repository rather than claiming both are installed. A Postman collection can document and exercise requests, but a manual successful request is not a complete automated regression suite.

## Use explicit adversarial cases
Test missing authentication, another tenant's object ID, invalid body fields, duplicate idempotency keys, a provider timeout and a database failure. Assert both the public outcome and the relevant persisted invariant. A response of 200 is not enough if the database contains two payments.

An in-memory substitute is useful for fast tests, but it may differ from PostgreSQL/MongoDB in isolation, SQL syntax, constraints or indexes. Keep selected tests against the target engine for the contracts that depend on it. Reset fixtures without touching a real user's database.

Make time, randomness and external responses controlled. Run the meaningful suite in CI and preserve a small regression case for a bug after fixing it. Do not mirror every internal helper in a test that would pass with the same mistake on both sides.
''','Write five API acceptance cases for task creation, including tenant isolation and a failed notification. Identify which need a real database and which can use a fake provider.',[
 ('Why are in-memory database tests not sufficient for every guarantee?','A substitute can have different transaction, constraint and query semantics from the production engine. Use the target database to test engine-dependent invariants and keep fakes for appropriately isolated behaviour.'),
 ('What should a duplicate-payment test assert?','It should inspect the persisted business effect as well as the response: one logical payment/order transition, a durable idempotency record and a consistent retry result.')],
 ('Which test provides the best tenant-isolation evidence?',['A verified tenant A user is denied tenant B\'s object through the actual API/data path','A hidden button is absent in one screenshot','A private helper has a particular name','A request returns any JSON'],0,'The protected object boundary must be tested with an authenticated cross-tenant attempt.'),skills=[77])
 lesson(c,'api-auth','Authentication, sessions, OAuth and tenant RBAC',r'''
## Identity and permission are separate
Authentication establishes who the caller is. Authorisation establishes whether that caller may perform this operation on this object. A valid login token does not prove access to every project ID. Derive tenant identity from verified server-side context and include it in the data-access condition.

Passwords need an appropriate password-hashing scheme with a salt and configurable work factor; bcrypt is one established option with input/parameter considerations. Do not use a fast general hash as a password database design. Support rate limits and a safe reset flow.

## Sessions and tokens
A signed JWT is not automatically encrypted. Verify its signature, allowed algorithm, issuer/audience and expiry according to your system's contract. Plan refresh, revocation/logout and key rotation. Browser storage choices have trade-offs: HttpOnly cookies reduce JavaScript token exposure but require CSRF-aware session design; localStorage is readable by injected script.

OAuth 2.0 concerns delegated authorisation; OpenID Connect adds an identity layer. A browser/mobile authorisation-code flow commonly uses PKCE, along with state/nonce checks where applicable. Do not treat an arbitrary frontend email string as proof that a user signed in through Google.

## Object-level access
Check role permissions and tenant/object ownership at the service/query layer. A task update should select by both task ID and the caller's permitted tenant, then enforce allowed status changes. Test one tenant trying another tenant's IDs, including nested resources, downloads and search endpoints.
''','Design an admin/member/client permission matrix for a project portal. Write the access condition for reading one invoice and specify how logout affects an already issued session/token.',[
 ('Why is hiding an admin button insufficient?','A user can call the endpoint directly. The server must verify the authenticated identity, role and relationship to the requested object on every protected operation.'),
 ('Are JWT payloads secret?','Ordinary signed JWT payloads are encoded, not encrypted. Do not place secrets in them; verify signatures and claims, and use a deliberate session, expiry and revocation strategy.')],
 ('Which tenant ID should a protected query trust?',['One derived from verified server-side identity','Any tenant ID from the request body','A CSS class in the browser','The first tenant in the database'],0,'Caller-controlled identifiers cannot establish access rights.'),skills=[86,87,88])
 lesson(c,'api-payments','Payment webhooks, signatures and replay protection',r'''
## The browser is not the payment authority
A checkout success callback improves the interface but is not proof that money settled. The backend creates the provider order using a server-authoritative amount and links it to your own pending business operation. Never accept a final price or paid flag just because the client supplied it.

## Verify the event boundary
Read the provider's current signature contract. For a typical HMAC webhook, compute the digest from the exact raw request body and the configured webhook secret, then compare using a timing-safe method. Check identifiers and expected business context, and keep the secret out of source code and ordinary logs.

## Process a duplicate safely
Providers retry deliveries. Store a unique event/delivery identifier and make the business transition idempotent. Verify the allowed state transition, update payment/order state transactionally and record a useful audit event. A valid signature proves origin/integrity under the shared-secret model, not that processing this same event twice is safe.

Outgoing webhooks need similar discipline: stable event IDs, a signed body, timestamps where appropriate, delivery logs, bounded retries and a way to inspect/retry failed deliveries. Receivers should understand the retry policy.

Keep invoices and payment records reconciliable. Partial refunds, cancelled orders and delayed events are separate states, not one boolean that every code path can overwrite.
''','Draw a pending-to-paid order flow using a verified webhook. Include signature failure, duplicate event, out-of-order event and a reconciliation job for a missing callback.',[
 ('Why verify a webhook signature on the server?','The endpoint is publicly reachable. Signature verification checks the event bytes against the configured provider secret so an arbitrary caller cannot simply claim a payment succeeded.'),
 ('Why is signature verification not enough?','A genuine event can be duplicated, delayed or irrelevant to the current business state. Idempotency, expected identifiers, allowed transitions and reconciliation are still required.')],
 ('Who should decide the final checkout amount?',['The backend using authoritative product/pricing data','The client-provided total alone','A hidden HTML field alone','A success toast'],0,'The client is an untrusted input source; pricing must be recomputed/verified on the server.'),skills=[89,92])
 lesson(c,'api-integrations','Email, uploads, PDF invoices and provider fallback',r'''
## An integration is a failure boundary
Email, media storage, SMS, AI and PDF services can time out, reject input or become unavailable. Define the success contract and decide which failures block the user action. A saved task should not disappear because its notification email failed.

Nodemailer works with configured SMTP delivery; services such as SendGrid/Resend expose their own APIs. A password-reset link needs a short-lived, single-use server-validated token and a response that avoids unnecessary account disclosure. Delivery acceptance is not the same as the recipient reading the email.

## Uploads and generated documents
Use file size/type limits and server-authorised object names. Cloudinary or S3-compatible storage can hold media; a signed upload/download URL should have a scope and expiry. Do not trust a supplied filename or allow a user to select another tenant's object path.

PDFKit can create a PDF programmatically; browser-based rendering tools can turn controlled HTML into a document. Escape untrusted fields and restrict external resource access. An invoice should snapshot the legally/business-relevant values at issuance rather than silently changing when a current product title or price changes.

## A graceful fallback
If an AI summary provider fails, return a clearly labelled deterministic summary from validated task counts. Preserve the non-AI workflow. Record the provider error safely and retry according to a bounded policy rather than locking the entire portal behind one optional integration.
''','Design a weekly project report that saves independently of email delivery. Specify an invoice snapshot, upload ownership check and a deterministic fallback when the text-generation provider is down.',[
 ('Why store an invoice/order snapshot?','The issued document must preserve the relevant price, tax, address and item details from that transaction. Reading only current product data later can rewrite the apparent historical transaction.'),
 ('What is a useful graceful fallback?','A feature remains usable with a clear deterministic result when an optional provider fails. For example, a report can show verified task counts instead of inventing an AI narrative or returning fake success.')],
 ('What should happen if a notification email fails after a task is saved?',['Retain the task and retry/report notification separately','Delete the task silently','Claim the email was read','Retry forever inside the original request'],0,'The core transaction and optional delivery have different lifecycles and failure policies.'),skills=[90,91])
 lesson(c,'api-jobs','Queues, schedules and state machines',r'''
## Long work needs a durable lifecycle
An HTTP request can enqueue a report job and return an identifier. A worker processes it, stores a result and updates status. BullMQ and Celery are examples of queue tools in different ecosystems. Queue choice does not eliminate duplicate delivery or partial failures.

Define queued, running, succeeded, failed and cancelled states with allowed transitions. Include retry count, last error category and a visibility/lease strategy appropriate to the queue. A dead-letter queue or failed-job store makes persistent failures inspectable rather than silently dropping them.

## Make recurring work safe
A scheduler such as cron identifies when work should begin; it does not prove that one instance ran exactly once. Several application replicas may trigger the same schedule, a machine can be down at the expected time and a retry can overlap. Use a unique logical period/job key, a durable ownership mechanism and a catch-up policy.

## Model business transitions explicitly
For an order, allowed transitions might include pending to paid and paid to shipped, with separate cancellation/refund paths. Centralise the rule rather than letting every route assign an arbitrary status string. Apply transitions with the relevant data change transactionally where possible.

Monitor queue depth, age and failure rate. A worker that never crashes but falls hours behind is still failing the product's timeliness contract. Bound provider retries and apply backoff/jitter instead of amplifying an outage.
''','Define the report job state machine and retry policy. Then prevent two weekly schedulers from producing two reports for the same tenant and calendar week.',[
 ('Why do workers need idempotency?','A job can be delivered again after a crash, lost acknowledgement or retry. The handler must recognise the business operation and avoid duplicating durable side effects.'),
 ('Why use an explicit state machine?','It makes valid transitions and their preconditions reviewable. It prevents unrelated routes from assigning impossible states such as shipping an unpaid/cancelled order.')],
 ('What best prevents duplicate weekly reports across replicas?',['A durable unique tenant-and-period job key','A global variable in one process','Only disabling a frontend button','Assuming cron never repeats'],0,'The logical job identity must be coordinated durably across processes.'),skills=[93,94,97])
 lesson(c,'api-realtime','WebSockets, Socket.io rooms and SSE',r'''
## Pick the direction of communication
WebSockets provide a persistent bidirectional channel. Socket.io adds its own connection/reconnection protocol and features; it is not interchangeable with a raw WebSocket client in every case. Server-Sent Events send a server-to-browser stream over HTTP and are useful for notifications or token output when client messages can use ordinary requests.

## Authenticate the connection and each action
A socket room is a routing mechanism, not a permission boundary. Derive permitted rooms from the verified identity and enforce tenant membership. Validate incoming event payloads and recheck permissions for sensitive actions. Do not let an arbitrary client join a tenant room by naming its ID.

## Design recovery
Connections drop. Include event IDs/versioning where needed, handle duplicates, reconcile a snapshot after a gap and specify when the UI is stale. Use heartbeat/idle policies that work through the actual proxy/load balancer. Unbounded per-client queues can consume memory when a client reads slowly.

For SSE, send correctly framed events and handle reconnect/last-event identifiers according to your retention strategy. A streaming response should not buffer the entire result accidentally at a proxy. Cancellation must propagate when the client stops watching a costly generation.

Realtime is not durability. Persist important changes first and use the stream to notify clients about committed state. A missed notification must not mean the underlying payment or task update vanished.
''','Choose Socket.io or SSE for task collaboration and for one-way AI token output. Define room ownership, duplicate handling and how the UI recovers after a 30-second disconnect.',[
 ('Are Socket.io rooms an access-control system?','No. They organise delivery. The server must authenticate the connection, derive allowed room membership and enforce object/tenant permissions on actions.'),
 ('When is SSE a good fit?','When the server mainly pushes a stream to the browser, such as notifications or tokens, while client commands can use regular HTTP. Bidirectional low-latency collaboration may justify a WebSocket-based design.')],
 ('What should happen before broadcasting an important task update?',['Persist and authorise the actual change','Only update one client\'s local array','Trust any room name from the client','Discard the event if no one is connected'],0,'The durable business change must remain correct independently of notification delivery.'),skills=[95,96])

 c=course('python-backend','Python Web Backend','Backend engineering','Choose Flask, Django or FastAPI deliberately, then validate, authorise and persist requests.','3-5 weeks after Python','Build a task API with tested CRUD, typed input, a database migration and a safe deployment configuration.',['python','fastapi','owasp'])
 lesson(c,'py-web-choice','Flask, Django and FastAPI: choosing a framework',r'''
## Frameworks organise the HTTP boundary
Flask is a small framework that lets you choose many surrounding components. Django supplies a broader integrated stack including ORM, migrations, forms/admin and authentication facilities. FastAPI focuses on typed API declarations and validation/OpenAPI integration. Choose according to the product and team rather than a claim that one is universally best.

## The shared request lifecycle
A server receives a request, a router selects a handler, middleware/dependencies establish context, input is validated, a service performs the operation and the response is serialised. Configuration, logging, error handling and access checks are part of that lifecycle in every framework.

Start with a small task resource. Implement list/create/read/update/delete and explicit error cases. Keep application logic independent enough to test without an actual HTTP server, then add request-level integration tests.

## Project environment
Create a virtual environment, record dependencies and use environment-based configuration. A development server is not automatically the complete production deployment design. Configure the appropriate application server, reverse proxy, timeouts, static/media handling and shutdown behaviour.

Do not add authentication by inventing a token format or hashing scheme. Use maintained framework/security components and understand their session/CSRF/permission contracts. Browser examples in this study desk explain the flow; a real Python web project needs its framework packages installed locally.
''','Choose a framework for a small JSON API and for an admin-heavy content application. Give two concrete reasons for each choice and list the components you must still configure.',[
 ('Why might Django fit an admin-heavy application?','It provides an integrated ORM, migrations, admin and common web facilities. That can reduce assembly work, while still requiring deliberate configuration, permissions and deployment.'),
 ('Does choosing an async framework make every handler nonblocking?','No. Blocking database drivers, HTTP clients or CPU work can still block an event loop. The handler and its dependencies must use a compatible execution strategy.')],
 ('What is common to all three framework choices?',['Server-side validation and authorisation remain necessary','No database design is needed','Every external call is automatically safe','A development server is always enough for production'],0,'Framework conveniences do not remove the underlying trust and data boundaries.'))
 lesson(c,'fastapi-routing','FastAPI routes, validation and dependencies',r'''
## Declare a clear endpoint
A FastAPI handler can receive path, query and body values through an explicit declaration. Pydantic models express request/response shapes and constraints. Generated OpenAPI/Swagger documentation makes the declaration inspectable, but clients still need correct examples, error contracts and access requirements.

## Dependency injection
Depends can provide a database session, authenticated user or validated settings. A dependency has a lifecycle and can be overridden in tests. Keep the dependency graph understandable; hiding every business rule in nested dependencies makes errors hard to trace.

## Async boundaries
Use async endpoints with compatible nonblocking operations. A synchronous blocking call inside async code can still occupy the event loop. Choose the framework's supported sync execution path or an appropriate worker for blocking work, and close sessions/clients reliably.

## Response contracts
Return public fields through an explicit response model. Never rely on a caller to ignore a private password hash or internal tenant flag. Validate ownership before returning a resource, even if its identifier is a valid integer/UUID.

Test a valid request, missing/invalid fields, unauthorised access and a failed dependency. Override a provider or session in tests so the result does not depend on an external network or an uncontrolled production database.
''','Specify a create-task endpoint with a Pydantic body, authenticated-user dependency and response model. Add tests for invalid title, another tenant and a database exception.',[
 ('What does dependency injection improve?','It makes collaborators and lifecycles explicit and provides a controlled way to replace them in tests. It should clarify ownership rather than hide all business logic behind magic.'),
 ('Why use a response model?','It documents and restricts the public output shape. This helps prevent accidental exposure of internal fields and makes the serialised API contract testable.')],
 ('Which value should a protected FastAPI dependency supply?',['A verified authenticated user context','A trusted role copied directly from the request body','A private key sent back to the browser','An unvalidated global account ID'],0,'The handler needs identity established by server-side verification.'),
 ('python-project','from fastapi import FastAPI, Depends\nfrom pydantic import BaseModel, Field\napp = FastAPI()\nclass TaskInput(BaseModel):\n    title: str = Field(min_length=1, max_length=120)\n@app.post("/tasks")\ndef create_task(body: TaskInput, user=Depends(require_user)):\n    return task_service.create(user.tenant_id, body.title)\n# require_user and task_service are project collaborators to implement/test.','Project sketch: validate the input and derive tenant context from a verified dependency.'),skills=[80,81,82,83,85])
 lesson(c,'py-orm','SQLAlchemy sessions, transactions and Alembic',r'''
## An ORM is a data-access tool
SQLAlchemy maps Python operations and models to database work. It does not remove SQL concepts, transaction design or query-plan costs. A session coordinates unit-of-work/identity behaviour and must have a clear lifetime; sharing one mutable session across unrelated requests is not a safe default.

## Make the transaction visible
Group related changes in an explicit transaction. Commit after the business invariant is satisfied and roll back on failure. A session flush can send changes to the database without being the same as a final commit. External calls inside a long database transaction can hold locks and connections unnecessarily.

## Migrations are reviewed changes
Alembic records schema changes. Inspect generated migrations, test them against representative data and plan backfills. Renaming a field in Python does not automatically prove that a generated database drop/add is the intended safe migration.

Avoid N+1 queries when rendering related objects. Choose suitable eager-loading or explicit queries and measure query count and plans. Authorisation belongs in the data-access conditions as well as the route contract.

For a breaking schema change, use expand/contract: add compatible fields, deploy code that can handle both forms, backfill safely, switch readers and remove the old form later. A rollback plan includes the data consequences, not only reverting application source.
''','Design a create-project transaction that also creates its initial membership. Explain session lifetime, rollback on the second insert failing and how you would migrate a required field without a long outage.',[
 ('How are flush and commit different?','Flush sends pending changes through the database session so constraints and generated values can be observed. Commit completes the transaction; a flushed change can still be rolled back.'),
 ('Why inspect autogenerated migrations?','A tool infers structural differences but not the intended business migration, data preservation or deployment order. Review destructive operations, backfills and compatibility before applying them.')],
 ('What should happen if a required second insert fails?',['Roll back the related transaction','Keep half the business operation and claim success','Ignore the exception','Commit the first change without considering the invariant'],0,'The transaction should preserve the business invariant across related changes.'),skills=[84])

 c=course('databases','SQL & DBMS','Systems foundations','Query data, design schemas and understand transactions, indexes and operational trade-offs.','4-6 weeks','Model users, projects, invoices and payments, then test constraints, query plans and a stock update under concurrency.',['postgres','mongo','rag'])
 lesson(c,'sql-query','SELECT, filtering, joins and aggregates',r'''
## A query describes a result
A relational table has named columns and rows constrained by a schema. SELECT chooses output expressions, FROM/JOIN establish input relations, WHERE filters rows, GROUP BY forms groups, HAVING filters grouped results and ORDER BY controls presentation. Without ORDER BY, do not depend on a particular row order. LIMIT bounds output.

## Joins are relationships
INNER JOIN returns matching combinations; LEFT JOIN retains unmatched rows from the left with nulls on the right. RIGHT/FULL joins express other preservation choices where supported. A one-to-many join can multiply rows, so COUNT(*) after a join may not mean the number of distinct customers. State which entity you are counting.

## Aggregates and NULL
COUNT(*) counts rows, while COUNT(column) excludes null values of that expression. SUM/AVG operate on their supported non-null inputs; an empty result has aggregate-specific behaviour. Use COALESCE deliberately rather than silently treating every unknown value as zero. NULL comparisons require IS NULL/IS NOT NULL rather than = NULL.

Use parameterised queries for external values. String concatenation is not a safe query-construction strategy. INSERT, UPDATE and DELETE change data; review WHERE clauses and use transactions when several changes must remain consistent.

The example runs in this app's bundled SQLite engine. Database-specific syntax and features should be checked against the actual database used in your project.
''','Write queries for customers with no orders, total paid amount by customer and customers whose total exceeds a threshold. Explain the difference between filtering orders before grouping and filtering totals after grouping.',[
 ('How do WHERE and HAVING differ?','WHERE filters individual input rows before grouping. HAVING filters groups after aggregation, such as customers whose sum exceeds a threshold.'),
 ('Why can a LEFT JOIN act like an INNER JOIN accidentally?','A WHERE condition requiring a non-null right-side value can discard the unmatched null-extended rows. Put the predicate in the join or account for nulls according to the intended result.')],
 ('Which counts all result rows including rows with NULL fields?',['COUNT(*)','COUNT(nullable_column)','SUM(*)','WHERE NULL = NULL'],0,'COUNT(*) counts rows, while COUNT(expression) excludes null values of that expression.'),
 ('sql','CREATE TABLE study_sales(customer TEXT, amount INTEGER);\nINSERT INTO study_sales VALUES (\'Asha\',100),(\'Ravi\',70),(\'Asha\',50);\nSELECT customer, SUM(amount) AS total\nFROM study_sales\nGROUP BY customer\nHAVING SUM(amount) >= 100\nORDER BY total DESC;','One row: Asha, total 150.'),skills=[98])
 lesson(c,'sql-advanced','Subqueries, CTEs, windows and upserts',r'''
## Break a query into named steps
A subquery provides an intermediate relation/value. A common table expression names a query within a statement, often making a multistep transformation easier to review. A CTE is not a universal performance optimisation; planner behaviour and materialisation rules depend on the database/version.

## Window functions preserve rows
GROUP BY normally collapses rows into aggregates. A window function computes across a related window while retaining each row. Use PARTITION BY to separate groups and ORDER BY to define sequence. The window frame matters: a running total is different from the total of an entire partition.

ROW_NUMBER assigns an order-based sequence; RANK leaves gaps after ties; DENSE_RANK does not. Add deterministic tie-breakers when the result needs one stable row. For top-N per category, compute the window rank in a subquery/CTE and filter in an outer query.

## Recursive and write patterns
A recursive CTE can traverse a hierarchy, but it needs termination and cycle handling appropriate to the data. An upsert combines an insert with conflict handling under a unique constraint; choose which fields may update and preserve business rules.

Use EXPLAIN to inspect a complex query and compare it with explicit expected rows on a tiny dataset. A concise query can still be expensive or wrong when joins multiply rows before the window calculation.
''','Produce a running total of study minutes per person and the top two scores per topic. Explain tie handling and test with equal scores and an empty input table.',[
 ('How is a window function different from GROUP BY?','It calculates over related rows without necessarily collapsing them. That lets a result include each original row beside a rank, running total or partition aggregate.'),
 ('Why add a tie-breaker to ROW_NUMBER ordering?','If equal ordering values remain, the database may choose any order among them. A stable unique secondary key makes pagination or selecting one representative row deterministic.')],
 ('Which function is suited to retaining rows with a running total?',['SUM(...) OVER (...)','Only GROUP BY with no detail columns','DELETE FROM','DROP TABLE'],0,'A window aggregate can retain detail rows while calculating an ordered running sum.'),
 ('sql','CREATE TABLE study_scores(id INTEGER, person TEXT, points INTEGER);\nINSERT INTO study_scores VALUES (1,\'Asha\',10),(2,\'Asha\',20),(3,\'Ravi\',15);\nSELECT id, person, points,\n SUM(points) OVER (PARTITION BY person ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running\nFROM study_scores ORDER BY person,id;','Asha running totals 10 and 30; Ravi running total 15.'),skills=[99])
 lesson(c,'db-schema','Keys, ER diagrams and normalisation',r'''
## Model the relationships first
An entity is a kind of thing you store; a relationship describes how instances connect. Cardinality asks one-to-one, one-to-many or many-to-many; optionality asks whether a link is required. Draw these before creating tables. A membership table often models users belonging to projects or tenants with roles.

A primary key identifies a row. A foreign key enforces a relationship to a referenced key. Unique and check constraints enforce additional rules close to the data. Application checks improve error messages but cannot reliably replace database constraints under concurrent requests.

## Reduce update anomalies
First normal form is commonly taught through atomic values and a consistent relational structure. Second normal form removes partial dependencies on part of a candidate key; third normal form addresses inappropriate transitive dependencies. BCNF requires determinants of nontrivial functional dependencies to be superkeys. State the relevant dependencies before claiming a schema is normalised.

Duplicating a customer's current address across many editable rows can create inconsistencies. A historical order snapshot is a different requirement and can intentionally preserve a transaction-time address. Normalisation is not a rule to delete meaningful historical data.

Denormalise deliberately for a measured access pattern, with a clear source of truth and update/rebuild policy. A schema should encode tenant ownership and prevent invalid cross-tenant relationships where feasible, not only store a tenant label that queries forget to use.
''','Draw an ER model for clients, projects, tasks, invoices and payments. Mark cardinality, required links, primary/foreign keys and one unique business rule. Explain a deliberate invoice snapshot.',[
 ('Why enforce uniqueness in the database?','Two requests can both pass a prior application existence check. A database uniqueness constraint arbitrates concurrent attempts at the actual write boundary.'),
 ('When is duplicated data justified?','When it serves a defined requirement such as historical snapshots or a measured read model. Specify its source, consistency/rebuild policy and why normalised access is insufficient.')],
 ('What does a foreign key primarily enforce?',['A referenced relationship between rows','A frontend colour rule','A password hashing algorithm','A guarantee that every query is fast'],0,'Foreign keys enforce referential integrity; performance and permissions need separate design.'),skills=[100,101,102,104])
 lesson(c,'db-prisma','Prisma models, migrations and ORM boundaries',r'''
## Map an application contract onto a real database
Prisma expresses models and relations and generates a client for typed data access. It can improve developer feedback, but the database still owns constraints, transactions and query execution. Generated types do not remove runtime validation or authorisation.

## A migration workflow
Change the schema, generate a migration in development, inspect its SQL and test it against representative data. Apply reviewed migrations through the deployment process rather than making production schema changes manually and hoping source catches up.

For a required new field, design defaults/backfills and compatible deployment order. Renames and destructive changes need particular attention. A migration that succeeds on an empty database can fail or lock a large production table.

## Query intentionally
Select the fields needed for the public response and scope by verified tenant/object permissions. Inspect query counts when loading related records; an ORM can still generate N+1 behaviour or large joins. Use transactions for related changes and a supported safe raw-query mechanism when the ORM does not express the necessary operation clearly.

Do not concatenate untrusted input into a raw SQL string. Keep generated code and client versions compatible with the schema/deployment. Integration tests should verify serialised API behaviour and constraints using the target database, not only a mocked ORM method.
''','Model Project and Task with a relation and tenant ownership. Plan a migration adding an optional deadline, then a later validated requirement, without breaking the previous deployed client.',[
 ('Does an ORM prevent every SQL injection?','No. Unsafe raw queries or string-built fragments can still introduce injection. Use the ORM\'s safe parameterisation facilities and validate allowed structural choices.'),
 ('Why inspect generated migration SQL?','The tool sees structural differences but cannot know your safe deployment/backfill intent. Review data loss, lock duration, constraints and compatibility with running application versions.')],
 ('Which is the safest raw-query pattern?',['Parameterised values through the supported API','Concatenate a user search string into SQL','Trust every query fragment from the browser','Disable constraints during ordinary requests'],0,'Parameterisation separates data values from SQL structure.'),skills=[103])
 lesson(c,'db-indexes','Storage, indexes, plans, WAL and vacuum',r'''
## Rows live in pages, not magic
A storage engine groups data into pages and maintains structures to find and update it. An index is an additional access structure, often a B-tree for ordered equality/range access. It consumes storage and adds write maintenance; adding an index to every column is not a free optimisation.

## Composite indexes follow access patterns
Column order matters because the index has an ordering. Consider equality filters, ranges and the requested sort together. A covering/index-only strategy can reduce table access under the database's rules; partial indexes target a subset of rows. Use the target engine's planner behaviour rather than a universal slogan about every composite index.

EXPLAIN shows a proposed plan; EXPLAIN ANALYZE executes and measures it, so do not run it blindly on destructive statements. Compare estimated and actual rows and inspect where work multiplies. Nested-loop, hash and merge joins have different cost profiles depending on input size, ordering and available memory.

## Writes and maintenance
Write-ahead logging records information needed for crash recovery before relevant changes become durable. In PostgreSQL, MVCC leaves old row versions that vacuum can reclaim when safe. Stale statistics can mislead the planner; analyse/maintenance are part of operating the database.

Measure a representative query before and after one index change. Record read benefit, write cost and data distribution. A plan from a tiny empty development table does not predict a large production workload reliably.
''','For a task query filtered by tenant and status and ordered by creation time/ID, propose an index. Explain how you would compare actual plans and what write/storage costs you would measure.',[
 ('Why can an index make writes slower?','Every relevant write may also update the index structure and its pages/log records. Additional indexes trade storage and write work for selected read paths.'),
 ('Why can a planner choose a sequential scan despite an index?','It may estimate that a large fraction of rows is needed or that index/table lookups cost more. Data distribution, statistics, table size and the exact query all affect the choice.')],
 ('What must you remember about EXPLAIN ANALYZE?',['It executes the statement to measure it','It never touches data under any circumstance','It automatically adds every useful index','It replaces backups'],0,'Execution makes it useful but requires care, particularly with data-changing statements.'),skills=[105,106,107,113,114])
 lesson(c,'db-transactions','ACID, isolation, locks and race-free updates',r'''
## A transaction groups a business invariant
Atomicity prevents a partially committed transaction. Consistency means the transaction must preserve the database's declared/business invariants, not that the database invents them. Isolation controls how concurrent work interacts. Durability concerns committed data surviving the failures promised by the configured system.

## The last-item problem
Reading stock=1 in two requests and later writing stock=0 twice can oversell. Use an atomic conditional update such as decrementing only where stock is sufficient and checking the affected-row result. Coordinate the order/payment workflow deliberately; a client-provided stock flag is not authoritative.

## Isolation is a contract
Read committed, repeatable-read and serializable behaviours differ by engine. Learn anomalies such as nonrepeatable reads, phantoms and write skew through specific interleavings. Serializable transactions can require retries; the application must retry the entire suitable transaction, not an arbitrary middle statement.

MVCC lets readers observe versions according to a snapshot policy. In PostgreSQL, ordinary readers and writers often avoid blocking each other, but locks and conflicts still exist. Lock resources in a consistent order, keep transactions short and handle deadlock/serialization errors explicitly.

Do not keep a database transaction open across an unbounded model or payment-provider call. Use a state machine, durable job/outbox or a well-defined reservation workflow when external side effects cannot join one database transaction.
''','Write a race-free stock decrement and describe two concurrent buyers. Then draw a write-skew example and explain whether a stronger isolation level or a constraint/lock is appropriate.',[
 ('Why is read-then-write stock checking unsafe?','Several requests can read the same available value before either writes. An atomic conditional update or properly coordinated transaction must enforce the invariant at the write boundary.'),
 ('Does MVCC mean no locks ever exist?','No. It changes how versions and snapshots serve readers, but writes, explicit locks, schema changes and isolation conflicts still require coordination and can block or abort work.')],
 ('Which best prevents stock from going negative?',['An atomic decrement conditioned on sufficient stock','A frontend disabled button only','An earlier unlocked read followed by an unconditional write','Trusting the requested quantity without validation'],0,'The condition and update must be enforced together under concurrency.'),
 ('sql','CREATE TABLE study_stock(id INTEGER PRIMARY KEY, quantity INTEGER CHECK(quantity >= 0));\nINSERT INTO study_stock VALUES (1,1);\nUPDATE study_stock SET quantity=quantity-1 WHERE id=1 AND quantity>=1;\nSELECT changes() AS first_success;\nUPDATE study_stock SET quantity=quantity-1 WHERE id=1 AND quantity>=1;\nSELECT changes() AS second_success;\nSELECT quantity FROM study_stock;','The first update changes one row, the second changes zero, and stock remains 0.'),skills=[108,109,110,111,112])
 lesson(c,'db-operations','Pools, migrations, backups, replicas and partitioning',r'''
## Connections are bounded resources
A connection pool reuses a controlled number of database connections. Size it against database capacity and the number of application instances, not just one process. Serverless scaling can multiply connections unexpectedly; a compatible pooler such as PgBouncer may help, with mode/transaction limitations that must match the application.

## Change schemas without breaking running code
Use expand/contract migrations and paced backfills for large data. Deploy compatible code, observe it, migrate data and remove old structures later. Set appropriate lock/statement timeouts and test rollback/recovery plans.

## Backups must be restorable
Logical backups describe database objects/data; physical backups capture storage-level state. Point-in-time recovery also depends on a correct log/archive strategy. A backup job reporting success is not proof: rehearse a restore and verify the data and recovery time.

Replicas can scale reads and improve recovery options, but replication lag means a just-written value may not be visible on every replica immediately. Decide which reads require read-your-writes consistency and route them appropriately.

Partitioning divides data within a database according to a rule; sharding distributes ownership across database nodes. Range/hash choices affect pruning, hotspots and operations. Do not shard merely because a project might grow: first measure indexes, queries, connection use and operational limits.
''','Specify a database recovery objective and restore rehearsal. Design a read-after-write path with replicas and a safe migration/backfill plan for a large task table.',[
 ('Why is a successful backup job insufficient evidence?','The backup may be incomplete, inaccessible or too slow to restore. A rehearsal verifies the actual recovery path, required credentials/logs and the promised recovery time/data-loss window.'),
 ('What can replica lag break in a UI?','A user writes successfully and then reads from a lagging replica, seeing an older value. The application needs a deliberate consistency/routing policy for such paths.')],
 ('What should precede sharding?',['Evidence that simpler query/index/operation improvements are insufficient','A guess that every app needs it immediately','Removing backups','Making every query unbounded'],0,'Sharding adds coordination and operational complexity, so it should solve a measured need.'),skills=[115,116,117,118,119])
 lesson(c,'db-documents','MongoDB documents, Mongoose and model choice',r'''
## Model access patterns
A document database stores structured documents, often with nested fields and arrays. Embedding related data can make a bounded read convenient; referencing can avoid unbounded duplication and support independent lifecycles. Choose based on how data is read/updated and its size/growth, not a slogan that documents have no schema.

Mongoose supplies application-side schemas, validation and mapping conventions. Database validation, indexes and transaction guarantees remain separate decisions. An application schema alone does not prevent another client from writing an incompatible document.

## Useful query discipline
Index the actual filters and sorts, paginate large collections and project only needed fields. Aggregation pipelines transform and combine data through stages; inspect cardinality and memory implications. A dynamic product specification may fit document modelling, while invoices/payments may require strong relational constraints or carefully designed document transactions.

Prevent operator/structure injection by validating request shape and building queries from allowed fields. Do not spread arbitrary client objects into a database filter. Atomic conditional updates can enforce a stock rule, but a multi-document business invariant still needs a coordinated transaction/workflow.

Relational, document and key-value models all have useful workloads. Explain your chosen consistency requirements, relationships and access patterns in an interview rather than presenting MERN or PERN as a complete architectural argument.
''','Model products with category-specific specifications and bounded variants. Decide which data is embedded versus referenced, and specify a safe filter/pagination contract.',[
 ('When is embedding a good choice?','When related data is naturally read/updated together, remains bounded and has a compatible lifecycle. Independent growth or many-to-many reuse may favour references and explicit query/consistency design.'),
 ('Does MongoDB mean no schema is needed?','No. The application still has a data contract, and validation/index/consistency choices remain important. Flexible storage does not make invalid or unbounded documents a good design.')],
 ('What is risky in a public search endpoint?',['Spreading arbitrary client objects directly into a database filter','Allowlisting supported filter fields','Bounding page size','Selecting only public output fields'],0,'Unvalidated structure can alter query semantics and expose unsupported operators or fields.'),skills=[120,121])
 lesson(c,'db-cache-search','Redis, text search, vectors and analytical workloads',r'''
## A cache needs an ownership policy
Cache-aside reads the cache, loads from the source on a miss and stores a value with a chosen expiry. Redis can support cached values, counters and other structures, but an expiring key does not automatically make invalidation correct. Choose keys that include tenant/user scope when the value differs by permission.

Prevent cache stampedes when many requests miss together through bounded coordination or suitable stale/refresh strategies. Define whether a failed cache should fall back to the source. A cache must not become an undocumented second source of truth.

## Search has several contracts
Full-text search ranks lexical terms and language-aware matches; PostgreSQL can be a useful starting point before a separate search engine is justified. Vector search compares embeddings and uses an index such as pgvector's supported structures. Semantic similarity does not prove factual correctness or permission to reveal a document.

For search engines, keep a freshness/reindex policy and apply access filters. Evaluate actual queries before changing technology. A faster retrieval of the wrong tenant's data is a security failure.

## OLTP versus OLAP
Transactional workloads optimise many bounded reads/writes and invariants. Analytical workloads scan/aggregate larger data sets, often benefiting from column-oriented storage and different data preparation. Sending every dashboard aggregation to the busiest transactional table can hurt request latency; measure before designing a separate warehouse/read model.
''','Define a tenant-scoped cached dashboard key, expiry and invalidation event. Compare exact keyword search, semantic search and a reporting aggregation for the same product catalog.',[
 ('Why is TTL not a complete invalidation policy?','A stale value can remain until expiry, and important changes may need immediate invalidation. Scope, source of truth and update/rebuild behaviour must be designed alongside the timeout.'),
 ('How do OLTP and OLAP differ?','OLTP focuses on bounded transactional operations and invariants; OLAP focuses on large scans and aggregations for analysis. Their storage/query patterns and latency trade-offs can differ.')],
 ('What must a private search cache key account for?',['The relevant tenant/user permission scope','Only the text colour','Only the public page title','A universal key shared across all private accounts'],0,'Different access scopes must not share a cached private result accidentally.'),skills=[122,123,124,125])
