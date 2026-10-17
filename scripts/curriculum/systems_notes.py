from .common import course,lesson

def build():
 c=course('os','Operating Systems','Systems foundations','Explain the processes, memory and I/O underneath your programs with concrete traces.','2-3 weeks alongside coding','Profile a small service, diagnose one resource limit and document graceful shutdown and concurrency behaviour.',['os','python','node'])
 lesson(c,'os-processes','Processes, threads, lifecycle and signals',r'''
## A process owns an execution context
A process has an address space and operating-system-managed resources. Threads within a process share much of that address space while having their own execution state/stacks. Sharing can make communication cheaper, but it also permits races. A crash or memory error in a native thread can affect the whole process.

## Lifecycle
A simplified process moves among ready, running and blocked/waiting states, then terminates. A scheduler chooses runnable work. A process blocked on I/O is not necessarily consuming a full CPU core. On Unix-like systems, fork creates a process context and exec replaces the program image; exact behaviour differs across operating systems.

Signals communicate events. SIGTERM requests termination and can be handled for graceful shutdown; SIGKILL forces termination and cannot be handled by the target. A service should stop accepting new work, finish or safely release in-flight work within a deadline, close resources and exit. Forced termination remains a fallback, not a normal flush strategy.

## Concurrency versus parallelism
Concurrency means overlapping progress; parallelism means simultaneous execution. One event loop can coordinate many waiting operations without doing several CPU instructions at once. Several threads/processes can run in parallel on suitable hardware and runtime configurations.

Context switches save/restore execution state and may disturb caches. More threads are not automatically faster. Measure runnable work, I/O waiting, CPU use and scheduling overhead for the actual workload.
''','Draw the lifecycle of a web request that waits on a database. Specify a graceful shutdown sequence for a worker and what happens if its deadline expires.',[
 ('How do processes and threads differ?','Processes normally have separate virtual address spaces; threads in one process share memory and many resources. Threads can communicate through shared objects but need coordination to protect invariants.'),
 ('Why handle SIGTERM before a forced kill?','It gives the service a bounded opportunity to stop new work, release/requeue jobs and close resources. A forced kill cannot run the target\'s cleanup logic.')],
 ('A process waiting on a network response is commonly in which simplified state?',['Blocked/waiting','Always running at full CPU','Already terminated','A database index'],0,'Waiting for I/O is different from being ready to execute CPU work.'),skills=[126,127,129,133])
 lesson(c,'os-scheduling','FCFS, SJF, Round Robin and priority scheduling',r'''
## Measure the same quantities
Arrival time is when work becomes ready, burst time is required CPU service and completion time is when it finishes. Turnaround = completion - arrival. Waiting = turnaround - burst in the simplified single-burst model. Response time measures when the first service begins, not when the process finishes.

FCFS serves arrival order and can make a short task wait behind a long one. SJF chooses the shortest available burst; its preemptive relative chooses shortest remaining work. These methods need burst estimates. Priority scheduling chooses by a priority policy and can starve low-priority work unless the design addresses it, for example through ageing.

Round Robin gives each ready process a time quantum. A very large quantum approaches FCFS; a very small one increases switching overhead. Real operating systems use more complex policies than this teaching model.

## Worked trace
All arrive at 0: P1 needs 5, P2 needs 3, P3 needs 1. FCFS P1/P2/P3 has waits 0,5,8: average 13/3. SJF P3/P2/P1 has waits 0,1,4: average 5/3. For Round Robin quantum 2, the sequence is P1(0-2), P2(2-4), P3(4-5), P1(5-7), P2(7-8), P1(8-9).

Always state arrival times, tie-breaking, preemption and context-switch assumptions before comparing algorithms. An average alone can hide a very poor response time for one class of work.
''','Calculate completion, turnaround, waiting and response times for the Round Robin trace. Then change P3 arrival to time 3 and recompute under an explicitly stated policy.',[
 ('How do waiting and turnaround differ?','Turnaround spans arrival to completion. In a simple one-burst model, waiting is turnaround minus CPU burst time; response time is the delay until first service.'),
 ('What is the Round Robin quantum trade-off?','A smaller quantum can improve initial responsiveness but increases switching overhead. A larger one reduces switches and increasingly behaves like FCFS for the ready queue.')],
 ('For arrival 2, burst 4 and completion 9, what is waiting time in the single-burst model?',['3','7','4','9'],0,'Turnaround is 9-2=7; waiting is 7-4=3.'),
 ('python','arrival, burst, completion = 2, 4, 9\nturnaround = completion - arrival\nprint(turnaround, turnaround - burst)','7 3'),skills=[128])
 lesson(c,'os-synchronisation','Critical sections, locks, semaphores and deadlock',r'''
## Interleavings can violate an invariant
A read-modify-write increment is several steps. Two workers can both read 0 and each write 1, losing an update. A critical section is the code region whose shared-state invariant must be protected. A mutex permits one owner; a semaphore tracks a count of permits and can bound concurrent access to a resource pool.

Locks need a clear scope and release path. Keep protected work small, avoid an external network wait while holding a lock and do not assume the language's runtime lock makes every business operation atomic. Read/write locks and fine-grained locks can help specific workloads but add design complexity.

## Deadlock requires four conditions
The classic conditions are mutual exclusion, hold-and-wait, no preemption and circular wait. Prevention breaks a necessary condition, such as a global lock order. Avoidance checks whether granting resources keeps the system in a safe state; an unsafe state is not automatically a current deadlock. Detection/recovery allows deadlocks to occur and then handles them.

## A concrete lock-order rule
If one operation locks A then B and another locks B then A, both can wait indefinitely. Require both to acquire in the same order and release reliably. Timeouts help detection/recovery but do not by themselves prove a race-free design.

Test concurrency with controlled barriers/interleavings where possible. A test that happens to run without collision once is weak evidence that a race cannot occur.
''','Trace the lost-update interleaving for two increments. Then describe a lock-order rule for transferring between two accounts and how a failed operation releases both locks.',[
 ('How do a mutex and a semaphore differ?','A mutex protects exclusive ownership of a critical region/resource. A semaphore represents permits and can allow a bounded number of concurrent users; correct ownership/release semantics still matter.'),
 ('Does a timeout prevent deadlock by itself?','It can bound waiting or trigger recovery, but the locking design still needs a correctness policy. Consistent ordering or an appropriate avoidance strategy addresses the circular dependency itself.')],
 ('Which is one classic deadlock condition?',['Circular wait','A sorted input array','A unique HTML ID','An empty task queue'],0,'Circular wait is one of the four necessary conditions in the classic model.'),skills=[130,131,132])
 lesson(c,'os-memory','Paging, virtual memory, stack/heap and garbage collection',r'''
## Virtual addresses are a mapping
Virtual memory gives a process an address-space abstraction. Paging maps fixed-size virtual pages to physical frames or other backing state; a translation cache such as a TLB accelerates common mappings. A page fault invokes the OS to resolve a missing/protected mapping and is not always a fatal program error. Excessive paging can cause thrashing and poor progress.

Segmentation models logical variable-sized regions; it is conceptually different from fixed-size paging. Real systems combine hardware/OS mechanisms, so do not reduce all address translation to a single classroom diagram.

## Stack and heap
Call stacks organise frames and control flow; heap allocation supports objects with other lifetimes/ownership patterns. The exact placement of a language value depends on its implementation and optimisation. Deep recursion can exhaust stack resources even when the algorithm's input data would fit elsewhere.

## Managed memory still leaks
Garbage collectors reclaim unreachable objects, not every object you no longer need logically. A cache, listener or global reference can keep obsolete data reachable. V8 uses generational collection techniques; CPython commonly combines reference counting with cyclic garbage collection, with build/version details that matter.

Container/cgroup memory limits add another boundary. A process may be killed for exceeding its limit even when the host has free memory. Compare heap metrics with total resident/native allocations and the configured limit before increasing one runtime heap setting.
''','Explain a page fault, a stack overflow and a retained-listener leak as three different failures. Design a bounded cache and a memory measurement plan for a Node or Python service.',[
 ('Why can a garbage-collected program leak memory?','Objects can remain reachable through a cache, closure, listener or global reference after they stop being useful. The collector cannot infer that the application no longer wants reachable data.'),
 ('Why can a container die while the host has free RAM?','The container/process can have its own enforced memory limit. Its runtime heap is only part of total memory, so native buffers and other allocations can exceed that boundary.')],
 ('What is a page fault?',['An event requiring the OS to resolve a memory mapping/access condition','Always a syntax error','A guarantee that RAM is physically broken','A CSS page break'],0,'A page fault can be part of ordinary virtual-memory operation or can indicate an invalid access.'),skills=[134,135,136,137,138])
 lesson(c,'os-io','File descriptors, file systems and durable writes',r'''
## Open resources have identities and limits
A file descriptor is a process-visible handle for an open resource such as a file, socket or pipe on Unix-like systems. A descriptor table and OS limits bound how many can be open. Leaking sockets/files can cause too-many-open-files errors even when CPU and memory look acceptable.

Blocking I/O waits in the calling execution context. Nonblocking I/O reports readiness/progress without requiring that thread to wait for every operation. Readiness mechanisms such as epoll or kqueue help event loops coordinate many resources; they do not make arbitrary CPU work parallel.

## File-system concepts
A filename maps through directory structures to underlying file metadata/data. Inodes, hard links, symbolic links, permissions, mounts and volumes explain why a path and a stored object are not always the same concept. A container's writable layer and a persistent mounted volume have different lifecycles.

## A successful write is not every durability guarantee
Data may first enter language/runtime buffers and OS page caches. Flushing those layers and calling filesystem synchronisation where required serves different purposes. Atomic rename/replacement can prevent ordinary readers seeing a partial destination, but a crash-durability design must also consider the filesystem and directory metadata guarantees.

Use context managers/finally blocks to close resources. Bound concurrent uploads/downloads and inspect descriptor counts under a sustained workload, including cancelled and failed requests.
''','Design safe persistence for a local notes file: encoding, temporary file, replacement, concurrent writers, backup and crash recovery. Explain why closing descriptors and ensuring durable data are related but distinct.',[
 ('Why can a service exhaust file descriptors?','It may leak open files/sockets or start too much concurrent I/O. Inspect ownership and cleanup paths, including failures, before treating a higher limit as the complete fix.'),
 ('Does write() returning mean data is safe against power loss?','Not universally. Buffers and OS caches can still hold it. Durability depends on explicit synchronisation and the storage/filesystem guarantees required by the application.')],
 ('Which resource can consume a file descriptor?',['A network socket','Only a plain-text .txt file','Only a Python integer','Only a Git commit'],0,'Descriptors can represent sockets, files, pipes and other OS-managed open resources.'),skills=[139,140,141,142])
 lesson(c,'os-linux','Linux shell, permissions, containers and service logs',r'''
## Navigate and inspect before changing
Learn pwd, cd, ls, path quoting and file permissions. Pipes connect streams; redirection changes stream destinations. Tools such as grep/rg, sed, awk, find and xargs transform/search data, but filenames with spaces/newlines require correct quoting or null-delimited handling. Inspect an absolute path before destructive operations.

Use ps/top/htop for processes, lsof for open resources and strace where appropriate for system-call diagnosis. A process existing is not proof that its service is healthy; check the relevant health endpoint and actual work.

## Least privilege
Users/groups and read/write/execute permissions determine access. Directory execute permission affects traversal. Run services with a suitable non-administrator account and grant only required paths/operations. chmod 777 is not a general deployment repair.

## Containers share the host kernel
Namespaces isolate selected views/resources and cgroups apply resource controls. A container is not simply a full virtual machine and is not an automatic boundary against every possible escape or host exposure. Docker images/layers package a filesystem/configuration; Compose coordinates related local services. Use mounted volumes for intended persistence.

On systems using systemd, service units declare startup/restart policy and journalctl helps inspect logs. Handle signals and configure restart limits so a broken process does not spin forever without an actionable error.
''','Write a non-destructive diagnosis checklist for a service returning 503: process, port, logs, dependencies, permissions and limits. Explain which data needs a persistent volume.',[
 ('How is a container different from a virtual machine?','A container generally isolates a process environment while sharing the host kernel. A VM typically virtualises hardware to run a guest kernel, with different isolation and resource trade-offs.'),
 ('Why is chmod 777 a poor default fix?','It grants broad access without identifying the required owner and operation. Diagnose the path/identity mismatch and assign the minimum permissions needed.')],
 ('What should persist outside a disposable container layer?',['The application data that must survive replacement','Every temporary build cache by default','A private key baked into a public image','Only the container name'],0,'Persistent data needs an explicit volume or external storage lifecycle.'),skills=[143,144,145,146,147,148])

 c=course('networks','Computer Networks','Systems foundations','Trace a request through addressing, transport, HTTP and failure recovery.','2-3 weeks','Draw and measure one browser-to-API request, then define timeout, retry, cache and access policies.',['network','os'])
 lesson(c,'net-models','LAN/WAN, OSI, IP addresses and subnets',r'''
## Layers are a debugging map
A local network connects nearby devices; a WAN spans broader networks. OSI is a seven-layer teaching model: physical, data link, network, transport, session, presentation and application. TCP/IP groups responsibilities differently. Use the models to ask where a failure occurs rather than treating every protocol as a perfect one-layer box.

An IP address identifies an interface in an addressing/routing context. IPv4 uses 32 bits and IPv6 128. A MAC address participates in local link delivery; routers move packets between networks using routing information. NAT translates addresses/ports at a boundary and is not a complete firewall policy by itself.

## Read CIDR notation
A prefix length says how many leading bits identify the network. An IPv4 /26 leaves 6 host bits, so it spans 64 addresses. Under the usual network/broadcast teaching assumptions that gives 62 ordinary host addresses; special cases such as point-to-point /31 links have different rules.

DHCP can supply addressing/configuration to a client. DNS maps names to relevant records; it is not the same as assigning a machine's local address. Private address ranges need routing/NAT/tunnels as appropriate to communicate beyond their networks.

When a request fails, check link connectivity, local address, route, name resolution, transport connection and application response in order. A successful ping alone does not prove an HTTPS endpoint works.
''','For an ordinary IPv4 /27 subnet, calculate its address count and usual host count. Draw the roles of a switch, router, DNS resolver and application server.',[
 ('How do IP and MAC roles differ?','IP supports addressing/routing across networks. MAC addresses support local link delivery within the relevant link-layer context; a remote destination is reached through next-hop links, not one global Ethernet segment.'),
 ('Why is the OSI model useful in an interview?','It gives a structured way to locate a problem: physical/link connectivity, addressing/routing, transport, encryption/protocol and application behaviour. It is a map, not a substitute for the actual protocol details.')],
 ('How many total addresses are in an IPv4 /27 block?',['32','27','64','128'],0,'32-27=5 host bits, giving 2^5=32 total addresses.'),
 ('python','import ipaddress\nnetwork = ipaddress.ip_network("192.168.1.0/27")\nprint(network.num_addresses)\nprint(len(list(network.hosts())))','32\n30'),skills=[149,150])
 lesson(c,'net-transport','TCP, UDP, ports and HTTP versions',r'''
## Transport connects application endpoints
A port identifies a transport/application endpoint within an address/protocol context. TCP supplies an ordered reliable byte stream with connection state, acknowledgements and congestion control. Its handshake establishes connection parameters; application message framing still has to be defined above the stream.

UDP sends datagrams without TCP's built-in reliable ordered stream contract. It is useful when the application or a higher protocol wants different latency/recovery trade-offs. UDP does not mean an application can never add reliability or encryption.

## Compare failure and latency
TCP retransmission recovers loss but ordering can make later bytes wait behind missing earlier bytes. Congestion control tries to avoid overwhelming the path. A fast local server can still feel slow across a high-latency or lossy connection.

HTTP/1.1, HTTP/2 and HTTP/3 have different transport/multiplexing behaviour. HTTP/2 multiplexes streams over a TCP connection; transport-level loss can still affect progress. HTTP/3 uses QUIC over UDP and provides a different stream/recovery design with integrated modern security mechanisms.

Do not choose a protocol only from a slogan that one is fast. Consider intermediaries, browser support, connection setup, loss patterns and the actual workload. WebSockets and SSE are application communication choices layered on these capabilities.
''','Explain TCP versus UDP for a file download and a realtime voice application. Then describe why several HTTP/2 streams can still be affected by one lost TCP segment.',[
 ('Does TCP preserve application message boundaries?','No. It presents an ordered byte stream. The application protocol must define lengths, delimiters or another framing mechanism to reconstruct messages.'),
 ('Does using UDP guarantee low latency?','No. Network congestion, application buffering and the higher-level protocol still matter. UDP offers datagrams with fewer built-in delivery guarantees; the application chooses what to add.')],
 ('Which statement is accurate?',['HTTP/3 uses QUIC over UDP','HTTP/2 eliminates every form of head-of-line delay','UDP cannot carry encrypted traffic','TCP automatically frames JSON messages'],0,'HTTP/3 changes transport through QUIC; the other statements overgeneralise.'),skills=[151,152,161])
 lesson(c,'net-dns-tls','DNS resolution and TLS trust',r'''
## Resolve a name before connecting
A client normally asks a resolver for records. Cached answers can avoid further work; otherwise the resolution process follows the relevant authoritative hierarchy. A/AAAA records supply addresses, CNAME expresses an alias and other records serve other purposes. TTL influences cache lifetime; a DNS edit does not instantly erase every cached answer.

## Establish an encrypted authenticated channel
TLS negotiates security parameters and proves the server controls a suitable credential for the requested identity under a trusted certificate chain. The client checks names, validity and trust. The padlock does not prove that the site's business claims are honest or that its application has no bugs.

Keep certificate renewal and hostname configuration operationally visible. A certificate error is not repaired safely by disabling verification in every client. For internal services, use an appropriate trust configuration rather than copying an insecure bypass.

## Diagnose the phases separately
Measure DNS, TCP/QUIC connection establishment, TLS negotiation, server processing and body transfer. A slow name lookup and a slow database query require different fixes. Reused connections and caches change repeat-request timings, so test under clear conditions.

DNS and TLS also affect deployment: a new domain, CDN or proxy can introduce stale records, wrong certificate names or an unexpected origin. Verify the actual deployed route rather than only a local hosts-file shortcut.
''','Draw a first visit to a new HTTPS hostname. Mark the DNS resolver/cache, connection, certificate check and HTTP request. Explain what a stale DNS cache can and cannot affect.',[
 ('What does a valid TLS certificate establish?','It supports an authenticated encrypted connection to the named endpoint under the client\'s trust model. It does not certify every application behaviour or business statement on that site.'),
 ('Why can a DNS change appear inconsistent temporarily?','Resolvers and clients can retain earlier answers according to cache/TTL behaviour. Different request paths may therefore use different cached records until they refresh.')],
 ('What should you do with a certificate-name mismatch?',['Fix the hostname/certificate configuration','Disable verification globally','Put a private key in the browser','Assume the database is corrupt'],0,'Verification errors identify a trust/configuration problem; bypassing them broadly removes the protection.'),skills=[153,154])
 lesson(c,'net-http','HTTP semantics, caching, CORS and cookies',r'''
## Requests and responses have meaning
HTTP methods, status codes and headers form a contract. Safe methods should not request state-changing semantics; idempotency describes repeated intended effect. A 2xx response, redirect, client error and server error need different handling. A frontend should not parse every response body as a successful domain object.

## Cache deliberately
Cache-Control specifies relevant reuse rules; ETag can identify a representation for conditional requests. A 304 response allows reuse of a validated cached representation. no-cache and no-store are different: one concerns reuse without validation, the other forbids storing under its rules. Shared versus private cache scope matters for user-specific data.

## Browser boundaries
CORS controls whether browser script may read a cross-origin response. Some requests trigger a preflight. A non-browser caller is not authenticated merely because the CORS allowlist is narrow. For credentialed browser access, configure explicit origins and the relevant cookie/credential policy; a wildcard is not a universal fix.

Cookies match domain/path and other policy constraints. Secure restricts transmission to secure contexts under its rules; HttpOnly blocks ordinary JavaScript cookie access; SameSite affects cross-site sending. These are complementary controls, not replacements for authorisation or CSRF analysis.

Learn common application protocols around this model: SMTP carries email, FTP is a file-transfer protocol family and DNS has its own record/query semantics. Their names alone do not imply modern secure deployment defaults.
''','Design cache headers for public static assets and a private progress endpoint. Explain a preflight failure separately from an expired login session and a server-side permission denial.',[
 ('How do no-cache and no-store differ?','no-cache permits storage but requires suitable validation before reuse. no-store directs caches not to store the response under its rules. Neither is an object-level permission check.'),
 ('Why is CORS not authentication?','It is enforced by browsers for script access to responses. Other HTTP clients can still call an endpoint, so the server needs real authentication and authorisation.')],
 ('Which cookie flag blocks ordinary JavaScript reads?',['HttpOnly','A CSS class','Cache-Control: public','The route name login'],0,'HttpOnly limits script access; transport, cross-site sending and permissions need separate controls.'),skills=[155,156,157,158])
 lesson(c,'net-streams','WebSocket and SSE connections through proxies',r'''
## A persistent connection changes operations
A WebSocket begins through a handshake and then supports bidirectional messages. An SSE response streams framed server events over HTTP. Both need authentication, capacity limits and a recovery policy; keeping one connection open does not guarantee every important event is delivered durably.

## Intermediaries matter
A reverse proxy can buffer output, enforce idle timeouts or reject an upgrade. Test through the deployed proxy/load balancer, not only directly against a development server. Configure heartbeat and timeout behaviour without creating excessive traffic or an unbounded connection count.

## Reconnection is an application contract
Use event IDs, sequence/version information or a snapshot resynchronisation path. Duplicate delivery should be harmless. If the server retains only a short replay window, explain what the client does after a longer offline period.

For streamed AI text, distinguish receiving chunks from completing a valid answer. A network chunk can split a UTF-8 sequence or logical event; use a streaming decoder/parser. When the user stops generation or leaves, propagate cancellation so expensive provider work does not continue without a consumer.

Bound per-client buffers and slow-consumer behaviour. A service can look healthy under fast local clients and exhaust memory with a few stalled readers. Persist business changes independently so a dropped connection cannot erase the real task or payment state.
''','Specify a notification stream that recovers after a disconnect, including replay limits and duplicate IDs. Name one proxy setting that can make a locally working stream appear frozen in production.',[
 ('Why can SSE appear to deliver everything at once?','A server or intermediary may buffer chunks instead of forwarding the stream promptly. Verify framing, flush behaviour and proxy configuration through the actual deployment path.'),
 ('Why should a stop button cancel the backend job?','Otherwise the UI stops showing output while the server/provider may keep doing costly work. Cancellation needs to cross the browser, server and provider/worker boundaries.')],
 ('What is a safe reconnect strategy?',['Replay by event ID or reconcile a fresh snapshot','Assume no events were missed','Append every duplicate forever','Disable authentication after reconnect'],0,'Recovery must restore a known state despite gaps and duplicates.'),skills=[159,160])
 lesson(c,'net-resilience','Latency, timeouts, retries and circuit breakers',r'''
## Separate latency sources
DNS, connection setup, TLS, server queueing, database/provider work and transfer all contribute. Measure percentiles and component timings. An average can hide a slow tail that dominates user complaints.

Every outbound call needs bounded connect/read/overall behaviour appropriate to the client. A timeout is not proof that a side effect did not happen. Retry only failures that are safe under the operation's idempotency contract and useful under the remaining deadline.

## Backoff and budgets
Exponential backoff increases delay between attempts; jitter avoids synchronised clients retrying together. Limit attempt count and total elapsed time. Respect relevant 429/Retry-After signals. Several layers each retrying independently can multiply load, so coordinate the retry budget.

## Fail fast when a dependency is unhealthy
A circuit breaker can stop repeated calls after a failure threshold and later allow limited probes in a half-open state. It needs useful metrics and recovery behaviour; it is not a substitute for fixing the dependency. A fallback should preserve a clear reduced capability instead of returning fabricated success.

Load tests should include a slow or unavailable dependency, not just a healthy local server. Observe queue growth, pending requests and recovery after the dependency returns. A service that recovers by sending every queued request at once can trigger another outage.
''','Design a report-provider call with an overall deadline, per-attempt timeout, safe retry conditions, jitter and a deterministic fallback. Explain which requests must not be retried blindly.',[
 ('Why add jitter to backoff?','Many clients can fail at the same time. Randomised delay spreads their retries instead of creating another synchronised traffic spike against the recovering service.'),
 ('What is a retry budget?','A limit on attempts and/or total time/load spent retrying. It keeps one user action or outage from causing unbounded multiplied work across several system layers.')],
 ('Which operation most needs idempotency before retrying?',['Creating a payment after an ambiguous timeout','Reading a public static document','Calculating a local sum','Formatting a date'],0,'The payment might already have succeeded, so a blind retry can duplicate its effect.'),skills=[162,163,164,165])
 lesson(c,'net-operations','Proxies, load balancers, CDNs and network tools',r'''
## Place the network components deliberately
A reverse proxy receives client traffic and forwards it to an application. A load balancer distributes requests/connections and checks backend health. Layer-4 decisions operate around transport information, while layer-7 systems can use application/HTTP information. Sticky routing can affect realtime/session designs but should not hide a missing shared-state policy.

CDNs place cached content closer to users. Define cache keys, freshness, private-data exclusions and invalidation. A CDN can speed the wrong response just as effectively as the right one. Validate origin and edge behaviour separately after deployment.

## Diagnose with focused tools
curl -v shows request/response and connection details. dig investigates DNS, ss inspects sockets and traceroute can help reason about a path, with important filtering/interpretation limits. A browser Network panel reveals preflights, redirects, status and timing that a screenshot cannot.

## Bound exposure
Firewalls and security groups restrict allowed traffic. Private subnets can reduce direct exposure, but identity, patching and service permissions are still needed. DDoS resilience combines provider/network controls, resource limits and application design; a login rate limit alone does not protect every layer.

Use separate health/readiness checks when the platform supports that distinction. An application can be alive but not ready to accept work because a required dependency or migration is unavailable.
''','Draw browser, CDN, load balancer, API and private database. For a 502 response, state which logs/health checks you would inspect and why a direct local 200 is insufficient.',[
 ('How do liveness and readiness differ conceptually?','Liveness asks whether the process should keep running; readiness asks whether it should currently receive traffic. A live process may be temporarily unready due to startup or a dependency condition.'),
 ('Why test through the actual proxy/CDN path?','Intermediaries can alter caching, routing, headers, timeouts and streaming. A direct backend success does not prove the user-facing route has the same behaviour.')],
 ('Which tool is directly useful for inspecting HTTP headers and redirects?',['curl -v','Only a CSS formatter','A database diagram alone','A code-theme selector'],0,'An HTTP client with verbose output exposes the actual request/response path.'),skills=[166,167,168,169])

 c=course('devops','DevOps & Cloud','Production engineering','Build reproducibly, deploy safely, observe failures and understand resource costs.','3-4 weeks','Containerise one project, run CI, deploy a reviewed build and demonstrate a rollback plus a restore rehearsal.',['docker','git','network'])
 lesson(c,'ops-delivery','Docker, CI and safe releases',r'''
## Build an artefact you can promote
A container image packages the application and its runtime dependencies into layers. A multi-stage build can keep build tools out of the final runtime image. Pin useful versions, avoid baking secrets into layers and run with an appropriate non-root identity when possible. Compose helps coordinate local dependencies with explicit configuration/volumes.

## Continuous integration
A workflow should install locked dependencies, run meaningful lint/type/test checks and produce a build. It needs limited permissions and protected handling of untrusted pull requests. A failing required check should block the release path instead of being silently ignored.

Use development, preview/staging and production environments with explicit configuration. Prefer promoting the same reviewed build rather than rebuilding untracked differences for each environment. Validate the deployed page/API and its critical assets after publication.

## Release safely
Feature flags separate deployment from enabling behaviour. A canary exposes a controlled portion of traffic and watches the relevant metrics. A rollback must account for database compatibility, background workers and external side effects, not only the web image tag.

Keep a small runbook: what success looks like, which signal triggers rollback, who/what performs it and how data remains compatible. A pipeline completing is useful evidence, but the user's actual journey is the final operational check.
''','Design CI and release steps for a task API and frontend. Include a container build, migration compatibility check, smoke test, feature flag and measurable rollback trigger.',[
 ('Why use a multi-stage Docker build?','It can separate compilers/build dependencies from the smaller runtime artefact. This reduces unnecessary runtime contents, while dependency trust and configuration still need deliberate controls.'),
 ('Why can an application rollback fail after a schema change?','The old application may no longer understand the new schema or data. Backward-compatible migration order and a tested data strategy are needed before assuming a source/image rollback is safe.')],
 ('Which is the strongest deployment practice?',['Promote a reviewed tested artefact and verify the live path','Rebuild manually from untracked local files','Ignore failed checks and hope','Publish private environment files with the static site'],0,'Reproducible artefacts and live verification connect reviewed source to actual behaviour.'),skills=[170,171,172,175])
 lesson(c,'ops-iac','Infrastructure as code and secret management',r'''
## Configuration is part of the system
Infrastructure as code describes resources such as networks, services and databases through reviewable configuration. Terraform/Pulumi can plan and apply changes, but a generated plan still needs review: a mistaken replacement can destroy data or change exposure.

State tracks the relationship between definitions and deployed resources. Protect it because it can contain sensitive values and operational authority. Coordinate concurrent changes through the tool's appropriate locking/backend design.

## Secrets have lifecycles
Use per-environment credentials with limited privileges. Keep them out of Git, frontend bundles, container layers and ordinary logs. A .env file is a local configuration convenience, not encryption or a complete secret-management platform. Production platforms can inject protected configuration or use a dedicated secret manager/workload identity.

Rotate credentials deliberately, revoke exposed ones and test that services reload/use the intended version. A secret removed from the latest commit may remain in history, caches or a published artefact. Avoid copying production secrets into preview environments.

Review infrastructure changes by intended outcome: which identities can read/write, which ports become reachable, which data persists and how rollback/restore works. A low-diff configuration edit can still have a large real-world effect.
''','Describe a staging/production secret policy and a rotation plan for a database credential. Review a hypothetical infrastructure plan that replaces a database and explain the required recovery evidence.',[
 ('Why protect infrastructure state files?','They describe deployed resources and can contain sensitive attributes or authority-related information. Treat their access, locking and backups as part of the system\'s security and recovery design.'),
 ('Why use different secrets per environment?','It limits the impact of a leak and prevents a compromised preview/test environment from automatically gaining production access. Permissions and rotation can then be managed independently.')],
 ('Where must a private server key never be placed?',['A publicly delivered frontend bundle','A protected server secret store','A carefully scoped deployment secret','A restricted runtime environment'],0,'Every visitor can inspect frontend assets, regardless of minification.'),skills=[173,174])
 lesson(c,'ops-cloud','Compute, storage, IAM and deployment models',r'''
## Learn one provider through the primitives
Compute runs work; a managed database stores/query data; object storage holds files; identity/access management determines who can perform operations. A virtual network/subnet/security-group design controls connectivity. Understanding these primitives transfers better than memorising console screenshots.

## Object storage
Use bucket/object keys with explicit tenant ownership and access policy. Presigned URLs delegate a bounded operation for a time window; they are capabilities, not harmless public labels. Validate upload size/type and do not let a caller choose another tenant's object name. Backups and retention need an explicit policy.

## Functions or long-running containers?
Serverless functions can fit bursty bounded requests but have platform-specific execution, connection and cold-start limits. Long-running containers can fit workers, persistent streams or other service lifecycles. Choose the deployment model that matches the operation rather than forcing a long job into a short request.

Kubernetes provides concepts such as pods, deployments and services for orchestration, but it adds operational machinery. Learn the concepts and use it when the system/team requirements justify it; a small application does not automatically need a cluster.

For this site, static GitHub Pages hosting serves files while a local launcher provides optional native operations. A static host cannot execute your Python backend just because its source file is uploaded. Hosting plans, quotas and prices change, so verify them before selecting a provider for a new project.
''','Choose compute/storage/network primitives for a private report API and a public image catalog. Decide which operation fits a function and which needs a worker, with explicit timeout and access assumptions.',[
 ('Why is a presigned URL sensitive?','It grants a particular operation under its scope/expiry, so someone who obtains it may use that capability. Keep its permissions narrow and avoid exposing a broader or longer-lived URL than needed.'),
 ('When might a long-running worker fit better than a function?','When work exceeds request/runtime limits, needs a durable queue lifecycle or requires long-lived processing. The choice depends on the platform\'s actual limits and operational contract.')],
 ('What does IAM primarily govern?',['Which identities can perform which resource operations','Only the CSS theme','Only array sorting','The number of React components'],0,'Identity/access policy controls authority over cloud resources.'),skills=[176,177,178,180,181])
 lesson(c,'ops-cost','Cost per user, quotas and capacity planning',r'''
## Cost follows a workload
Identify the unit that grows: requests, stored bytes, database connections, egress, background jobs or model tokens. Estimate cost per useful user action instead of comparing only a provider's headline free tier. A low request count can still be expensive if each request triggers several long model calls or transfers a huge file.

## Set measurable budgets
Define per-tenant limits, maximum input/output sizes and concurrency. Cache appropriate repeated work, but keep private-data scope and correctness intact. Rate limiting prevents some abuse; it does not replace capacity planning for legitimate spikes.

Measure latency, saturation and errors as load increases. A system near a database connection limit may fail suddenly rather than slow smoothly. Include downstream limits and retry amplification in the model.

## A concrete estimate
If one report uses 1,000 input and 200 output tokens, record those quantities independently because pricing can differ. Multiply by report frequency and active tenants, add retries and cache-hit assumptions, then compare the estimate with observed usage. Do not hard-code today's provider price as an eternal constant.

Use alerts and spending controls where supported, review anomalous usage and keep a graceful reduced-capability path. Saving money by silently discarding required data or bypassing access checks is not an acceptable optimisation.
''','Estimate monthly work for 200 tenants generating four reports each, with 10% retries and a documented cache policy. List the quantities you need before calculating an actual bill.',[
 ('Why track cost per useful action?','It connects infrastructure/model spending to product usage and exposes expensive fan-out or retries hidden by aggregate request counts.'),
 ('Why include retries in capacity estimates?','Failures can multiply downstream work. A service sized only for healthy first attempts can overload its dependencies precisely when they are already struggling.')],
 ('Which quantity can make an AI feature unexpectedly expensive?',['Repeated large input/output token usage and retry fan-out','Only the page background colour','Only the file extension of a README','Only the number of navigation links'],0,'Actual model work and retry patterns drive usage, latency and cost.'),skills=[179])
 lesson(c,'ops-observability','Logs, metrics, tracing and actionable alerts',r'''
## Different signals answer different questions
Structured logs explain events with safe fields such as request/job IDs, component and error category. Metrics summarise rates, latency distributions and saturation over time. Traces connect spans across services and dependencies so one slow request can be followed end to end.

OpenTelemetry provides instrumentation conventions/tooling for traces and related signals. Propagate correlation context across HTTP, queues and model calls without logging private prompts indiscriminately. A trace should show where time went and which operation failed, not become a secret dump.

## Measure a distribution
Average latency can look fine while a minority of users wait much longer. Percentiles such as p95/p99 describe the tail but need sufficient sample size and a correctly aggregated metric. Track error rate, queue age, CPU/memory/connection saturation and dependency health alongside latency.

Error trackers such as Sentry group failures and associate them with releases/source maps. Scrub sensitive fields and ensure deployed source maps match the release being diagnosed.

## Alerts need an action
Alert on user-visible symptoms or impending resource exhaustion with a runbook and an owner. Too many noisy alerts train people to ignore them. A useful alert states the affected capability, evidence, likely diagnosis path and immediate mitigation. Test that the alert actually fires in a controlled failure exercise.
''','Design signals for a report API: one structured log, three metrics, a trace with database/provider spans and an alert that has a concrete mitigation.',[
 ('How do logs and traces differ?','Logs record discrete events; traces link timed spans in one distributed operation. Correlation IDs let you move between them, while metrics reveal aggregate trends.'),
 ('What makes an alert actionable?','It identifies a meaningful symptom/threshold, relevant context, an owner and a response path. An alert with no useful decision or mitigation mainly creates noise.')],
 ('Which metric can reveal a slow minority hidden by the mean?',['A suitable tail latency percentile','Only the total source line count','Only the logo file size','Only the number of Git branches'],0,'Tail latency measurements expose delays that an average can conceal.'),skills=[182,183,184,185,186])

 c=course('security','Application Security','Production engineering','Protect identities, data and side effects through explicit trust boundaries and tests.','Study throughout every project','Threat-model one project, test cross-tenant access and webhook replay, and document dependency/secret controls.',['owasp','network','payment'])
 lesson(c,'security-risks','OWASP risks and threat modelling',r'''
## Start with assets and boundaries
List valuable data/actions, the identities that may access them and where untrusted input enters. Draw browser, API, database, storage and external-provider boundaries. For each, ask how an attacker could read another user's data, change a price, replay a request or exhaust resources.

## OWASP Top 10:2025 as a review map
The named 2025 list groups risks into broken access control, security misconfiguration, software supply-chain failures, cryptographic failures, injection, insecure design, authentication failures, software/data integrity failures, security logging/alerting failures and mishandling of exceptional conditions. It is an awareness map, not proof that a checklist guarantees security.

Connect each group to your stack: tenant-filtered queries for access, non-debug production configuration, reviewed dependencies, appropriate secret/password protection, parameterised queries, abuse-resistant workflows, session controls, verified artefacts/events, useful monitoring and bounded fail-safe error paths.

## Design before patching symptoms
A permission check at one route cannot repair a data model that has no reliable ownership information. An encrypted connection cannot repair an endpoint that returns another tenant's invoice. Prioritise the actual business invariant and enforce it at the relevant boundary.

Test negative paths on systems you own: cross-account IDs, malformed fields, duplicate events and unavailable dependencies. Record what the test proves and its limits; a single successful scan does not establish permanent safety.
''','Create a threat model for a client portal with invoices and uploaded documents. For each major asset, name the allowed identities, likely abuse and one concrete test/control.',[
 ('Why is threat modelling more useful than blindly adding middleware?','It identifies the actual assets, trust boundaries and abuse paths. Controls can then enforce relevant invariants instead of creating an impressive but incomplete list of packages.'),
 ('Does passing an OWASP checklist prove the application is secure?','No. It improves coverage of common risk classes, but the real design, configuration, dependencies and changing behaviour still need analysis and tests.')],
 ('Which is a direct broken-access-control example?',['Tenant A can download tenant B\'s invoice by changing an ID','A page uses a different font','A static image loads slowly','A local variable is named total'],0,'The caller is accessing an object outside the authorised relationship.'),skills=[187])
 lesson(c,'security-injection','SQL/NoSQL injection, XSS and CSP',r'''
## Separate code structure from data
SQL injection occurs when untrusted input changes query structure. Parameterised values protect that boundary; dynamic table/column/order choices need an allowlist or safe structural construction. An ORM can still be misused through unsafe raw queries.

NoSQL queries also have structure and operators. Validate the expected field types and construct supported filters explicitly rather than accepting an arbitrary client object. Command execution adds another boundary: avoid invoking a shell for data arguments and restrict the executable/argument contract.

## Render text as text
Cross-site scripting lets attacker-controlled content execute in a user's web context. Use safe text insertion or framework escaping by default. When rich HTML/Markdown is an intentional feature, use a maintained sanitiser with a deliberate policy and validate URL schemes. Do not execute model-generated or imported code merely because it appears in a lesson.

A Content Security Policy can reduce the impact of selected injection paths, but it is not a replacement for correct encoding/sanitisation and it must match the real application. Avoid weakening the entire policy to silence one blocked resource without investigating it.

## Verify behaviour
Test an HTML-looking task title and an unsupported query shape in a controlled local test. The expected outcome is inert text or a validation error, not a page script or a widened database filter. Keep legitimate content working while closing the unsafe interpretation boundary.
''','Review a task-title renderer, a raw SQL search and an imported Markdown preview. Specify safe handling for each and a regression test that demonstrates inert untrusted input.',[
 ('Why is input filtering alone a weak universal XSS defence?','The safe representation depends on the output context, and many legitimate characters are useful. Use context-appropriate encoding/safe APIs and a maintained sanitiser when HTML is intentionally supported.'),
 ('Can a CSP replace output sanitisation?','No. It can constrain selected execution/resource behaviours, but application-safe rendering remains necessary. An overly broad or bypassable policy does not repair unsafe HTML construction.')],
 ('Which is the best default for rendering a user note?',['Insert it as text','Evaluate it as JavaScript','Treat every URL scheme as safe','Concatenate it into an event-handler attribute'],0,'Plain text avoids an unnecessary executable interpretation boundary.'),skills=[188,189])
 lesson(c,'security-access','CSRF, IDOR and multi-tenant isolation',r'''
## The browser can send ambient credentials
A session cookie may be attached to a request under browser policy even when a different site initiated the action. CSRF protection considers which state-changing requests can be induced and which tokens/origin/SameSite controls apply. Use framework-supported protection and do not change state through a supposedly safe GET endpoint.

SameSite reduces some cross-site request scenarios, but it is not a universal replacement for analysing the session design. HttpOnly addresses script access to a cookie, not whether an authenticated request is authorised for a particular object.

## IDOR is an object relationship failure
An opaque or random ID can reduce guessing but is not access control. Every invoice/task/download/search result needs an authorisation condition based on verified identity and the object's ownership/relationship. Enforce it in service/query boundaries so a second route cannot accidentally bypass a first route's check.

## Tenant isolation includes derived paths
Scope cache keys, object-storage paths, background jobs, exports, search indexes and realtime rooms. A correctly filtered main list is insufficient if a PDF export or semantic search can retrieve another tenant's data.

Test tenant A versus tenant B through read, update, delete, nested resources and direct file access. Verify error behaviour without disclosing unnecessary information about whether another tenant's object exists. Log denied sensitive operations without putting the protected data into the log.
''','Write a tenant-isolation test matrix for tasks, invoices, uploads, search, exports and socket rooms. Explain why UUIDs alone do not satisfy any row of that matrix.',[
 ('Why are random IDs not authorisation?','A user can obtain an ID through sharing, logs or another leak. The server must verify the relationship between the caller and the object regardless of how guessable the identifier is.'),
 ('Where can tenant leaks occur beyond API routes?','Shared caches, object storage, background jobs, search indexes, exports and realtime room membership can all cross the same boundary if tenant scope is missing.')],
 ('What is the correct basis for an invoice access decision?',['Verified identity plus the invoice\'s permitted ownership/relationship','Only whether its ID is hard to guess','Only whether the button was visible','Only whether the request used HTTPS'],0,'Transport and identifier design do not establish object-level authority.'),skills=[190,191,192])
 lesson(c,'security-events','Webhook replay, API limits and fail-safe errors',r'''
## Verify, then apply a bounded operation
A valid webhook signature authenticates the signed bytes under the provider contract. Replay protection also needs a stable event/operation identity and an idempotent state transition. Timestamp checks can help where the signing protocol supports them, but clocks and retry windows need a defined policy.

Validate content type, body size, expected event type and relevant business identifiers. Preserve raw bytes for the signature operation. Reject invalid events without performing a partial side effect, and retain safe delivery evidence for investigation.

## Limits protect several layers
Rate limits can apply by account, tenant, endpoint or another verified key. A login limit and a report-generation quota address different costs. Bound concurrency, request size, output size and execution time as well as request count.

Security headers and CORS are additional controls with their own contracts. Do not mark an operation successful simply because one optional downstream call timed out. Fail safely: return a stable error or a clearly labelled reduced capability, release resources and preserve a retry/recovery path.

For a native local code runner, same-origin/token checks protect the API boundary, while the program still executes with the computer user's permissions. Calling it a sandbox without OS isolation would give the user a false safety model.
''','Design a webhook handler that rejects an invalid signature, ignores a duplicate event safely and logs a bounded error if the database is unavailable. Add independent rate and size limits.',[
 ('How do signature verification and replay protection differ?','A signature checks the event content/origin under a signing scheme. Replay protection prevents a previously valid event from causing a duplicate or invalid business effect.'),
 ('Why limit output and concurrency as well as request count?','One request can consume excessive memory, CPU or storage. Different resource dimensions need independent bounds and recovery behaviour.')],
 ('Which should an invalid webhook signature cause?',['No business side effect and a clear rejection','A paid flag update before verification','An unlimited retry loop','A success response with a hidden failure'],0,'Verification must precede the protected business transition.'),skills=[193,194])
 lesson(c,'security-supply','Dependency trust, lockfiles and secure maintenance',r'''
## Dependencies become part of your application
A package can execute during installation/build or at runtime. Review why it is needed, its origin/maintenance and the authority it receives. A lockfile records resolved versions but does not prove that those versions are safe.

Use dependency audits and update tooling as inputs to a review process. Prioritise reachable risks and apply/test a suitable update. Avoid blindly disabling a finding or replacing an entire toolchain without understanding compatibility. Pin CI actions appropriately for the repository's trust policy and keep workflow permissions narrow.

## Build provenance matters
Know which reviewed source and dependencies produced a deployed artefact. Keep release metadata and verify the published path. Untrusted pull-request code should not receive deployment secrets simply because it runs inside a familiar CI platform.

## Maintenance is continuing work
Track runtime/framework support windows, model/provider deprecations and migration plans. Re-run meaningful tests after a dependency change and preserve a rollback path. A copied tutorial's old dependency versions are not automatically a suitable production baseline.

Keep source licenses/notices when bundling external code and distinguish original teaching content from imported reference modules. Secret scanning can catch selected patterns, but it does not replace reviewing changed files and rotating credentials if a leak occurs.
''','Create a dependency update checklist for a project: why the package exists, current risk, compatible version, relevant tests, license notices and deployment rollback.',[
 ('What does a lockfile guarantee and not guarantee?','It records a resolved dependency graph for reproducibility. It does not guarantee that every dependency is trustworthy, vulnerability-free or correctly configured.'),
 ('Why restrict CI secrets on untrusted changes?','Build/test code can execute commands and read its environment. Giving unreviewed code privileged secrets can turn a routine pull-request check into credential exposure.')],
 ('Which is a useful dependency-update outcome?',['A reviewed compatible update with relevant tests and a rollback path','Ignoring every audit permanently','Publishing all CI secrets for debugging','Assuming a familiar package name proves its integrity'],0,'Maintenance needs evidence of compatibility and controlled deployment, not only a version-number change.'),skills=[195])
