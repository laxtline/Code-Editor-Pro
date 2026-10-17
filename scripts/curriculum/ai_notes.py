from .common import course,lesson

def build():
 c=course('ai-foundations','AI & Model APIs','AI engineering','Use models as measured components with explicit input, output, cost and fallback contracts.','3-4 weeks after Python and APIs','Build a report generator with validated output, a deterministic fallback and a small evaluation dataset.',['claude','sklearn','numpy'])
 lesson(c,'ai-ml','AI, learning paradigms and a baseline model',r'''
## Put the terms in a useful hierarchy
Artificial intelligence is a broad field of computational systems performing tasks associated with intelligent behaviour. Machine learning fits patterns from data; deep learning uses multilayer neural models. Generative models produce outputs such as text or images. An application calling a model API is not thereby training a new model.

Supervised learning uses labelled examples; unsupervised learning seeks structure without the same explicit target labels. Self-supervised learning creates prediction signals from data itself. Reinforcement learning concerns actions and reward feedback through an environment. These are learning setups, not promises of accuracy.

## Training and inference
Training adjusts parameters using data and an objective. Inference uses a trained model to produce an output. A neural network can be understood as parameterised transformations whose loss guides updates; gradient-based optimisation changes weights to reduce an objective, not to guarantee that every generated statement is true.

## Generalise, do not memorise the test
Separate training, validation and held-out test data according to the real deployment setting. For time-dependent or grouped data, a random row split can leak future or related information. Fit preprocessing only on the appropriate training data. Repeatedly tuning against the test set makes it part of the training process in practice.

Start a product problem with a deterministic rule or simple classical ML baseline. If a labelled classifier and a few well-chosen features solve the problem reliably, an LLM may add unnecessary cost and unpredictability. Compare on the same representative held-out cases.
''','Define a ticket-priority problem, a deterministic baseline and a possible supervised model. Specify labels, split strategy, leakage risks and the decision threshold used by the product.',[
 ('What is overfitting?','A model performs well on the patterns/noise of its training data but fails to generalise to new relevant examples. Evaluate on a properly separated dataset that matches the deployment setting.'),
 ('Why build a simple baseline before an LLM feature?','It establishes whether the added complexity improves a real outcome. A cheaper deterministic or classical model can be easier to test, explain and operate for a bounded classification task.')],
 ('Which is data leakage?',['Using future outcome information as a training feature','Holding out a test set correctly','Fitting preprocessing only on training data','Measuring a simple baseline'],0,'The model receives information that would not be available at the real decision time.'),skills=[196,197,198,199,201])
 lesson(c,'ai-metrics','Confusion matrices, precision, recall and a scikit-learn pipeline',r'''
## Count the errors that matter
For a binary positive class, true positives are correctly flagged positives, false positives are incorrect flags and false negatives are missed positives. Precision = TP/(TP+FP); recall = TP/(TP+FN). F1 is the harmonic mean of precision and recall when defined. Specify a policy for zero denominators rather than hiding undefined cases.

Accuracy can mislead with an imbalanced class. If only one in a hundred events is positive, a system predicting negative for everything has high accuracy and zero positive recall. Choose metrics and thresholds based on the cost of misses versus false alarms.

## A reproducible classical pipeline
In a local scikit-learn project, split data appropriately, combine preprocessing and estimator in a Pipeline, fit on training data, choose parameters/threshold using validation and report the held-out results. Use suitable cross-validation for the data structure. Keep feature construction, label definition and dataset version explicit.

Inspect error examples, not only one aggregate score. Report per-group or per-category coverage where relevant and verify that a model did not exploit a leaking identifier. Compare with the same baseline and test population.

The runnable example computes metrics with the standard library. scikit-learn itself is a separate local project dependency and is not downloaded by this offline lesson.
''','For TP=12, FP=3 and FN=8, calculate precision, recall and F1. Then choose which metric matters most for a support escalation feature and explain the trade-off.',[
 ('Why can accuracy be misleading?','A dominant negative class can make an always-negative classifier appear accurate while missing every useful positive. Inspect class-specific precision/recall and the real costs of mistakes.'),
 ('Why put preprocessing inside a training pipeline?','It keeps transformations fitted on the correct training folds and applied consistently to new data, reducing leakage and mismatched train/inference processing.')],
 ('With TP=8 and FP=2, what is precision?',['0.8','0.2','4','10'],0,'Precision is TP/(TP+FP), so 8/(8+2)=0.8: eight of ten positive predictions are correct.'),
 ('python','tp, fp, fn = 12, 3, 8\nprecision = tp/(tp+fp)\nrecall = tp/(tp+fn)\nf1 = 2*precision*recall/(precision+recall)\nprint(round(precision, 3), round(recall, 3), round(f1, 3))','0.8 0.6 0.686'),skills=[200,202])
 lesson(c,'ai-llms','Tokens, attention, generation and embeddings',r'''
## Tokens are a model-specific unit
A tokenizer splits input/output into units used by a model. Token count affects context capacity, latency and billing under the provider's contract; it is not always equal to word or character count. The context window is a bounded working input/output budget, not an unlimited reliable memory.

Transformers use attention to combine information from token representations according to learned relationships. Pretraining builds broad predictive capabilities; instruction tuning and preference-based methods shape assistant behaviour. These processes do not turn generated text into a verified database lookup.

## Generation is conditional prediction
Sampling controls such as temperature/top-p influence output selection. Lower randomness does not guarantee truth or perfect repeatability across providers, model revisions and infrastructure. Models can hallucinate, reflect stale knowledge or respond sensitively to prompt wording. Evaluate the actual task instead of treating confidence in wording as evidence.

## Embeddings are vectors
An embedding maps input to a numeric representation useful for a chosen similarity task. Compare compatible vectors from the same intended model/space and dimension. Cosine similarity measures direction after accounting for magnitude; a dot product has different behaviour unless normalisation makes them equivalent for ranking.

An embedding similarity is not a probability that a statement is correct. Keep text, metadata and source identifiers so retrieval can return inspectable evidence instead of only a score.
''','Compute cosine similarity for two small vectors and explain what a high score can and cannot prove. Design a context budget for a report that includes instructions, data and an output allowance.',[
 ('Does temperature zero guarantee factual correctness?','No. It changes sampling behaviour, not whether the model has reliable evidence. Validate outputs and use grounded retrieval or deterministic logic where correctness requires it.'),
 ('Why must embedding model/dimension be tracked?','Vectors from incompatible spaces cannot be meaningfully mixed just because they are arrays. Indexes, stored vectors and query embeddings need a compatible representation and migration policy.')],
 ('What does a high embedding similarity establish?',['Similarity under that representation/metric','Guaranteed factual truth','Permission to reveal the document','A valid payment'],0,'Similarity is a retrieval signal, not truth, authority or access control.'),
 ('python','import math\na, b = [1, 0, 1], [1, 1, 0]\ndot = sum(x*y for x,y in zip(a,b))\nscore = dot/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(y*y for y in b)))\nprint(round(score, 3))','0.5'),skills=[203,204,205,206,207,208])
 lesson(c,'ai-providers','Model selection, local models and a provider interface',r'''
## Select against the task
Compare candidate models using a representative evaluation set, latency distribution, output constraints and total cost. A small model may be sufficient for classification, while a harder synthesis task may justify a stronger model. Brand or size alone is not a task evaluation.

Open-weight models can run locally through tools such as Ollama when hardware, model size and licensing permit. Downloaded weights, memory requirements and capabilities are separate from this site's bundled Python engine. This app does not silently include a full local LLM.

## Put a narrow interface around providers
Define an internal operation such as generate_report(input, budget) returning validated output plus usage/status metadata. Keep provider-specific message formats, retries and credentials inside an adapter. A thin abstraction is easier to maintain than pretending every model/provider has identical features.

Claude/Groq and other services can differ in supported modalities, structured output and streaming/tool semantics. Keep API keys on the server. For images/documents, validate type/size and privacy policy before sending data outside the system; a model accepting a file does not imply the user intended every private file to leave.

## Preserve a deterministic path
If generation fails or validation rejects the output, return a clearly labelled template based on verified counts. Keep the rest of the product working and record the provider failure safely. Do not quietly invent a successful model response.
''','Design a provider-neutral report interface with a timeout, validated result, usage metadata and a fallback. Explain how you would compare a local model and an external API on the same cases.',[
 ('What should a provider abstraction hide?','Transport/message details and provider-specific integration should be localised. It should not hide meaningful capability limits, cost, errors or validation evidence from the product.'),
 ('Does local inference automatically make a feature private and safe?','It can reduce external data transfer, but local storage, logs, permissions, model licensing and tool access still need a deliberate design.')],
 ('Where should a paid model API key be stored?',['In protected server-side configuration','In a public React environment variable','In a GitHub Pages HTML file','Inside a query parameter shared with users'],0,'A static/browser bundle is public to its users and cannot keep a server secret.'),skills=[209,210,211,212,219,220])
 lesson(c,'ai-prompts','Prompt structure, schemas and prompt versioning',r'''
## A prompt is an input contract
State the task, relevant context, constraints and expected output. Give examples when they clarify edge cases, and delimit data so the model can distinguish it from instructions. Do not assume that a retrieved document or user-supplied text is trusted control logic.

## Ask for a verifiable result
For a report, specify fields such as status, completed_count and evidence_ids. Use structured-output/schema support where available, then parse and validate the result at runtime. A syntactically valid JSON object can still contain incorrect values, nonexistent references or an impermissible action.

Decide how to handle invalid output: reject, apply a bounded repair attempt or use a deterministic fallback. Do not loop indefinitely asking the same model to fix itself. Keep the original input/output and error category only within the permitted privacy/logging policy.

## Change prompts like code
Store a versioned template with the model/configuration and evaluation results. Review changes against a golden set containing ordinary, edge and adversarial cases. A prompt that improves a few demonstrations can regress important categories silently.

Keep instructions specific without demanding unsupported certainty. If evidence is insufficient, the output should say so. Let deterministic code compute totals and enforce permissions; reserve the model for the part that benefits from language interpretation or generation.
''','Write a project-report prompt whose numeric totals come from code and whose narrative cites task IDs. Define its output schema, validation rules and failure fallback.',[
 ('Why validate after requesting JSON?','Formatting constraints do not prove field values, reference IDs or business rules are correct. Runtime checks must verify the actual output before the application relies on it.'),
 ('Why version prompts?','Prompt changes can alter behaviour like code changes. Versioning connects a deployed result to its template/model and allows comparison, regression testing and rollback.')],
 ('Which fact should deterministic code compute when possible?',['The exact count of completed tasks','A fabricated source citation','A guessed payment state','An unverified account owner'],0,'Exact structured facts should come from authoritative data and validated computation.'),
 ('python','import json\ndef valid_report(text, total):\n    data = json.loads(text)\n    if set(data) != {"completed", "summary"}:\n        raise ValueError("unexpected fields")\n    if type(data["completed"]) is not int or not 0 <= data["completed"] <= total:\n        raise ValueError("invalid completed count")\n    if not isinstance(data["summary"], str):\n        raise ValueError("summary must be text")\n    return data\nprint(valid_report(\'{"completed":2,"summary":"Two tasks finished."}\', 3))',"{'completed': 2, 'summary': 'Two tasks finished.'}"),skills=[213,215,217])
 lesson(c,'ai-streaming','Streaming, token budgets and cancellation',r'''
## Stream an operation, not an illusion of success
A provider can emit incremental events/tokens. The server forwards an appropriate stream and the browser decodes/fragments it into a visible partial result. Show whether the answer is still generating, complete, stopped or failed. Receiving some text is not proof that a required structured result completed successfully.

## A budget spans the whole operation
Count prompt/context input and reserved output separately. Set maximum output, request deadline and per-tenant usage controls. Provider pricing and caching rules vary, so use current configuration/usage data instead of a permanent price copied from a tutorial.

Prompt caching can help repeated supported input, but cache identity and privacy scope matter. Trimming context should preserve the task's necessary evidence, not arbitrarily discard the most inconvenient source. The smallest model that passes the task evaluation can be a good cost/latency choice.

## Cancel through every boundary
When the user stops, propagate abort/disconnect to the server/provider where supported and close resources. Preserve useful partial output with a stopped/partial label instead of claiming it is a final verified answer. Handle slow readers and proxy buffering with bounded queues.

Measure time to first useful output and time to a validated final result separately. A fast first token can coexist with a slow, expensive or ultimately invalid operation.
''','Design a streaming report UI with Stop, partial-output preservation and a final validation step. Allocate a context/output budget and name the usage/cancellation signals to record.',[
 ('Why measure more than time to first token?','The user needs a useful and ultimately valid result. A fast opening token can hide long completion latency, high cost or a failed structured output.'),
 ('What should a stopped stream display?','The retained partial content should be clearly labelled stopped/incomplete. The backend should cancel remaining work where possible and release resources.')],
 ('Which is an appropriate final success condition?',['The required complete output passed validation','One token arrived','A spinner appeared','The provider returned any bytes'],0,'A complete validated outcome is different from the first partial stream event.'),skills=[214,218])
 lesson(c,'ai-coding','AI-assisted coding with specs, tests and review',r'''
## Make the task reviewable
Give a coding assistant the repository context, intended behaviour, constraints and acceptance criteria. Ask for a small coherent change and identify the relevant validation path. A vague request to make everything perfect provides little basis for reviewing the result.

## Review generated code as code
Read the diff, trace data ownership and trust boundaries, and test explicit cases. Look for plausible but nonexistent APIs, missing error paths, unbounded work, data loss and secret exposure. A confident explanation is not evidence that the implementation ran.

Use tests to encode a real contract, not to repeat every implementation detail. Preserve a failing regression case when a bug is found. Check the actual built/deployed artefact where packaging or runtime behaviour matters.

## Know when to constrain authority
Security-sensitive logic, payment transitions, authentication and destructive data changes need careful human review and established components. Do not paste secrets or private data into a tool without an appropriate data-sharing decision. Respect source licenses when importing code.

AI can help plan, explain, refactor and diagnose, but the engineer remains responsible for the final system's behaviour and evidence. A useful portfolio describes what was built, why the trade-offs were chosen and which checks actually passed, without inventing usage numbers or project features.
''','Write acceptance criteria for autosaving a study note across reload and a storage quota failure. Review a hypothetical assistant change that catches every error and still displays Saved.',[
 ('Why can generated tests still miss the bug?','They may encode the same mistaken assumption as the generated implementation. Use explicit expected outcomes, independent examples and boundary cases tied to the user requirement.'),
 ('What evidence should accompany a coding change?','A focused diff, the resulting behaviour, relevant tests/checks and meaningful limitations. For packaging/deployment changes, verify the actual produced or live artefact too.')],
 ('Which is strongest evidence that autosave works?',['A draft survives an immediate reload and a meaningful failure case is handled','A comment says autosave is robust','The button is green','The assistant sounds confident'],0,'Observable behaviour and failure handling are evidence; presentation alone is not.'),skills=[221,222,223,224])

 c=course('rag','Retrieval & Evaluation','AI engineering','Build source-grounded answers and measure retrieval and output quality before expanding features.','3-4 weeks after model API basics','Build a small private-document search/report pipeline with citations, access filters and a versioned evaluation set.',['rag','postgres','claude','sklearn'])
 lesson(c,'rag-ingestion','Ingest, clean, chunk and retain source metadata',r'''
## Retrieval starts before the model call
A basic RAG pipeline ingests documents, extracts/cleans text, creates chunks, embeds/indexes them, retrieves candidates, optionally reranks, assembles context and generates a source-grounded answer. A failure in extraction or permissions cannot be repaired just by choosing a larger generation model.

## Keep provenance
For PDFs, HTML and office files, preserve document ID, version, page/section, tenant/access metadata and extraction status. Tables and multi-column layouts need inspection: plain text extraction can scramble relationships. Keep a recoverable source link rather than storing only an anonymous paragraph.

## Chunk by meaning
Prefer a structure-aware boundary such as a section, paragraph or coherent table region. Token size and overlap trade context continuity against duplication and retrieval precision. Very small chunks can lose meaning; very large ones can waste context or mix unrelated subjects. Evaluate actual questions rather than declaring one universal chunk size.

Normalise obvious extraction noise without destroying important headings, units or qualifiers. Treat embedded instructions in documents as data, not instructions for an agent. Reject or flag unreadable sources rather than silently pretending they were indexed correctly.

Build a small inspection tool that shows retrieved chunks beside their original location. It is often easier to improve answers by fixing a broken source/chunk than by adding another layer of prompt text.
''','Design ingestion records for a PDF with tables and a DOCX with headings. Specify chunk IDs, source locators, tenant metadata and how you detect an extraction failure.',[
 ('Why keep page/section metadata?','It supports verifiable citations, debugging and updates. A user and evaluator need to trace an answer back to the relevant source rather than trusting an anonymous retrieved string.'),
 ('Why is there no universal best chunk size?','Documents and tasks differ in structure, evidence length and query granularity. Size/overlap must be evaluated against actual retrieval and answer outcomes.')],
 ('Which ingestion output is most useful?',['Text plus source/version/location/access metadata','Only a vector with no source ID','Only a filename with no content','A claim that every PDF parsed perfectly'],0,'Retrieval, updates, permissions and citations all need provenance.'),skills=[225,226,227])
 lesson(c,'rag-search','Vector indexes, hybrid search and reranking',r'''
## Retrieve candidates under a representation
A vector database/index stores embeddings with metadata and supports a similarity query. pgvector can fit a PostgreSQL-centred application; other systems may fit different scale/operation needs. Use the same compatible embedding representation for indexed and query vectors.

Cosine, dot product and distance metrics have different meanings and normalisation assumptions. Approximate nearest-neighbour indexes trade recall, latency and resource use. HNSW uses a graph-based search structure; IVF partitions candidate space and searches selected partitions. Index parameters and data distribution affect the actual result.

## Lexical and semantic signals complement each other
Keyword ranking such as BM25 can match exact identifiers or rare terms; embeddings can match related meanings. Hybrid search combines signals/ranks. Raw scores from unrelated systems are not automatically comparable; a rank-fusion method or calibrated combination is more deliberate than simply adding arbitrary numbers.

A reranker can examine query/candidate pairs more deeply and reorder a smaller candidate set. It adds latency and cost, so measure the gained quality per operation. Keep the candidate stage broad enough that the right passage can reach the reranker.

Evaluate recall and latency with real filters and permissions enabled. A benchmark over public unfiltered documents does not prove that private tenant-scoped queries work correctly.
''','Compare keyword, vector and hybrid retrieval for an exact invoice number and a conceptual help question. Define candidate count, reranking budget and the recall/latency measurements.',[
 ('Why might keyword search beat embeddings for an identifier?','An exact rare code or invoice number is a strong lexical signal. Semantic similarity can blur those distinctions, so hybrid or exact matching may be important.'),
 ('Can a reranker recover a passage never retrieved?','Not if it only sees the candidate set. Candidate recall constrains later ranking, so inspect retrieval failures before tuning a final generation prompt.')],
 ('What is an approximate vector index trade-off?',['Recall versus latency/resource use','Permission checking versus no permission checking','Truth versus a guaranteed false answer','Only text colour'],0,'Approximate search parameters affect which neighbours are found and the work required.'),skills=[228,229,230,231])
 lesson(c,'rag-grounding','Context assembly, citations and access-aware retrieval',r'''
## Context is a bounded evidence set
Choose relevant passages, preserve their source identifiers and fit them into the token budget with enough surrounding meaning. Duplicated or contradictory chunks waste space and can confuse the output. Ordering can affect whether important evidence is used, so test the actual assembly policy.

## Ground claims in inspectable sources
Ask the system to cite source IDs/locations that exist in the retrieved context. Validate those references and check that the cited passage actually supports the claim. A syntactically valid citation can still be irrelevant. When evidence is missing, the answer should say so rather than invent a source.

## Apply permissions before exposure
Retrieval must use the caller's permitted tenant/documents and enforce access in the actual data path. Filtering only the final answer is too late if private text was already sent to a provider or logged. Cache keys, reranker inputs and context assembly must preserve the same access scope.

Use a stable public reference format rather than leaking an internal filesystem path unnecessarily. Document redaction and provider-data handling belong to the system design, not to a hopeful prompt line saying keep it private.

Test with two tenants containing similar document titles and with a question that has no supported answer. Verify both the retrieval set and the generated output; a correct-looking answer can conceal an access leak in the context.
''','Design an answer record with text, evidence IDs and an insufficient-evidence status. Add a cross-tenant retrieval test and a citation-support test.',[
 ('Why is filtering only the final answer insufficient?','Private content may already have reached retrieval logs, a reranker or an external model. Access scope must be enforced before those exposures, not only at display time.'),
 ('Does a valid-looking citation prove support?','No. The reference may exist but not support the associated claim. Validate both source identity and the relationship between the passage and the claim.')],
 ('When should document access filtering happen?',['Before private content is retrieved/exposed downstream','Only after the model writes an answer','Only when a user complains','Only in a CSS rule'],0,'Permissions must protect the actual retrieval and downstream data path.'),skills=[232,233,234])
 lesson(c,'rag-freshness','Index updates, query rewriting and advanced trade-offs',r'''
## An index has a version and freshness policy
When a source changes, identify affected chunks, remove stale ones and index the new version. A deleted or access-revoked document must stop being retrievable according to the product's policy. Changing embedding models can require re-embedding and a new compatible index; do not mix dimensions/spaces accidentally.

## Query transformation
Rewriting, expansion or decomposition can improve a difficult query, but it can also change intent or expose more data. Retain the original question and evaluate the transformed retrieval. Bound the number of subqueries and downstream calls.

## Choose extra machinery from evidence
Graph-based retrieval can help with explicit relationships; agentic retrieval can choose multiple search steps; long context can avoid some chunk selection for suitable bounded corpora. Each adds different costs, failure modes and access-control obligations. A long context window does not guarantee reliable use of every passage.

Measure the baseline first. If failure comes from stale documents, broken extraction or missing keywords, adding an agent loop may make the system slower without fixing the cause. Keep a rollback path to a simpler retrieval policy.

Track document, chunker, embedding model, index and prompt versions together. An answer should be diagnosable against the data/index state used at that time, within the allowed retention/privacy policy.
''','Design reindexing after a document edit, deletion and embedding-model switch. Compare a simple hybrid retriever with a multi-step agent for three representative questions.',[
 ('Why can an embedding-model change require reindexing?','The new representation can have a different dimension or semantic space. Query and stored vectors must remain compatible; version and migrate them deliberately.'),
 ('Why preserve the original query after rewriting?','It lets you detect intent drift and diagnose whether transformation improved retrieval or introduced a different question. The original user request remains the task boundary.')],
 ('What is the first fix for an answer based on a deleted document?',['Repair deletion/freshness propagation and access checks','Add more prompt adjectives only','Increase output temperature','Hide all source links'],0,'The underlying stale retrieval must be corrected rather than disguised.'),skills=[235,236,237])
 lesson(c,'eval-methods','Golden datasets, retrieval metrics and answer rubrics',r'''
## Define success before adding features
A golden dataset contains representative questions, expected evidence/outcome, edge cases and adversarial inputs. Version it and keep the held-out evaluation policy clear. A tiny set of impressive demos does not establish broad reliability.

## Retrieval and answer metrics differ
Recall@k asks what fraction of known relevant items appears in the top k. Precision@k asks what fraction of the top k is relevant under the chosen fixed-k convention. Reciprocal rank is 1/rank of the first relevant result, or zero if none; MRR averages that quantity across queries. These require relevance labels and do not directly measure whether a generated answer is faithful.

For answers, define faithfulness to evidence, relevance to the question and completeness of required points. Exact match fits strict outputs, while a rubric fits acceptable paraphrases. An LLM judge can help scale scoring but has biases, prompt sensitivity and potential disagreement with humans.

## Inspect error categories
Separate missing evidence, poor ranking, unsupported claims, wrong arithmetic, invalid format and access leaks. A single average score can hide a catastrophic failure category. Use deterministic checks for schema, IDs and arithmetic whenever possible.

Compare versions on the same dataset and budgets. Report sample size and uncertainty rather than claiming that a perfect score on ten examples proves production correctness.
''','Create ten questions for a small document collection with relevance labels. Compute recall@3 and reciprocal rank for one query, then write a three-point answer-faithfulness rubric.',[
 ('Why separate retrieval recall from answer quality?','The retriever may find the right passage while the generator ignores or misstates it, or the generator may guess a correct answer without valid evidence. The stages need distinct diagnostics.'),
 ('What is a limitation of LLM-as-judge?','It can prefer style, share model biases, vary with prompts and disagree with humans. Calibrate it against labelled examples and use deterministic checks where possible.')],
 ('If the first relevant result is at rank 4, what is reciprocal rank?',['0.25','4','1','0.75'],0,'Reciprocal rank is 1 divided by the first relevant rank.'),
 ('python','relevant = {"b", "d"}\nretrieved = ["a", "b", "c"]\nrecall = len(set(retrieved) & relevant)/len(relevant)\nrr = next((1/(i+1) for i,item in enumerate(retrieved) if item in relevant), 0)\nprint(recall, rr)','0.5 0.5'),skills=[238,239,240,241,242])
 lesson(c,'eval-operations','Human review, regression gates and feedback loops',r'''
## Calibrate automated scores
Sample outputs for human review across ordinary, rare and high-risk categories. Use a written rubric, compare reviewer disagreement and revise ambiguous labels. A judge score is useful only when it correlates with the decisions the product actually needs.

## Put evaluations in the release path
Run a suitable fixed suite when prompts, models, retrieval/index policies or tool contracts change. Gate on important categories, not only an average. Keep cost/latency budgets beside quality thresholds, and investigate a regression before silently lowering a threshold.

## Learn from production carefully
User corrections, negative feedback and escalations can identify new cases. Validate them, protect private data and add representative examples to the dataset under a controlled process. Feedback volume is not automatically an unbiased quality measure because some users/categories report more than others.

Tools such as Langfuse, LangSmith, Ragas or promptfoo can help collect traces or run evaluation workflows. A small local harness can also be sufficient at first. Choose tooling after the dataset, rubric and release decision are clear.

Keep versioned records of prompts/models/indexes and the suite result associated with a release. When a model is deprecated or swapped, rerun the relevant suite and compare actual outcomes. A new model label does not establish that your application improved.
''','Define a CI gate with one access-leak must-pass category, a faithfulness threshold and a latency budget. Specify how one real user correction becomes a privacy-safe regression example.',[
 ('Why can an average quality gate be dangerous?','An improvement on easy cases can hide a severe regression on a small high-risk category. Keep category-specific requirements for failures such as data exposure or unsupported payment actions.'),
 ('When is a small evaluation harness enough?','When it can reproducibly run the representative cases, apply meaningful checks and support the release decision. Tooling should serve that contract rather than replace it.')],
 ('What should a model migration trigger?',['Re-run task-specific evaluations and compare budgets','Assume the newest label is always better','Delete all old failure cases','Disable access tests to save time'],0,'The application\'s real quality/cost/latency contract must be verified after a model change.'),skills=[243,244,245,246])

 c=course('agents','Agents & AI Products','AI engineering','Build bounded tool workflows, safe authority boundaries and observable user-facing AI features.','3-4 weeks after retrieval/evaluation','Build a read-only project assistant first, then add one validated action with review, audit and cancellation.',['claude','mcp','owasp'])
 lesson(c,'agent-loop','Workflows, tools, planning and memory',r'''
## A tool loop is an application protocol
The model proposes a tool call, deterministic code validates/executes an allowed operation and the result returns as data for the next step. The loop needs explicit completion, maximum steps, time and cost limits. A tool call string is not authority to execute any arbitrary command.

Use a fixed workflow when the required steps are known. An agent can be useful when selecting the next bounded step genuinely depends on intermediate results. More autonomy also increases the number of possible failure paths, so justify it against a simpler baseline.

## Design narrow tools
A get_project_summary tool is easier to validate and authorise than a generic run_anything tool. Define input schemas, output/error shapes and idempotency for side effects. Derive tenant/user context outside model-controlled arguments and enforce it during execution.

Conversation state, short summaries and long-term stores have different lifecycles. A summary can omit facts; a stored memory can become stale or contain untrusted content. Keep source/version/access metadata and let the user correct relevant state.

Planning can decompose a task and revise after a failure, but a plan remains a proposal bounded by the user request and tool permissions. Frameworks such as LangGraph or LlamaIndex can organise state, yet plain code may be simpler for a small controlled workflow.
''','Design a read-only project assistant with three tools, structured errors, a five-step limit and a final evidence-based answer. Compare it with a fixed report pipeline.',[
 ('When is a fixed workflow preferable to an agent?','When the steps and decision rules are already known. A deterministic pipeline is easier to test, bound and debug; use an agent when dynamic choice provides measurable value.'),
 ('Why make tools narrow?','A small contract reduces ambiguous inputs and excessive authority. It lets deterministic code validate permissions, resource limits and expected outcomes for each operation.')],
 ('Who must enforce a tool\'s tenant permission?',['The deterministic tool/server boundary','Only the model\'s polite wording','Only the frontend icon','An unverified tenant argument supplied by the model'],0,'Model-controlled arguments cannot establish authority over private data.'),skills=[216,247,248,249,250,254,255])
 lesson(c,'agent-mcp','MCP, human review and bounded authority',r'''
## Standardise the connection, not the permission decision
Model Context Protocol provides a standard way for clients/hosts to connect with tool/data capabilities through compatible servers. It can reduce custom integration work, but installing or discovering a server does not automatically authorise every action it exposes.

Review the server's origin, requested permissions, authentication and data flow. A tool description is a contract to inspect, not an instruction that outranks the user. Apply the same tenant/object controls as any other API and validate returned data.

## Separate preparation from consequence
A system can prepare a draft invoice, show the exact recipient/amount/content and require the appropriate human review before a consequential send/payment/deletion. The review should concern a concrete proposed action, not an abstract request to trust the agent forever.

## Bound the run
Set step/time/token limits, restrict accessible tools/resources and provide Stop. Side-effect tools need suitable isolation, idempotency and an audit trail. A kill switch must stop further actions, while already committed external effects require their own recovery process.

Use a read-only capability first and test adversarial tool results. Add write authority only when its validation, review and rollback/reconciliation policy are clear. A protocol's existence does not make arbitrary remote instructions or plugins safe.
''','Design a draft-and-review invoice workflow through a narrow tool interface. Specify what is shown for review, which permissions are checked and what Stop can and cannot undo.',[
 ('Does MCP make every connected tool trusted?','No. It standardises interaction, while trust, authentication, permissions and validation remain responsibilities of the host/application and server design.'),
 ('What should a useful approval screen show?','The exact consequential action, target, relevant content/amount and expected effect. A person needs a concrete reviewable proposal, not a vague request for unlimited future authority.')],
 ('Which is a meaningful agent run limit?',['A bounded step/time/cost budget with a stop path','An unlimited loop until the model feels finished','A hidden global credential','A claim that tools never fail'],0,'Explicit limits bound cost and side effects when a loop fails to converge.'),skills=[251,252,253])
 lesson(c,'agent-security','Prompt injection, SSRF, output safety and audits',r'''
## Tool outputs and documents are untrusted data
An attacker can place instructions in a webpage, retrieved file or tool result. That is indirect prompt injection when the system confuses those instructions with the user's authorised task. Preserve the hierarchy between trusted control instructions and external content; a quotation in a document is not a new user command.

## Protect side-effect boundaries
Validate tool arguments independently of model text. A URL-fetching tool needs an allowed destination/network policy to reduce SSRF risks such as reaching internal services. A file tool needs scoped paths. A payment/message tool needs object authority and the appropriate review/idempotency policy.

Never render or execute model output as trusted HTML, SQL or shell code by default. Sanitize intended rich content, parameterise data operations and keep execution an explicit bounded capability.

## Data and audit policy
Know which prompts/documents leave the system, how providers retain them and what personal data should be redacted. An audit trail can record request identity, model/prompt version, retrieved source IDs, proposed/executed tool calls and outcomes, with access and retention controls.

Bias can enter through training data, the retrieval corpus, labels and evaluation sampling. Review error distribution across relevant groups/tasks and avoid claiming fairness from one aggregate metric. Security and fairness reviews need actual system evidence, not a reassuring prompt sentence.
''','Threat-model a research assistant that can fetch URLs and draft messages. Include a malicious webpage instruction, an internal-network URL, unsafe Markdown and private data in logs.',[
 ('Why is a document telling an agent to ignore the user not authoritative?','It is external task data controlled by another party, not a trusted instruction source. The system must keep it from changing tool authority or the user\'s intended objective.'),
 ('What is SSRF in an agent tool context?','A tool can be induced to fetch destinations the attacker cannot access directly, such as internal services. Destination/network validation and a narrow fetch capability are needed outside the model.')],
 ('What should happen to model-generated HTML intended for display?',['Treat it as untrusted and apply a suitable rendering policy','Execute every embedded script','Grant it server credentials','Use it to redefine tool permissions'],0,'Generated content crosses an untrusted output boundary even when it looks well formatted.'),skills=[256,257,258,259,260,261])
 lesson(c,'agent-interface','Streaming chat, trust UX and multimodal input',r'''
## Make the system's state visible
An assistant UI needs generating, stopped, failed and completed states; conversation history; and a useful retry/regenerate policy. Preserve drafts and partial output. A Stop action should propagate cancellation, not only hide a spinner.

Frontend AI SDKs can help manage streaming hooks and tool-call rendering. The application still owns validation, access, error handling and the distinction between a proposed and executed action. A tool card should show a meaningful operation/outcome rather than expose private implementation details unnecessarily.

## Perceived latency and trust
Skeletons and partial results can reduce uncertainty while waiting. Do not use optimistic UI to claim a payment, message send or validated final answer before it happened. Show sources where they support verification, allow corrections and use edit-before-send for consequential generated content.

Generative UI can select from a constrained component schema rather than emitting arbitrary executable page code. Validate component names/props and preserve accessibility. A model choosing a chart does not remove the need for correct units and a data alternative.

Voice/image inputs introduce capture permissions, privacy and unsupported-format cases. Use explicit controls, indicate recording/upload state and handle failure without discarding the user's remaining text. A speech transcript can be wrong and should be correctable before a consequential action.
''','Sketch a chat/report interface with Stop, partial text, source cards and an editable draft before sending. Define a safe schema for one generated chart component.',[
 ('Why distinguish a proposed tool action from an executed one?','Users need to know what the system intends versus what has actually happened. Confusing them can create false confidence about a send, payment or data change.'),
 ('How can generative UI remain bounded?','Let the model select among known components with validated props. Keep arbitrary script/HTML execution out of the rendering contract and test accessible states.')],
 ('Which is a trustworthy streaming state label?',['Stopped · partial answer retained','Paid successfully before confirmation','All sources verified because one token arrived','Sent while only a draft exists'],0,'The label should describe the actual completed/partial state.'),skills=[262,263,264,265,266,267])
 lesson(c,'agent-production','Queues, fallback, per-tenant budgets and tracing',r'''
## Place AI where its latency fits
A quick bounded classification may fit a request; a long report may belong in a durable queue. Return a job ID and observable state when completion outlives the request. Define idempotency, cancellation and retry behaviour for each stage.

## Keep the non-AI product functional
If the model/provider is down, preserve core CRUD/payment/task workflows and offer a clear deterministic fallback for optional summaries. A fallback should not fabricate evidence or hide that a capability was reduced.

## Cost controls are resource controls
Limit input size, output tokens, concurrent jobs and per-tenant usage. Cache only under a correct permission/freshness key. Trim prompts deliberately and choose a smaller model when it passes the required evaluation, rather than changing models solely from a headline price.

## Trace the operation
Record safe metadata such as prompt/model/index version, tokens, stage latency, retries and outcome. Correlate browser request, queue job, retrieval and provider call. Apply redaction/retention rules so observability does not become a private-document archive by accident.

Test an outage, a slow reader, an over-budget tenant and a cancelled job. Observe whether queue age, resource use and recovery remain bounded. A healthy provider benchmark does not prove production behaviour when dependencies fail.
''','Define a queued weekly report with per-tenant limits, a deterministic outage response and a trace spanning retrieval/provider/output validation. State what metadata is logged and what content is excluded.',[
 ('Why separate a long report from the request path?','A durable job lifecycle can survive request timeouts and provide explicit progress/retry/cancellation. It avoids relying on a short-lived HTTP context to own lengthy work.'),
 ('What should AI observability avoid?','Unnecessary secrets, private documents and personal data in broadly accessible logs. Capture useful operational metadata with scoped access and retention instead of logging everything by default.')],
 ('Which is a good per-tenant control?',['Bounded token/job/concurrency budgets','One unlimited shared provider key exposed to browsers','No accounting until the bill arrives','Dropping access checks to reduce latency'],0,'Independent quotas constrain cost and resource impact without sacrificing data boundaries.'),skills=[268,269,270,271])
 lesson(c,'agent-lifecycle','Model migrations, routing, semantic caches and load tests',r'''
## Version the whole behaviour
A deployed AI feature depends on prompt, model, retrieval/index and tool/schema versions. Record them together with evaluation results and a changelog. When a provider deprecates a model, plan a migration and rerun the actual task suite before switching traffic.

## Route from evidence
A smaller model can handle easier cases and escalate under a defined policy. A model's self-reported confidence is not automatically calibrated. Evaluate the routing rule, error cases and escalation cost as a system, not just the strongest model alone.

## Semantic caching has correctness risks
Equivalent-looking questions can differ in tenant, permissions, date, source version or a critical numeric detail. Include the appropriate scope/freshness context and choose a conservative reuse policy. Measure wrong hits as well as hit rate; a high hit rate is not a success if answers are stale or leaked.

## Load the complete dependency graph
Ten times the user traffic can multiply retrieval, reranking, model and queue work. Include token lengths, slow-provider responses, retries, concurrent streams and cancellation. Watch p95/p99 latency, queue age, memory, connection limits and spending.

Keep a fallback/rollback plan that remains compatible with stored data and running jobs. A model upgrade is a product release with measurable quality, latency, cost and safety consequences, not merely a string replacement in configuration.
''','Plan a model migration with a shadow/canary comparison and rollback. Define semantic-cache exclusion cases and a load scenario that includes retries plus long responses.',[
 ('Why can a semantic-cache hit be wrong?','The wording may be similar while permissions, time, source version or a numeric detail differ. Cache equivalence must preserve the task\'s relevant context, not only embedding similarity.'),
 ('What must be evaluated in model routing?','The combined routing/escalation policy, including missed hard cases, latency, cost and category-specific errors. Evaluating only the strongest fallback model misses routing mistakes.')],
 ('What should accompany a model identifier change?',['Task evaluations, budget comparison and rollback evidence','A claim that all newer models are better','Deletion of the old golden dataset','Removal of source versioning'],0,'The deployed system must still satisfy its own quality/cost/latency contract.'),skills=[272,273,274,275,276])
