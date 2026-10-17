from pathlib import Path
import json
from .common import course,lesson

def build():
 c=course('projects','Project Architecture','Build and explain','Connect the skills into a portal or storefront and explain the actual trade-offs with evidence.','Build incrementally alongside the courses','Deliver a small tested vertical slice, then add permissions, payments, background work and an operational runbook.',['react','next','node','postgres','mongo','owasp'])
 lesson(c,'project-portal','Design a multi-tenant client portal',r'''
## Begin with one vertical slice
A portal connects an agency/team to clients, projects, tasks and invoices. Start with one authenticated user creating and reading one tenant-scoped project through UI, API and database. Verify the full path before adding a Kanban board, charts or AI summaries.

## Model the permissions
Write an admin/member/client matrix. Associate resources with reliable tenant/relationship data and enforce it in every query, export, upload and realtime room. A protected route in React improves navigation but cannot replace a backend access check.

## Add capabilities by boundary
React/Vite can build an interactive dashboard; Router handles client navigation; a state/context policy owns session/UI state. Recharts can display labelled metrics and dnd-kit can support accessible task moves. Node/Express and PostgreSQL/Prisma are one suitable implementation family, with validated inputs and migration evidence.

Payments require server-authoritative amounts, verified/idempotent provider events and transaction-time invoice snapshots. Notifications should not decide whether the core task change succeeded. A report job needs a durable period identity and a deterministic fallback if the chosen model provider fails.

## Interview with proof
The supplied project references disagree on some provider/testing details. Treat them as study prompts, not verified claims about a shipped repository. Before naming Claude/Groq, Jest/Vitest or an integration on a resume, check the actual dependency/configuration, code path and test evidence in that project.
''','Build a project creation slice and write its permission tests. Then prepare a two-minute explanation of one real schema/permission decision, citing the actual code/test rather than a planned feature.',[
 ('How does a client avoid seeing another client\'s data?','Verified identity must constrain the actual object/data access across API queries, exports, storage, search and realtime delivery. Test a cross-tenant request through the full boundary instead of relying only on hidden UI.'),
 ('What if the model provider is down?','The optional summary should degrade to a clear deterministic result based on validated task facts while the core portal remains usable. Preserve bounded retries and safe operational evidence.')],
 ('Which is a defensible project interview claim?',['A feature you can trace through actual code and tests','Every optional service named in an old plan','An invented traffic number','A tool listed only because it is popular'],0,'A project claim should be supported by the actual implementation and evidence.'))
 lesson(c,'project-commerce','Design a storefront, inventory and order workflow',r'''
## Separate browsing from transaction authority
A public storefront benefits from discoverable product pages and clear loading/error states. Next.js can support pre-rendered/server-rendered routes, while a client cart provides interaction. The backend remains authoritative for product availability, prices, discounts, tax calculations and final order state.

## Choose data by access patterns
Products with varying specifications may suit document modelling; relations and invariants still need explicit design. Index filtering/sorting fields, paginate large collections and avoid loading every product into one response. Redis/CDN caches need freshness and tenant/public scope rules.

## Preserve the transaction
Validate the cart against current server data, reserve/decrement stock atomically under a defined policy and create an immutable order snapshot. Track pending, paid, fulfilled, cancelled and refunded transitions deliberately. A frontend success callback is not a paid-state authority; verified provider events and reconciliation are required.

Record base amounts, discounts, applicable tax amounts and totals using a deliberate money/rounding contract. Keep historical invoice/order values stable when current catalog data changes. Address/pincode serviceability and configurable branding are separate validated business features, not reasons to accept arbitrary admin payloads.

One API can serve web and mobile clients with explicit versioned contracts. Authentication, permissions and rate limits apply equally to each client. Test the last-item race, duplicate payment event, failed notification and a mobile client using an older compatible contract.
''','Draw checkout from validated cart to payment event to fulfilment. Specify atomic stock handling, snapshot fields, duplicate events and a stale-cache scenario.',[
 ('How do you stop the last item being sold twice?','Enforce sufficient stock in an atomic database update or suitable transaction/reservation design, then check its result. A prior read or disabled frontend button cannot arbitrate concurrent buyers.'),
 ('Why use server rendering for some storefront routes?','Public product routes may benefit from pre-rendered discoverable content and a controlled caching strategy. A private dashboard can have different requirements; choose per route and verify actual freshness/performance.')],
 ('What must an order snapshot preserve?',['The relevant transaction-time item/pricing/address values','Only a pointer to mutable current product details','Only the cart button colour','An unverified paid flag from the browser'],0,'Historical records must remain meaningful after the current catalog changes.'))
 lesson(c,'project-interview','Architecture comparisons, testing evidence and scaling',r'''
## Compare from requirements
PERN/MERN labels name some technologies, not the full architecture. Explain why a relational schema fits one set of relationships/transactions and why document modelling fits a particular flexible catalog. State the trade-offs, not that one database is universally superior.

## A useful interview answer
Start with the concrete user problem, identify the chosen boundary/invariant, explain the implementation and show the evidence. For a webhook, describe raw-body signature verification, duplicate event handling and a negative test. For tenant isolation, show the query condition and a cross-account test.

## Scale the measured bottleneck
If traffic grows tenfold, inspect latency breakdown, query plans, cache hit/miss behaviour, connections, queue age and provider quotas. Possible responses include better indexes, pagination, bounded jobs, a correctly scoped cache and horizontal capacity. Do not promise sharding or microservices before identifying the limit.

Document failure behaviour: invalid input, denied permission, provider outage, a retried request and a cancelled job. Include deployment/migration/restore evidence and a clear list of remaining limitations.

Prepare short answers, then expect a deeper follow-up. A two-sentence explanation that you can expand with a trace/test is stronger than reciting a long list of packages. Keep resume/project claims aligned with the actual repository and release.
''','Prepare answers for database choice, tenant isolation, stock concurrency, provider failure, token storage and tenfold traffic. For each, identify one concrete code/test/measurement you would show.',[
 ('What would you change first for ten times the traffic?','Measure the actual saturation and latency path first. Optimise the demonstrated query, connection, queue or provider bottleneck with a testable change rather than choosing a fashionable architecture blindly.'),
 ('How do you explain a technology you planned but did not ship?','Call it planned/optional and distinguish it from implemented work. Explain the design if relevant, but do not claim operational or testing evidence that does not exist.')],
 ('Which answer best demonstrates engineering judgement?',['A measured bottleneck, chosen fix and validation','A list of every popular technology','A claim that microservices solve all load','An invented production user count'],0,'Requirements, trade-offs and evidence support a useful architecture explanation.'))

 c=course('placement','Placement Notes','Interview and exam foundations','Combine formulas, reasoning methods, verbal evidence and CS/output questions with deliberate review.','Daily short sessions alongside DSA','Use the dashboard, revise due mistakes and compare topic accuracy/time after each short mock.',['dsa','python','postgres','mdn'])
 lessons=[
 ('placement-quant','Quantitative aptitude & data interpretation',['Quant','DataInterpretation'],r'''
## Build a method before a timer
Translate the question into units and a known relationship. For percentages, keep the reference base explicit; successive changes multiply factors. For ratios, use a common scale. For work, add rates rather than completion times. For speed, convert units before comparing journeys.

Simple interest uses principal, annual rate and time under its stated convention; compound growth multiplies period factors. Profit percentage and discount percentage can use different bases. In mixtures, conserve the actual quantity being mixed. For probability, define the sample space and independence assumptions.

## Read a dataset carefully
Identify the population, period and units before calculation. A bar height, table count and percentage share are different quantities. Use the correct denominator for growth/share and compare absolute versus relative change. Do not average percentages from differently sized groups without the appropriate weighting.

## A practical routine
Read the worked example below, cover its answer and solve it again. Check a boundary or alternative method, then take a topic drill. After a mock, review incorrect and unanswered items and the active time spent on them. Reducing time is useful only while preserving a meaningful accuracy level.

The topic reference below includes the app's bundled formulas, notes, traps and worked examples, so you can study them here without opening another website.
'''),
 ('placement-reasoning','Logical and diagram-based reasoning',['Logical'],r'''
## Separate evidence from assumption
Represent the given relationships explicitly before choosing an answer. In a syllogism, all/none/some statements have different logical strength, and existence must not be invented. In arrangements, track fixed positions, adjacency, direction and exclusion constraints separately.

## Trace a pattern with a rule
For a number/shape sequence, describe the change at every step and test that one rule explains all shown terms. Rotation, reflection, count and fill can be independent dimensions. A plausible next picture is insufficient if it ignores a second changing feature.

For blood relations and directions, choose a consistent reference and draw a small labelled structure. For coding/decoding, test the transform across every provided example instead of matching one coincidence. In data sufficiency, judge whether the statements determine one answer under the exact combination rules; do not solve a different question.

## Review usefully
Record the assumption that caused a mistake and rewrite the valid inference. Use the answer palette to mark a difficult item, move on deliberately and return when time allows. A marked answer still counts if selected; an unanswered item contributes no correct answer.

The reference below includes topic-specific rules and examples, including the original diagram questions added for this upgrade.
'''),
 ('placement-verbal','Verbal ability and reading comprehension',['Verbal'],r'''
## Read for a supported claim
Identify the passage's main point, evidence and limits. Distinguish a directly stated fact, a necessary inference and a plausible outside assumption. Choose an answer supported by this passage rather than by personal knowledge about the subject.

## Grammar is a relationship
Check subject/verb agreement, tense sequence, pronoun reference, modifiers and parallel structure in context. A familiar phrase can still be wrong for the sentence's intended meaning. For vocabulary, use surrounding evidence and note the tone rather than assuming every synonym is interchangeable.

For sentence ordering, look for an introduction, references that need an earlier noun, logical connectors and a conclusion. For concise writing, preserve meaning while removing redundancy; do not remove a qualification that changes the claim.

## A timed passage routine
Read the question, locate the relevant paragraph, state the evidence in your own words and eliminate choices that exaggerate, reverse or go beyond it. Main-idea and inference questions may require the whole passage, not one isolated keyword.

After review, write why the distractor was tempting and which exact phrase/relationship rejects it. This develops a reusable reading method more effectively than memorising an answer letter. Worked topic notes and passage questions are bundled below.
'''),
 ('placement-cs','CS awareness and coding-output reasoning',['GeneralAwareness','Coding'],r'''
## Explain execution and invariants
For an output question, trace state in the language actually named. Operator precedence, scope, mutation and async ordering can differ between languages. Do not use a Python rule to answer a JavaScript question or assume every database has identical transaction behaviour.

CS interview preparation connects SQL/DBMS, OS, networks and OOP to a concrete system. Explain a transaction through a payment/stock example, a deadlock through a lock order and a cache through a freshness/access policy. The separate courses provide deeper notes; this reference supports short written drills.

## Awareness has a dated scope
Static science, geography, civics and history practice is different from current affairs. This app's static bank does not automatically update itself with every exam's current-affairs syllabus. A practice profile is not a guarantee of a future company's official pattern.

## Review a wrong option
State the language/database/version assumption, trace a minimal example and identify why each distractor fails. If a question is ambiguous, fix the wording or add the missing assumption rather than pretending the answer is universal.

Use the following topic rules and worked examples for revision, then a short mixed drill and an interview explanation of one related project decision.
''')]
 raw=(Path(__file__).resolve().parents[2]/'assets/practice-data.js').read_text(encoding='utf-8')
 bank=json.loads(raw.removeprefix('window.CODELAB_PRACTICE=').rstrip(';\n'))
 for id,title,sections,intro in lessons:
    topics=[t for t in bank['topics'] if t['section'] in sections]
    body=intro+'\n\n## Bundled topic reference\n'
    interviews=[('How should I review a wrong answer in this subject?','State the relevant rule and its assumptions, solve the example without looking, identify why the chosen distractor fails and schedule a focused review instead of memorising an option letter.'),('How should speed and accuracy be balanced?','Begin with a correct method and explicit units/assumptions. Use measured short drills to reduce avoidable time while preserving accuracy, then review skipped and incorrect items by topic.')]
    for t in topics:
        q=t['example'];context=q.get('passage','');v=q.get('visual',{});context+='\n'+(v.get('alt') or v.get('title',''));context+='\n'+('; '.join(f'{k}: {x}' for k,x in zip(v.get('labels',[]),v.get('values',[]))) if v.get('type')=='bar' else '\n'.join(' | '.join(map(str,row)) for row in [v.get('columns',[])]+v.get('rows',[])) if v.get('type')=='table' else '');body+=f'\n{context}\n';body+=f'\n### {t["title"]}\n\n**Formula / rule:** `{t["formula"]}`\n\n{t["notes"]}\n\n**Shortcut:** {t["trick"]}\n\n**Common trap:** {t["trap"]}\n\n**Worked example:** {q["q"]}\n\n**Answer:** {q["options"][q["answer"]]}\n\n{q["explanation"]}\n'
        interviews.extend([(f'Explain the method for {t["title"]}.',f'{t["formula"]}. {t["notes"]} Common trap: {t["trap"]}'),(q['q'],f'The answer is {q["options"][q["answer"]]}. {q["explanation"]} Method: {t["formula"]}. Check: {t["trap"]}')])
    lesson(c,id,title,body,'Choose two topics below. Solve each worked example with the answer covered, explain the trap and then complete a short focused practice set.',interviews,('Which is the strongest review habit?',['Explain the method and why the distractor fails','Memorise only the option letter','Ignore units and assumptions','Reduce time even when accuracy collapses'],0,'A reusable explanation exposes the underlying mistake and transfers to new questions.'),minutes=max(20,len(topics)*5))
