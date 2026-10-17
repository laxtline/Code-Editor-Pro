from .common import course,lesson

def build():
 c=course('mobile-flutter','Flutter & Dart','Mobile development','Choose one cross-platform path and learn its state, navigation and device boundaries.','4-6 weeks after programming basics','Build a task app with forms, local storage, API loading/error states and a signed test release.',['flutter'])
 lesson(c,'flutter-dart','Dart, widgets, layouts and state',r'''
## Dart first, then widgets
Learn variables, types, null safety, functions, collections, classes and async/await before copying a large Flutter screen. A nullable value needs an explicit handling path; suppressing every null warning does not make missing data valid.

Flutter builds UI from widgets. StatelessWidget describes output from inputs, while StatefulWidget associates a state object with a widget lifecycle. The framework rebuilds descriptions as state changes; a rebuild is not automatically a full recreation of every native resource.

## Compose a layout
Use Row/Column for linear arrangement, Stack for overlap and padding/alignment/sizing widgets for constraints. Parent constraints and child sizing rules explain many overflow errors. A long scrollable list should use an appropriate lazy builder rather than constructing an unbounded giant column.

setState marks relevant state as changed so UI can rebuild. Keep a small form's state local. Provider/Riverpod can organise broader state/dependency ownership, but choose one policy and understand its lifecycle instead of adding several state libraries at once.

Test text scaling, narrow devices, keyboard appearance and screen-reader labels. A layout that fits one emulator screenshot may overflow when translated or when a user increases font size. The browser study desk displays Dart examples as reading material; a Flutter project requires its SDK/toolchain.
''','Build a two-screen task UI with a list, an add form and a local completed filter. Explain which state is local, which is shared and how layout responds to a large font.',[
 ('How do stateless and stateful widgets differ?','A stateless widget describes UI from its inputs. A stateful widget has an associated state lifecycle for values that change over time; state ownership and update rules still need deliberate design.'),
 ('Why does a Row overflow?','Its children may request more horizontal space than the parent constraints allow. Inspect constraints and use appropriate flexible/wrapping/scrolling behaviour rather than shrinking every text blindly.')],
 ('What should guide choosing a state-management tool?',['State ownership and lifecycle needs','The largest number of packages','A belief that every value must be global','Only the app icon'],0,'A state tool should clarify who owns updates and how long state lives.'),
 ('dart','class Task {\n  final String id;\n  final String title;\n  final bool completed;\n  const Task(this.id, this.title, {this.completed = false});\n}\nvoid main() {\n  const task = Task("1", "Revise widgets");\n  print(task.title);\n}','In a Dart environment, prints Revise widgets.'))
 lesson(c,'flutter-data','Navigation, APIs, local storage, Firebase and release',r'''
## Navigation preserves a state contract
Pass stable identifiers between screens instead of relying on an object from one previous click. Decide which state survives returning, app backgrounding and process restart. Forms need validation, a submit state and retained data after a failed request.

## Local and remote data
Use an HTTP client such as http/dio with explicit timeouts, status/payload validation and stale-request handling. Preferences suit small non-secret settings; a local database/store can suit structured offline data. Do not store sensitive credentials in an ordinary unencrypted preferences file.

Firebase can provide authentication, Firestore and notifications, but its security rules are an actual backend boundary. A client configuration file is not permission to read every document. Enforce user/tenant access in rules/server logic and test denied cases. Service plans/quotas and setup requirements should be checked before deployment.

For offline updates, define conflict/deletion and retry policies. A local success indicator should distinguish saved-on-device from acknowledged-by-server. Notifications require device/platform permissions and an authenticated delivery design; they are not a reliable source of truth for business state.

## Prepare a release
Build the correct signed Android/iOS artefact using the relevant SDK/toolchain or supported build service. Keep signing material private, test on real devices and review current store requirements. An Android APK for local testing and an AAB/store distribution workflow are different deliverables.
''','Specify task persistence across app restart, a failed API save and a later retry. Plan authentication/rules for a per-user Firestore collection and a release smoke checklist.',[
 ('Why distinguish device-saved from server-synced?','A local write can succeed while the network request has not. The user should know which durability/synchronisation boundary has actually acknowledged the change.'),
 ('Does a Firebase client SDK remove access-rule design?','No. Security rules and server-side validation determine which data a signed-in or anonymous caller may access. Test one user attempting another user\'s documents.')],
 ('Which belongs in ordinary preferences?',['A non-secret theme choice','A private server administrator key','A payment webhook signing secret','An unrestricted database credential'],0,'Preferences are not a server secret store or a substitute for secure credential storage.'))

 c=course('mobile-kotlin','Android & Kotlin','Mobile development','Build native Android screens with Compose, lifecycle-aware state and tested local data.','4-6 weeks after basics','Build a Compose task app with Room persistence, an API repository and a signed internal-test build.',['android'])
 lesson(c,'android-state','Kotlin, Compose, ViewModel and navigation',r'''
## Learn the language contract
Kotlin has val/var bindings, nullable types, functions, classes and data classes. A nullable reference requires handling; a force-unwrapping operator can still crash when the assumption is wrong. Use immutable data and explicit updates for predictable UI state.

Jetpack Compose describes UI with composable functions. State changes can trigger recomposition, so keep composables free of unintended repeated side effects. Remembered UI state, saveable state and persistent database data have different survival lifetimes.

## ViewModel and MVVM
A ViewModel can own screen-level state and interact with repositories across suitable lifecycle events. MVVM separates presentation state, UI and data responsibilities; it is not a rule to place every function into a class with a particular suffix.

Navigation should use a defined route/argument contract and handle missing/deleted items. Pass an ID and reload through a repository when appropriate rather than keeping a fragile full object forever. Account for process death and configuration changes explicitly.

Use Android Studio/emulators for development and real-device tests for important behaviour. Validate large fonts, orientation/size changes, keyboard focus and accessibility semantics. A screen that recomposes is not by itself a performance bug; measure the actual expensive work.
''','Design Compose UI state for loading/error/ready task details. Explain what survives recomposition, configuration changes and process death, and where the task record is persisted.',[
 ('Why use a ViewModel rather than storing everything in a composable?','It can provide an appropriate owner for screen state and repository interaction across relevant lifecycle changes. Persisted data still needs a durable store; a ViewModel is not a backup database.'),
 ('What is recomposition?','Compose reevaluates relevant UI descriptions when observed state changes. Side effects and expensive work need appropriate APIs/ownership so reevaluation remains safe and efficient.')],
 ('Which value should normally be loaded through a stable navigation argument?',['A task ID used by a repository','A private backend key','An arbitrary executable string','A global mutable screen object required from a previous click'],0,'A stable identifier supports direct navigation, reload and clear data ownership.'),
 ('kotlin','data class Task(val id: String, val title: String, val done: Boolean = false)\nfun main() {\n    val task = Task("1", "Learn Compose")\n    val completed = task.copy(done = true)\n    println(completed)\n}','In a Kotlin environment, creates an updated immutable record.'))
 lesson(c,'android-data','Room, Retrofit, coroutines and publishing',r'''
## Repository boundaries
Room maps structured local data onto SQLite through defined entities/DAOs. Migrations preserve installed users' data as the schema evolves. A repository can coordinate local/remote sources, but it needs an explicit authority, freshness and conflict policy.

Retrofit is a common HTTP API client tool. Configure serialisation, authentication and timeouts, then handle non-success status and malformed/missing payloads. A generated interface does not validate every business invariant automatically.

## Coroutines are structured work
A suspend function can suspend without blocking its current execution context at supported operations; it does not automatically move every calculation to a background thread. Use appropriate dispatchers and lifecycle scopes, propagate cancellation and avoid retaining a dead screen through a long task.

Observe data through a lifecycle-aware mechanism and render loading, empty, failed and success states. Keep a failed edit locally and show whether retry/sync is pending. Handle app restart and a cancelled request without silently duplicating the operation.

## Platform boundaries
Ask for permissions only when the related feature needs them and provide a usable denied path. Notifications and background execution follow platform/version policies. For publishing, sign the correct artefact, protect signing credentials and verify current Play requirements, privacy declarations and target SDK rules before release.
''','Design an offline task edit stored in Room and retried through a repository. Explain coroutine cancellation on leaving a screen and the migration test for adding a required field.',[
 ('Does suspend mean run on a background thread?','No. It means the function can suspend. The execution context/dispatcher and the operations inside it determine where work runs and whether blocking occurs.'),
 ('Why test a Room migration with existing data?','An empty new database does not expose data-preservation and compatibility failures. A migration must keep previously installed users\' records valid under the new schema.')],
 ('What should a denied notification permission do?',['Keep the core app usable and explain the optional feature state','Delete local tasks','Retry the permission prompt forever','Assume every notification was delivered'],0,'Permissions are user-controlled capabilities with a required denied/recovery path.'))

 c=course('mobile-react-native','React Native & Expo','Mobile development','Reuse React concepts while learning native components, storage and device-specific delivery.','3-5 weeks after React','Build a cross-platform task client with navigation, API access, local drafts and a tested release build.',['rn','react'])
 lesson(c,'rn-components','Native components, hooks and screen navigation',r'''
## React concepts, different rendering targets
React Native uses components such as View, Text, Image, Pressable and scroll/list primitives instead of browser divs and paragraphs. Hooks and composition remain useful, but DOM APIs and CSS files do not transfer unchanged. Learn the supported style/layout model and platform differences.

Expo provides development/build tooling and modules around React Native. The available runtime and native-module workflow depend on the project configuration; do not assume every third-party native package works in every preview client without an appropriate build.

## Screen state and navigation
Use a navigation library with a clear route/parameter contract. Keep stable IDs and reloadable data, preserve useful local drafts and handle a missing/deleted resource. A mobile Back action and a browser history entry are different platform interactions that need testing.

Large lists should use an appropriate virtualised list primitive with stable keys. Handle safe areas, keyboard interaction, text scaling and accessible labels. A screenshot on one device does not establish correct layout across Android/iOS sizes.

Keep server state separate from purely local interface state. A repository/API module can centralise request configuration, but the backend still enforces auth, tenant permissions and business rules for the mobile client just as for the web client.
''','Convert a React web task card into a native component using supported primitives. Define navigation parameters, loading/error UI and a stable-key large-list strategy.',[
 ('Can a React Native screen use the browser DOM directly?','No. It renders through native-target components and APIs. React state/composition knowledge transfers, while platform UI, permissions and storage contracts differ.'),
 ('Why test real device text scaling?','Longer/larger text and platform accessibility settings can expose clipping, inaccessible controls and layout assumptions that a fixed emulator screenshot misses.')],
 ('Which is a basic React Native UI primitive?',['View','A browser-only document.querySelector call','An HTML table tag as a native layout','A CSS stylesheet link element'],0,'React Native has its own supported component and platform API model.'),
 ('jsx','import { View, Text, Pressable } from "react-native";\nexport function TaskCard({task, onComplete}) {\n  return <View><Text>{task.title}</Text><Pressable accessibilityRole="button" onPress={() => onComplete(task.id)}><Text>Complete</Text></Pressable></View>;\n}','In a React Native project, renders a native task card with an accessible action.'))
 lesson(c,'rn-release','Async storage, API sync, notifications and EAS builds',r'''
## Local data has a sensitivity level
AsyncStorage is useful for suitable non-secret key/value persistence, not a universal secure credential vault. Use an appropriate platform-backed secure store for credentials, and understand what survives logout, reinstall or device backup. Version structured saved data and test migrations.

For offline edits, store a local result and an explicit pending operation with an idempotency policy. Show device-saved versus server-acknowledged status. Resolve conflicting remote edits/deletions deliberately; copying one entire JSON blob over another can lose work.

## Connect to the right backend
On a physical device, localhost names that device, not your development laptop. Use the intended reachable development/staging endpoint with appropriate transport and auth configuration. Do not expose a privileged local code-execution server to a wider network as a shortcut.

Push notifications require platform credentials, permissions and token lifecycle management. A notification is a delivery signal, not proof of payment/order state. The app should fetch authorised durable state when needed.

Expo EAS can support build/distribution workflows with the required project configuration and signing credentials. Native iOS local builds/simulators require the relevant Apple tooling; cloud-build services have their own requirements. Review current store policies, privacy declarations and account/signing rules before publishing.
''','Specify local draft persistence, secure token handling and a pending-sync indicator. Plan an Android/iOS test release and explain how you verify the backend URL on a real phone.',[
 ('Why is AsyncStorage not the default place for a server secret?','It is client-side application storage, not a protected server credential boundary. Users/devices and compromised client code can expose it; keep server secrets on the backend.'),
 ('Why does localhost fail to reach a laptop API from a phone?','The hostname refers to the phone\'s own loopback interface. Development connectivity needs the correct reachable endpoint and security configuration, not an assumption that every device shares one localhost.')],
 ('What should a push notification trigger for sensitive business state?',['An authorised check of durable server state','Blindly marking an invoice paid','Skipping login forever','Publishing the device token to everyone'],0,'Notifications can be missed/duplicated and should not replace server-authoritative state.'))

 c=course('mobile-swift','Swift & SwiftUI','Mobile development','Learn native Apple UI, optionals, model ownership and async data boundaries.','4-6 weeks after basics','Build a SwiftUI notes app with persisted data, navigation, API error states and a distribution plan.',['swift'])
 lesson(c,'swift-state','Swift optionals, SwiftUI views and MVVM',r'''
## Make missing data explicit
Swift uses value/reference types, functions, structs/classes and optionals. An optional can hold a value or nil. Optional binding and other supported patterns make the missing path explicit; force unwrapping merely asserts that the programmer's assumption is correct at runtime.

SwiftUI describes views from state using layouts such as VStack, HStack and List. State ownership matters: local state, a binding into another owner's value and observable model state have different roles. The exact observation APIs depend on the supported SDK/version; learn the ownership contract rather than memorising one property wrapper for every situation.

## Separate responsibilities
MVVM can keep view rendering, screen state and data/repository operations understandable. A view model should expose useful loading/error/ready state, not hide every operation behind unrelated mutable flags. Keep persistence outside a temporary view's lifetime.

NavigationStack and a route/data identity strategy help make navigation reproducible. Handle deletion or a missing record when returning to a screen. Test larger accessibility text, keyboard/VoiceOver and device size changes.

Native Apple development uses the appropriate Xcode/macOS tooling for local builds and simulators. This offline lesson is reference material and does not emulate Xcode or package an iOS SDK.
''','Model a note detail screen with an optional selected note, loading/error/ready state and an editable title binding. Explain where the durable note lives when the view disappears.',[
 ('Why avoid force unwrapping by default?','It converts a potentially missing value into a runtime crash if the assumption is wrong. Handle the missing case explicitly unless a genuinely enforced invariant justifies the assertion.'),
 ('What is a binding conceptually?','It lets a child view read/update a value owned elsewhere through a controlled relationship. It is not an independent durable copy of that value.')],
 ('What does an optional represent?',['A value that may be absent','A guarantee that nil can never occur','Only a UI colour','A background thread'],0,'The missing case is part of the type and needs appropriate handling.'),
 ('swift','struct Note { let id: Int; var title: String }\nlet selected: Note? = Note(id: 1, title: "Learn Swift")\nif let note = selected {\n    print(note.title)\n} else {\n    print("No note selected")\n}','In a Swift environment, prints Learn Swift.'))
 lesson(c,'swift-data','URLSession, local persistence and App Store delivery',r'''
## Networking is a typed failure boundary
URLSession supports HTTP work and modern async/await interfaces. Check status, decode a defined model and handle transport, decoding and business errors distinctly. Do not assume a response body has the expected shape merely because bytes arrived.

Cancel stale work when an operation no longer belongs to the current screen/request. Keep a failed edit locally and make retry state visible. Update UI state on the appropriate execution context and avoid a long blocking calculation on the main actor.

## Persistence and permissions
Core Data and other current Apple persistence options manage structured local records under their own lifecycle/migration rules. Choose one and test existing data through a schema update. Store credentials using appropriate secure platform facilities, not a plain note database.

Notifications, photos, microphone and other device capabilities need purpose-specific permission handling and a useful denied path. Private media/document uploads require a clear user action and backend access policy.

## Release is more than Build succeeded
Signing, identifiers, distribution profiles, TestFlight/App Store Connect and current review/privacy requirements form a delivery workflow. Local native iOS tooling requires a suitable Mac/Xcode setup; cloud workflows still need the relevant credentials and supported configuration. Test launch, offline data, login recovery, permissions and an upgrade from a previous installed version.
''','Design a notes API call with cancellation, decoding and retained drafts on failure. Create a release checklist covering signing, privacy/permissions, persistence migration and real-device tests.',[
 ('Why distinguish transport and decoding errors?','They indicate different failure boundaries and recovery paths. A reachable server can return an incompatible payload, while a network outage can occur before any valid response exists.'),
 ('Why test an upgrade from an earlier installed app?','Existing users bring saved data, credentials and prior configuration. A clean install cannot expose migration or compatibility failures affecting those users.')],
 ('What must a persistence upgrade protect?',['Existing users\' valid saved data','Only a new empty demo database','Only the launch icon','Only a screenshot of the newest screen'],0,'Migration correctness includes previously stored records and their intended meaning.'))

 c=course('desktop-electron','Electron Desktop','Desktop development','Combine web UI with a narrow, permission-aware native bridge.','2-3 weeks after web development','Build a local notes desktop app with scoped file import/export and a signed/reviewed packaging plan.',['electron','mdn'])
 lesson(c,'electron-processes','Main, renderer, preload and IPC',r'''
## A desktop window has separate responsibilities
Electron combines a native main-process application layer with renderer windows using web technology. The main process owns privileged application/window operations. A preload can expose a narrow bridge; the renderer should not receive unrestricted operating-system authority just because it displays your UI.

Use context isolation and keep Node integration disabled for untrusted/ordinary renderer content according to the application's security design. Expose specific operations such as choose-and-read-note rather than a generic execute-command or read-any-path function. Validate IPC arguments and the calling context.

## Native workflows
Menus, windows and file dialogs belong to a clear process/lifecycle owner. A renderer asks for an operation; the privileged side validates the request and returns a bounded result. Keep source paths scoped to the user's intended selection and handle cancelled dialogs without discarding current work.

Treat loaded remote content, imported Markdown and generated HTML as untrusted. Navigation/new-window policy and resource loading matter in a desktop renderer too. Do not disable security settings merely to make an iframe or package work.

Test malformed IPC, a cancelled file picker and a renderer failure. A desktop wrapper adds capabilities and responsibility; it does not make an unsafe web interface automatically safe.
''','Define a preload API with readSelectedNote and saveCurrentNote operations. Specify input/output limits, cancellation and why arbitrary path/command methods are excluded.',[
 ('Why keep a narrow preload bridge?','It limits the authority available to renderer code. A successful renderer injection should not automatically become unrestricted file or command access.'),
 ('Does context isolation replace IPC validation?','No. It separates JavaScript contexts, while each exposed operation still needs argument, caller and resource-scope checks.')],
 ('Which bridge is safer?',['A specific validated save-note operation','An unrestricted execute-shell method','A read-any-file method exposed to every page','A private signing key in renderer state'],0,'A narrow operation can enforce the actual user-authorised resource and action.'),
 ('electron','// Preload concept: expose a small operation, not Node itself.\ncontextBridge.exposeInMainWorld("notes", {\n  save: (note) => ipcRenderer.invoke("notes:save", note)\n});\n// The main handler must validate note shape, caller and destination.','Project sketch: the privileged handler owns validation and file access.'))
 lesson(c,'electron-packaging','Local data, updates and installers',r'''
## Separate application files from user data
Packaged application assets may be replaced during an update. Store user notes/settings in an appropriate per-user data directory and use versioned migrations. Do not place the only copy of a user's work inside a disposable installation directory.

## File workflows
Use native dialogs for user-selected import/export, validate content and preserve a current backup before destructive replacement. Atomic replacement can reduce partial writes; concurrency, crash recovery and durability still need their own policy. Bound imported sizes and sanitise rich content.

## Package deliberately
Tools such as electron-builder can create platform deliverables, but signing, notarisation, runtime dependencies and distribution requirements differ. Protect signing credentials. Test the actual installed artefact away from the source repository, including paths with spaces and a user account without administrator privileges.

An update mechanism must verify artefact origin/integrity under its design and preserve user data. Stage a release, test upgrade/rollback and keep a clear version/history view. A downloaded file being named update does not establish trust.

For an offline-first tool, distinguish local saving from any optional remote sync. Export/import should remain usable when the provider or network is down. An installer finishing successfully is not proof that the app can open, save and reopen a note.
''','Specify a user-data directory policy, migration backup and installed-app smoke test. Include a path with spaces, a cancelled import and an upgrade retaining existing notes.',[
 ('Why keep user data outside application assets?','Updates and reinstalls can replace the application files. User data needs an independent lifecycle, migration and backup policy.'),
 ('Why test the installed package away from source?','The development environment can hide missing files, paths and runtime dependencies. A portable/installed smoke test checks what the user actually receives.')],
 ('What is essential in an app update?',['Verified artefact handling and preserved user data','Replacing every user note unconditionally','Publishing signing credentials','Assuming source-tree execution proves packaging'],0,'Updates affect both executable trust and the lifecycle of existing user work.'))

 c=course('desktop-python','Python Desktop','Desktop development','Build event-driven tools with a clear UI/thread/storage boundary.','2-3 weeks after Python','Build a local task manager with SQLite, import/export and a tested packaged executable.',['python'])
 lesson(c,'gui-python','Tkinter, PySide and event-driven interfaces',r'''
## Choose a toolkit and learn its event loop
Tkinter is part of the usual Python GUI ecosystem and is available in many standard Python installations; actual platform packaging can vary. PySide/PyQt provide Qt bindings, while CustomTkinter offers another styled-widget approach. Choose one toolkit and its deployment/license requirements before mixing several UI stacks.

Widgets include windows, buttons, labels, inputs, lists and menus. Layout managers express size/placement relationships; fixed pixel coordinates rarely survive different fonts and window sizes well. Keep callbacks small and move reusable business logic into plain Python functions/classes.

## Keep the interface responsive
The GUI event loop must continue processing input/render events. A long blocking network call or CPU loop inside a button callback freezes the window. Use a suitable worker strategy and the toolkit's supported way to deliver results back to the UI thread. Do not mutate widgets from arbitrary worker threads.

Show running, failed and completed states and preserve a draft on errors. Handle window-close while work is active with a bounded cancellation/save policy.

The browser's Python runtime does not provide an operating-system GUI display, so these toolkit examples belong in a local desktop environment. You can still read the full explanation and practise the non-GUI logic here.
''','Design a desktop task form with add/complete/delete callbacks. Separate validation/storage from widgets and explain how a slow import runs without freezing the window.',[
 ('Why does a long callback freeze a GUI?','It occupies the event-loop thread, preventing it from processing input and redraws. Move suitable work away and return updates through the toolkit\'s supported UI mechanism.'),
 ('Why test business logic outside the GUI?','Pure validation/calculation/storage contracts can be tested deterministically without opening windows. Keep a smaller set of interaction tests for the actual widget workflow.')],
 ('Where should a worker deliver a widget update?',['Through the toolkit\'s supported UI-thread mechanism','By mutating every widget from any thread','Only through a global print statement','By blocking the event loop until it finishes'],0,'Most GUI toolkits require coordinated UI-thread access.'),
 ('python-gui','import tkinter as tk\nroot = tk.Tk()\nroot.title("Study tasks")\nlabel = tk.Label(root, text="One useful task today")\nlabel.pack(padx=24, pady=12)\ntk.Button(root, text="Complete", command=lambda: label.config(text="Completed")).pack(pady=12)\nroot.mainloop()','Run in a local Python installation with Tk support, not the browser engine.'))
 lesson(c,'gui-storage','SQLite persistence and PyInstaller packaging',r'''
## Local data still needs a contract
SQLite is useful for structured single-application storage. Use parameterised SQL, transactions for related changes and a versioned migration policy. A desktop UI should not concatenate a task title into a SQL statement merely because the database is local.

Store the database in an appropriate writable user-data location. The current working directory can differ between a terminal, shortcut and installed executable. Keep temporary files separate from the only durable copy of a user's notes.

## Package the real dependency set
PyInstaller can bundle a Python application for a target platform, but hidden imports, data files, native libraries and toolkit plugins need validation. Building on one platform does not automatically produce a correct native installer for every other platform.

Test the output on a clean environment without the source folder or development virtual environment. Include a path with spaces/nontrivial characters, read-only install assets, database creation and a retained-data upgrade. Antivirus/code-signing and distribution policies can affect delivery and need a proper release process.

Provide export/import and a recoverable backup before a migration or replacement. A packaged executable starting once is only the first check; saving, closing and reopening actual user data is the important workflow.
''','Define SQLite tables and a migration for a desktop task app. Plan a package test that opens, saves, closes and restores data without access to the source repository.',[
 ('Why not rely on the current working directory for user data?','It can change depending on how the app is launched and may be unwritable or disposable. Use a deliberate per-user data location and keep installation assets separate.'),
 ('What can a source-folder test miss in packaging?','Missing bundled resources, native libraries, writable-path assumptions and implicit development dependencies. Test the produced executable in an isolated location.')],
 ('Which SQL approach is correct for a task title?',['A bound parameter','String concatenation into SQL','Trust it because the app is local','Execute it as a statement'],0,'Local input can still alter query structure if data and SQL are concatenated unsafely.'),
 ('python-desktop','import sqlite3\nwith sqlite3.connect(":memory:") as db:\n    db.execute("CREATE TABLE tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL)")\n    db.execute("INSERT INTO tasks(title) VALUES (?)", ("Revise SQL",))\n    print(db.execute("SELECT title FROM tasks").fetchone()[0])','Revise SQL'))

 c=course('desktop-dotnet','C# & .NET Desktop','Desktop development','Use typed models, native Windows UI and explicit data/service boundaries.','3-4 weeks after programming basics','Build a Windows task tool with validation, local data, async operations and a tested installer.',['dotnet'])
 lesson(c,'dotnet-ui','C#, .NET, WPF and WinForms',r'''
## Language, runtime and UI are separate layers
C# is the language; .NET supplies runtime/libraries/tooling. WPF and WinForms are Windows UI frameworks with different programming models. A .NET application is not automatically cross-platform when its selected UI stack is Windows-specific.

Learn types, nullable-reference contracts, collections, classes/interfaces, exceptions and async/await. Use composition/dependency injection for services when it clarifies ownership. Value and reference semantics affect copies, equality and mutable shared state.

## UI architecture
WinForms is event/control-oriented; WPF uses XAML, binding and commonly an MVVM approach. Keep validation and persistence out of a large button-click handler. A view model exposes state/commands while a service/repository handles a clear external boundary.

Do not block the UI thread with long synchronous work. Async I/O needs cancellation/error handling and an explicit loading state. CPU work needs an appropriate worker strategy rather than merely adding async to the method name.

Use accessible labels, keyboard paths and scaling-aware layouts. Test data binding updates and error recovery as behaviour. A successful compile does not prove that a binding points at the intended property or that user data survives closing the window.
''','Choose WPF or WinForms for a small Windows tool and explain the choice. Separate a task model, view model/callback layer and repository with a cancellation-aware save operation.',[
 ('Does .NET imply every UI is cross-platform?','No. Portability depends on the selected framework and platform APIs. WPF/WinForms are Windows-specific choices even though other .NET workloads can target different platforms.'),
 ('Why avoid database work directly in a giant click handler?','It mixes UI, validation and persistence lifecycles, making testing and failure recovery difficult. Separate responsibilities and keep the visible loading/error state explicit.')],
 ('Which is a Windows UI framework choice?',['WPF or WinForms','A DNS record','A Git remote','A database index'],0,'Those frameworks provide Windows desktop UI capabilities.'),
 ('csharp','public record TaskItem(int Id, string Title, bool Done);\nvar task = new TaskItem(1, "Learn .NET", false);\nvar completed = task with { Done = true };\nConsole.WriteLine(completed.Title);','In a compatible C# project, prints Learn .NET.'))
 lesson(c,'dotnet-data','Entity Framework, configuration and installers',r'''
## Data access still has database semantics
Entity Framework Core maps models and queries to a database provider. It can simplify access, but constraints, transactions, indexes and generated query behaviour still need review. Keep a DbContext lifetime appropriate to the unit of work rather than sharing one global mutable context across unrelated operations.

Review migrations against existing data and test the selected provider. An in-memory substitute does not reproduce every relational guarantee. Select explicit public/view models instead of binding an unrestricted persistence entity directly to a privileged edit form.

## Configuration and secrets
Separate environment settings from application source. A desktop client distributed to users cannot keep a universal privileged server credential private. Authenticate the user to a backend when access requires server authority, and use suitable OS-backed storage for local credentials.

## Deliver a repeatable artefact
Choose framework-dependent versus self-contained deployment according to runtime/distribution needs. An installer/update path should preserve user data and apply safe migrations. Signing, runtime dependencies and enterprise/store distribution requirements depend on the target environment.

Test installation under a normal user, first launch, offline local work, save/reopen and an upgrade with prior data. Keep a recovery/export path when a migration fails. Record which produced artefact was tested, not only that the IDE run button worked.
''','Plan an EF Core SQLite task repository and a migration test. Compare framework-dependent/self-contained deployment and specify an installer upgrade that retains existing data.',[
 ('Why does DbContext lifetime matter?','It tracks a unit of work and entity state. An inappropriate global/shared lifetime can retain stale state, grow memory or create concurrency issues; scope it to the operation design.'),
 ('Can a distributed desktop client keep a shared admin API key secret?','No reliable client-side boundary makes a universal embedded key private from its users. Use per-user authentication and a backend that enforces authority.')],
 ('Which must an installer upgrade preserve?',['The intended user-data lifecycle and migration path','Only the development project file','A private admin key embedded in every copy','Only a new empty screenshot'],0,'Existing saved data and compatibility are part of the delivered product contract.'))
