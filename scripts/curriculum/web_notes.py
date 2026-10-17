from .common import course,lesson

def build():
 c=course('html','HTML','Web foundations','Structure meaningful pages, forms and content before adding styling.','1-2 weeks','Build an About Me page with a portrait, navigation, a skills table and an accessible contact form.',['mdn','w3html','freecodecamp'])
 lesson(c,'html-start','Document structure, elements and attributes',r'''
## A page is a tree of elements
HTML describes the meaning and structure of a document. A tag such as `<p>` starts an element, its text is content, and `</p>` ends it. Attributes add information to the opening tag. Void elements such as `<img>` and `<input>` do not wrap child content. Nest elements correctly: a browser may repair invalid markup in surprising ways.

## Build the smallest real document
Start with `<!doctype html>` so the browser uses standards mode. Put the language on `<html lang="en">`. The `<head>` contains metadata such as UTF-8 encoding, viewport information and the tab title; the `<body>` contains the visible document. A title in the head is different from the main heading in the body.

Use `<h1>` for the main page heading and h2/h3 for subsections. Heading levels express structure, not font size. Paragraphs use `<p>`. Use `<strong>` for importance and `<em>` for emphasis; styling alone does not communicate those meanings.

## IDs and classes
An `id` identifies one element in a document and can be a link target or a form label target. A `class` can be shared by many elements for styling and selection. Keep IDs unique. Escape literal `<`, `>` and `&` where needed in text using character references such as `&lt;` and `&amp;`.

Create a valid page first, open it in a browser, then inspect its DOM in DevTools. HTML validation and visual appearance are separate checks.
''','Create an About Me document with a meaningful title, one main heading, two subsections and a paragraph containing an escaped less-than symbol. Inspect the DOM tree.',[
 ('What is the difference between an element and an attribute?','An element defines a piece of document structure, such as a paragraph or image. An attribute configures that element, such as an image source, alternative text or a language value.'),
 ('Why declare the viewport?','Mobile browsers need an appropriate layout viewport to render a responsive design at device width. The viewport declaration enables that behaviour; responsive CSS still has to supply a suitable layout.')],
 ('Where does the browser-tab title belong?',['Inside title in head','Inside every paragraph','As the first class name','Inside the image alt attribute'],0,'The title element in the document head supplies the page title.'),
 ('html','<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>My learning desk</title></head>\n<body><h1>My learning desk</h1><h2>Today</h2><p>Learn HTML &amp; build one page.</p></body>\n</html>','A heading, a subsection and a paragraph appear in the preview.'))
 lesson(c,'html-content','Links, images, lists and tables',r'''
## Use the right content element
Use `<a href="...">` for navigation and `<button>` for an action. A relative link points within your site; an absolute URL names a complete location. A fragment such as `#contact` jumps to an element ID. Write descriptive link text so a reader understands the destination without surrounding text.

An image needs a source and a text alternative that serves the image's purpose. A decorative image usually needs `alt=""`, while an informative diagram needs a useful explanation. Set dimensions or an aspect ratio to reserve space and reduce layout shifts. Use responsive image techniques when one file would be unnecessarily large for small screens.

## Lists express relationships
Use `<ul>` when order does not matter, `<ol>` when sequence matters and `<li>` for each item. A description list uses `<dl>`, `<dt>` and `<dd>` for term/description pairs. Do not imitate a list using repeated paragraphs and decorative dashes when the semantic relationship is a list.

## Tables are for tabular data
Use a caption, table head/body groups and header cells. A column header can use `<th scope="col">`; a row header can use `scope="row"`. Keep the data comprehensible in reading order and provide horizontal overflow on narrow screens when needed. Do not use tables merely to position a page's sidebar.

When a chart communicates a value, include the values or a data table as an alternative. Colour alone should not be the only way to identify a series or status.
''','Add a project list, a contact fragment link and a skills table with a caption and headers. Write alternative text for an informative portrait and explain when an empty alt would be correct.',[
 ('When should a button be used instead of a link?','Use a link to navigate to a location or resource. Use a button to perform an action such as saving, submitting or opening a dialog. Native elements provide expected keyboard and browser behaviour.'),
 ('Why add table headers and a caption?','They explain what the data means and help assistive technology associate values with the correct rows or columns. A visually bold cell alone does not provide that relationship.')],
 ('Which element represents an ordered sequence?',['ol','ul','div','span'],0,'An ordered list communicates that the sequence of items matters.'),
 ('html','<h1>Practice plan</h1>\n<ol><li>Read the rule</li><li>Solve an example</li><li>Review mistakes</li></ol>\n<table><caption>Weekly targets</caption><thead><tr><th scope="col">Topic</th><th scope="col">Questions</th></tr></thead><tbody><tr><th scope="row">Arrays</th><td>10</td></tr><tr><th scope="row">SQL</th><td>5</td></tr></tbody></table>','A numbered plan and a labelled two-column table.'))
 lesson(c,'html-semantic','Semantic pages, divs and accessible structure',r'''
## Structure expresses purpose
A div is a generic block container and a span is a generic inline container. They are useful when no more specific element fits. A meaningful page also has landmarks: `<header>`, `<nav>`, `<main>`, `<aside>` and `<footer>`. An article is independently meaningful content; a section groups a thematic part, normally with a heading.

## Build a page skeleton
1. Put a skip link before repeated navigation so keyboard users can reach main content quickly.
2. Use a navigation landmark for the important site links and a main landmark for the primary content.
3. Keep heading levels in a logical hierarchy. Use CSS to change visual size instead of choosing a wrong heading level.
4. Use native interactive controls. A clickable div does not automatically gain focus, button semantics or Enter/Space handling.

## Accessibility is behaviour
Test the whole path using Tab, Shift+Tab, Enter and Space. Ensure visible focus and sufficient contrast. A hidden control should not remain unexpectedly focusable. For custom widgets, use ARIA only when native HTML cannot express the required role and state; incorrect ARIA can make a useful page worse.

Screen-reader testing complements automated checks. A tool can find a missing label, but it cannot prove that a checkout instruction or an image alternative is helpful. Write specific error messages and associate them with the relevant field. Accessibility improves predictable interaction for everyone, including users on a small screen or with a temporary injury.
''','Rebuild your About Me page with landmarks, a skip link and a logical heading order. Complete its form using only the keyboard and note every unexpected focus movement.',[
 ('Why is semantic HTML useful beyond SEO?','It communicates document structure and expected interaction to browsers and assistive technology. A native button, labelled form and clear heading hierarchy provide behaviour that generic containers do not.'),
 ('Should every div receive an ARIA role?','No. Start with appropriate native elements. Add ARIA only when required semantics are missing, and implement the associated keyboard and focus behaviour as well.')],
 ('Which is the best default for a Save action?',['A button with meaningful text','A div with a click listener only','A paragraph with a green colour','An image without an accessible name'],0,'A native button already has keyboard focus and activation behaviour.'),
 ('html','<a href="#main">Skip to content</a>\n<header><h1>Learning notebook</h1><nav aria-label="Main"><a href="#main">Notes</a> <a href="#contact">Contact</a></nav></header>\n<main id="main"><article><h2>Why I practise</h2><p>Small deliberate exercises build understanding.</p></article></main>\n<footer id="contact">Contact: learner@example.invalid</footer>','A semantic page with a skip link, navigation, article and footer.'),skills=[27,31])
 lesson(c,'html-forms','Forms, labels and validation',r'''
## A form is an input contract
A form groups controls and submits named values. The action identifies the destination and the method describes submission semantics. GET is useful for a search whose state belongs in a URL; POST sends a request body for a submission. A secure connection is still required for private data.

Associate a visible `<label>` with its input through `for` and a matching unique ID, or wrap the input in its label. A placeholder is not a replacement for a label: it disappears as the user types. The `name` controls the key used in form data; the ID is mainly for document relationships and selection.

## Common controls
Use text/email/password/number/date input types according to the value, a textarea for longer text, a select for a fixed list and radio buttons for one choice in a group. Checkboxes represent independent choices. Related controls can be grouped with fieldset and legend. In a form, set `type="button"` on an action that must not submit; the default button type can otherwise surprise you.

## Validate without trusting the browser
Attributes such as required, minlength, min, max and pattern improve immediate feedback. The backend must validate again because a caller can send an HTTP request without your form. Show a useful field-specific error and retain valid entered data. Do not accept a price, role or account owner simply because a hidden form field supplied it.

The offline preview demonstrates native validation only; it does not send email or create an account.
''','Create a contact form with a name, email, topic selection and message. Add visible labels, native constraints and a non-submit Clear button. Describe the checks a real backend must repeat.',[
 ('Why is client-side validation insufficient?','It helps usability, but callers can bypass it or modify requests. The server must enforce data constraints, permissions and business rules independently.'),
 ('What is the difference between an input name and id?','The name determines the field key included in form submission. The id identifies an element in the document and can connect its label, error message or fragment link.')],
 ('Which label association is correct?',['label for="email" with input id="email"','label class="email" with any input','A placeholder with no label','Two unrelated IDs with matching colours'],0,'The for value and the input ID create an explicit label relationship.'),
 ('html','<h1>Contact practice</h1>\n<form onsubmit="event.preventDefault(); document.getElementById(\'result\').textContent=\'Valid demo form; nothing was sent.\'">\n<p><label for="name">Name</label><input id="name" name="name" required minlength="2"></p>\n<p><label for="email">Email</label><input id="email" name="email" type="email" required></p>\n<p><label for="message">Message</label><textarea id="message" name="message" required></textarea></p>\n<button type="submit">Check form</button><p id="result" role="status"></p></form>','Invalid inputs trigger browser feedback; a valid form displays a local demo message.'))
 lesson(c,'web-browser','Page loading and DevTools diagnosis',r'''
## Follow a page request
The browser resolves the host, establishes a connection and requests the document. It parses HTML into a DOM and CSS into style information. Scripts may modify that structure. The browser calculates styles and layout, paints content and composites layers. These activities overlap with downloading resources; a slow page is not explained by one universal number.

## Find the bottleneck
Open the Network panel, reload and inspect the waterfall. Separate waiting for the server from transferring a large file. Look for unnecessary requests, oversized images and render-blocking resources. Cache behaviour changes repeat visits, so compare a controlled cold load with a repeat load.

The Performance panel shows main-thread work, long tasks and layout/paint activity. A large JavaScript loop can freeze interaction even after all files finished downloading. Memory tools help find retained objects and detached DOM nodes. Check whether a suspected leak persists after ordinary garbage collection rather than treating every temporary allocation as a leak.

## Measure a change
Record a baseline, make one relevant change and repeat the same interaction under similar conditions. Core Web Vitals address different parts of experience: loading, visual stability and interaction responsiveness. Lab results help diagnose, while real-user measurements reveal actual device/network conditions.

Source maps connect bundled code to original sources. They improve diagnosis, but deployment policy should control access and avoid publishing secrets in source files. A production minifier does not make embedded credentials private.
''',"Inspect this app with Network and Performance tools. Identify one request's timing phases and one user interaction. Write a before/after measurement plan for lazy-loading a large optional component.",[
 ('Why can a page remain unresponsive after downloading?','JavaScript and rendering work can still occupy the main thread. A long synchronous task blocks input handling even when the network panel is idle.'),
 ('How would you investigate a layout shift?','Find which element moved and when, then inspect late-loading images, fonts or injected content. Reserve dimensions and compare the same loading path after the change.')],
 ('Which tool best shows long main-thread tasks?',['The browser Performance panel','Only the page title','A screenshot of the footer','A Git branch name'],0,'The Performance timeline exposes CPU work and interaction delays.'),
 skills=[40,41])

 c=course('css','CSS','Web foundations','Style readable, responsive interfaces with a predictable cascade and layout.','2-3 weeks','Style your About Me page, then build an original responsive landing page with keyboard-visible controls.',['mdn','w3css','freecodecamp'])
 lesson(c,'css-cascade','Selectors, cascade, units and colours',r'''
## A rule selects and declares
`p { color: navy; }` selects paragraphs and declares a property value. Use element selectors for broad defaults, classes for reusable components and IDs sparingly for styling. Combinators express relationships; pseudo-classes such as `:hover` and `:focus-visible` express state.

When rules conflict, the cascade considers origins/importance, layers, specificity and order. More selectors do not automatically make a better design. Keep specificity low and avoid solving every conflict with `!important`. Some properties inherit from an ancestor; many layout properties do not.

## Choose units deliberately
Pixels are useful for fine borders, while rem scales with the root font size and em depends on the relevant font size. Percentages depend on the containing context. Viewport units relate to the viewport, but mobile browser chrome makes dynamic viewport units useful for some full-height layouts. `clamp()` can bound a fluid value.

Define theme colours and spacing as custom properties so changes have one source of truth. Ensure contrast, and do not use colour alone to communicate an error. Keep focus visible when changing button styling.

A practical debugging order is: inspect the element, check which rule wins, inspect computed values, then inspect the box and its containing layout. Guessing by repeatedly adding selectors makes the stylesheet harder to maintain.
''','Create reusable text, button and card classes with custom properties. Intentionally create a conflicting rule, then explain from DevTools why one declaration wins.',[
 ('Why avoid excessive selector specificity?','It makes later overrides difficult and ties styles to a particular DOM shape. Small reusable classes with a deliberate cascade are easier to maintain and theme.'),
 ('How do rem and em differ?','rem is based on the root element\'s font size. em is based on the relevant element\'s font size, with details depending on the property, so nested contexts can scale differently.')],
 ('What should you inspect first when a colour rule is ignored?',['The winning cascade and computed styles','The GitHub repository description','The database index','The screen brightness only'],0,'DevTools shows overridden declarations and the value actually applied.'),
 ('css',':root { --accent: #157c52; }\nbody { font: 1rem/1.7 system-ui; padding: 2rem; }\nh1 { color: var(--accent); font-size: clamp(1.8rem, 5vw, 3rem); }\nbutton { padding: .7rem 1rem; color: white; background: var(--accent); border: 0; border-radius: .5rem; }\nbutton:focus-visible { outline: 3px solid #d68b00; outline-offset: 3px; }','The preview has a fluid green heading and a visibly focusable button.'))
 lesson(c,'css-layout','Box model, display, Flexbox and Grid',r'''
## Every rendered box has layers
Content is surrounded by padding, then border, then margin. With content-box, width describes content width; with border-box, the declared width includes padding and border. Set border-box consistently to simplify component sizing. Margin collapse can affect adjacent block margins; padding does not collapse in the same way.

`display` chooses a layout participation model. Block elements normally start a new line; inline content flows in a line; flex and grid containers lay out their children with their own rules. `display:none` removes a box from layout; hiding visibility can preserve its occupied space.

## Flexbox for one dimension
Use Flexbox for rows or columns such as a toolbar. The main axis follows flex-direction; justify-content acts on that axis, while align-items acts on the cross axis. Gaps separate children. A child with long content may need `min-width:0` to shrink rather than overflow.

## Grid for rows and columns
Grid defines tracks and lets items align across two dimensions. `repeat(3, minmax(0, 1fr))` gives three shrinkable equal columns. An auto-fit/minmax pattern can create a card grid that adapts to available width. Use Grid for a sidebar/content page and Flexbox within a toolbar.

Do not fix an overflow bug by hiding all page overflow. Find the element whose intrinsic size or minimum size exceeds its container. Tables and code samples may need their own scroll region.
''','Build a dashboard with a sidebar, a main area and responsive cards. Put a long unbroken code string in one card and repair the resulting overflow without clipping the entire page.',[
 ('When would you choose Grid over Flexbox?','Grid is useful when rows and columns should align together. Flexbox is useful for distributing items along one main axis, such as a navigation row; both can be combined.'),
 ('Why does min-width:0 fix some flex/grid overflows?','A child can otherwise keep an automatic minimum based on its content. Allowing it to shrink lets wrapping or a deliberate inner scroll area handle long content.')],
 ('With border-box, what does width include?',['Content, padding and border','Only margin','The entire browser window','Only the text characters'],0,'Border-box includes padding and border in the declared width, but not margin.'),
 ('css','* { box-sizing: border-box; }\nbody { margin: 0; padding: 1.5rem; font: 1rem system-ui; }\nmain { display: grid; gap: 1rem; max-width: 50rem; margin: auto; }\np, h1 { padding: 1rem; margin: 0; background: #e3f4eb; border-radius: .5rem; }\n@media (min-width: 40rem) { main { grid-template-columns: 2fr 1fr; } h1 { grid-column: 1 / -1; } }','The example switches between one and two columns as the preview width changes.'),skills=[28])
 lesson(c,'css-responsive','Responsive design, positioning and stacking',r'''
## Start with a usable narrow layout
Mobile-first design means the base rules work at a small width. Add columns when content has enough space, not merely at a device brand's width. Let text wrap, size images within their containers and use comfortable interactive targets. Test keyboard interaction and zoom as well as a resized window.

Media queries respond to conditions such as viewport width or reduced-motion preference. Container queries respond to an element's containing layout, which is useful for components reused in different page regions. Fluid sizing with percentages, max-width and clamp can reduce the number of breakpoints.

## Positioning is relative to a context
Static is ordinary flow. Relative positioning offsets a box while retaining its flow space and can establish a containing block. Absolute positioning removes a box from normal flow and positions it against its containing block. Fixed positioning relates to a fixed containing context, commonly the viewport. Sticky positioning combines flow participation with a scroll threshold and depends on the relevant scrolling ancestors.

`z-index` does not rank every element in the entire document independently. Stacking contexts group descendants; properties such as transforms and opacity can create one. A large z-index inside a lower context may still sit below another context.

For a mobile topic drawer, preserve a close control, focus behaviour and page scrolling. Do not cover the code editor with a fixed footer unless sufficient space is reserved for the footer's actual height.
''','Turn a two-column tutorial page into a narrow-screen layout with a topic drawer. Test at 360px, with long titles and at 200% zoom. Explain the containing block for an absolutely positioned badge.',[
 ('Why can z-index:999999 fail to bring a modal above a header?','The modal may be inside a stacking context below the header\'s context. Inspect the ancestor contexts instead of repeatedly increasing one descendant\'s number.'),
 ('How do media and container queries differ?','A media query normally responds to environment conditions such as viewport width. A container query responds to a selected ancestor container\'s dimensions or supported style conditions, making a component more reusable.')],
 ('Which is a good breakpoint rule?',['Change layout when the content needs more space','Use one phone model as the only test','Prevent all text from wrapping','Always force three columns'],0,'Content-driven breakpoints adapt better to varied screens, text lengths and zoom.'),skills=[29])
 lesson(c,'css-modern','Transitions, custom properties and modern CSS',r'''
## Animate a meaningful change
A transition interpolates between supported property values when state changes. An animation uses named keyframes for a sequence. Prefer transforms and opacity for many motion effects, and measure when a complex effect affects responsiveness. Animation should clarify a state change rather than delay the user's next action.

Respect `prefers-reduced-motion` and avoid essential information that can be understood only while something moves. Keep loading and validation states clear even when motion is disabled.

## Maintainable modern rules
Custom properties hold reusable design values and participate in inheritance and the cascade. They can change by theme or component context. Cascade layers let a stylesheet declare the relative priority of groups such as base, components and utilities before specificity is considered within them.

`:has()` selects an element based on a relative selector condition, such as a field group containing invalid input. Use it as a precise tool, not as an excuse to make the DOM and stylesheet inseparable. Container queries allow a card to respond to its allocated width instead of assuming that viewport width predicts its space.

Use progressive enhancement: begin with readable content and working controls, then add modern presentation where supported. A CSS feature should improve the experience without making the underlying information disappear in a less capable environment.
''','Add hover/focus transitions to a card, then disable nonessential motion under prefers-reduced-motion. Create a theme using custom properties and explain the fallback appearance.',[
 ('Why use design tokens through custom properties?','They give colours, spacing and typography shared names and a controlled override mechanism. A theme can change a small set of values instead of editing dozens of unrelated rules.'),
 ('Why honour reduced-motion preferences?','Some motion can be uncomfortable or disruptive. The interface should preserve all information and actions while reducing nonessential movement for users who request it.')],
 ('Which is the best fallback strategy?',['Readable working content before optional effects','Hide all content until animation loads','Require hover to reveal every action','Use motion as the only error signal'],0,'Progressive enhancement preserves the core experience when optional presentation is unavailable.'),
 ('css',':root { --surface: #ecf8f1; --accent: #146b48; }\nbody { font: 1rem system-ui; padding: 2rem; }\nmain { padding: 2rem; border-radius: 1rem; background: var(--surface); }\nbutton { background: var(--accent); color: white; padding: 1rem; border: 0; transition: transform .15s ease; }\nbutton:hover { transform: translateY(-3px); }\n@media (prefers-reduced-motion: reduce) { button { transition: none; } button:hover { transform: none; } }','A themed card with a small optional button transition.'),skills=[32])
 lesson(c,'css-utilities','Tailwind, Bootstrap and a reusable design system',r'''
## Frameworks encode styling choices
Tailwind uses utility classes to compose a design directly in markup. Bootstrap supplies a collection of layout utilities and predesigned components. Neither removes the need to understand HTML semantics, the box model or responsive behaviour. Choose a consistent approach for the project instead of mixing several conflicting systems.

## A utility workflow
Start with shared colour, spacing and typography tokens. Compose a component from a small set of utilities, add responsive and interaction variants, then extract a component when its behaviour or repeated pattern deserves a name. A reusable component should expose meaningful variants such as size or intent rather than arbitrary unrelated class strings.

When building class names dynamically, understand what the build tool scans. A runtime-generated class that is absent from scanned source may not be generated. Prefer complete known class names or the framework's supported mechanisms.

## Design for states
A button needs normal, focus, disabled and loading states. A form field needs valid, invalid and help-message states. A dashboard needs loading, empty, successful and error states. A design system is not just a colour palette; it is a set of accessible, consistent decisions and contracts.

The offline example uses plain CSS equivalents so it does not download a framework. In a real Tailwind or Bootstrap project, install/configure the selected major version according to its documentation; build setup can differ between versions.
''','Define primary/secondary button variants, two card densities and a form-error style. Implement them first in plain CSS, then describe how you would map them to utilities without changing their semantics.',[
 ('Does a utility CSS framework replace CSS knowledge?','No. It gives convenient names and conventions for CSS decisions, but debugging alignment, overflow, specificity and responsive behaviour still requires understanding those decisions.'),
 ('What makes a design system more than a component folder?','It includes shared tokens, accessible interaction contracts, documented variants and rules for states and composition. Consistency is a behaviour and maintenance concern as well as a visual one.')],
 ('Which state must an interactive design system include?',['Visible keyboard focus','Only hover on a mouse','Only a static screenshot','Only the brand colour'],0,'Keyboard users need a visible indication of the active control.'),skills=[30])

 c=course('javascript','JavaScript','Web foundations','Learn the browser language, from variables and arrays to DOM events and async APIs.','4-6 weeks','Build a calculator, persistent task list, offline quiz and API-powered weather interface with loading/error states.',['mdn','jsinfo','odin'])
 lesson(c,'js-values','Variables, operators, conditions and loops',r'''
## Values and bindings
Use const when a binding should not be reassigned and let when reassignment is part of the algorithm. const does not freeze an object. Avoid var in new beginner code so block-scoping rules remain predictable. JavaScript values include numbers, strings, booleans, null, undefined, objects and other specialised types such as BigInt.

Use strict equality `===` for comparisons unless coercion is a deliberate part of the contract. The plus operator can add numbers or concatenate text, so convert input explicitly. `Number("")` is zero; a conversion alone does not prove that required input was present. Number values use floating-point arithmetic, so money calculations need a deliberate representation and rounding policy.

## Flow control
Use if/else or switch for choices, for/while for controlled repetition and for...of to visit iterable values. for...in enumerates property keys and is not the default array-value loop. `break` exits and `continue` skips to the next iteration.

Nullish coalescing `??` supplies a default for null or undefined. The `||` operator also treats zero, false and an empty string as false, which may overwrite valid values. Optional chaining can safely access a missing nested property, but it should not silently hide a missing required field.

Trace the initial value, each update and the stopping condition. Test empty inputs, zero and negative values before trusting a loop.
''','Write a calculator function accepting two numeric values and an operator. Reject missing/invalid inputs and division by zero; keep DOM handling separate from calculation.',[
 ('Can a const array be changed?','Its binding cannot be reassigned, but the array object can still be mutated through methods such as push. Immutability requires a separate design or enforcement mechanism.'),
 ('When is ?? safer than || for a default?','When false, zero or an empty string are legitimate values. ?? substitutes only for null or undefined, while || substitutes for every falsy operand.')],
 ('What does 0 ?? 10 evaluate to?',['0','10','null','undefined'],0,'Zero is not null or undefined, so the left operand is retained.'),
 ('javascript','const values = [0, 2, 4];\nconsole.log(values.map(n => n * 3));\nconsole.log(0 ?? 10);\nconsole.log(0 || 10);','[0,6,12]\n0\n10'))
 lesson(c,'js-arrays','Arrays, objects and useful transformations',r'''
## Choose a transformation by its result
map creates one transformed output per input item. filter keeps matching items. find returns the first matching item or undefined. some/every answer boolean questions. forEach performs side effects and returns undefined; it is not a replacement for map when you need a result array. reduce combines items into an accumulator and benefits from a clear initial value.

Objects group named properties. Use destructuring to read meaningful fields and spread to make shallow copies. A shallow copy shares nested objects, just as in Python. Use Map when key/value operations require arbitrary key types or a dedicated map interface; use Set for uniqueness.

## Sorting is a common trap
Array.sort mutates its array and compares strings by default. For numeric ascending order, pass `(a,b) => a-b`. Clone first when the original order must remain unchanged. A comparator must be consistent; returning only true/false is not a correct general numeric comparison.

## Use data to drive the UI
Store tasks as records with stable IDs, titles and completion flags. Derive the visible filtered list rather than keeping several independently mutated copies. For a quiz, keep question data separate from the current answer state. This makes saving, testing and rendering easier.

Treat arrays from external JSON as untrusted until their shape is checked. An apparently successful fetch can still return a missing field or an unexpected object.
''','Build a pure transformation that filters completed tasks, sorts them by title and returns only their IDs. Verify the original task array remains unchanged.',[
 ('How do map and forEach differ?','map returns a new array of transformed values. forEach is intended for side effects and returns undefined, so assigning its result does not give you transformed items.'),
 ('Why clone before sorting in state code?','sort mutates the array. A shallow array copy lets you reorder a new container while preserving the previous state\'s array identity and order; nested objects are still shared.')],
 ('Which sorts numbers without mutating nums?',['[...nums].sort((a,b)=>a-b)','nums.sort()','nums.forEach(x=>x)','nums.sort((a,b)=>a>b)'],0,'A copy preserves the original, and the numeric comparator avoids string ordering.'),
 ('javascript','const nums = [10, 2, 5];\nconsole.log([...nums].sort((a,b) => a-b));\nconsole.log(nums);\nconsole.log(nums.filter(n => n > 3).map(n => n*2));','[2,5,10]\n[10,2,5]\n[20,10]'))
 lesson(c,'js-functions','Functions, closures, this and prototypes',r'''
## Functions are values
A function can be passed as an argument, returned from another function or stored in an object. Arrow functions provide concise syntax and capture this from the surrounding scope. Ordinary function calls determine this from how they are invoked, with strict-mode details affecting unbound calls. An arrow is therefore not a universal replacement for an object method.

## Scope and closures
Lexical scope depends on where code is defined. A closure retains access to its defining environment even after the outer call finishes. Use this for private state or a configured callback. Avoid unintentionally retaining large objects through long-lived closures.

let/const are block-scoped. Their bindings exist before the declaration is evaluated but cannot be accessed in the temporal dead zone. A loop with let creates useful per-iteration bindings for closures, unlike a single shared var binding.

## Objects delegate through prototypes
When a property is not found on an object, JavaScript can look along its prototype chain. Class syntax builds on that object model; it does not turn JavaScript into a different runtime. Prefer composition for independent behaviours instead of long inheritance chains.

ES modules use import/export and explicit dependencies. Browser modules have their own scope and strict semantics. Keep a module's public API small and avoid relying on execution order of unrelated global script files when designing a new application.
''','Write a counter factory with increment/read functions that share private state. Create two counters and prove that their state is independent. Then explain a method losing its receiver when passed as a callback.',[
 ('What is a closure?','A callable that retains access to its lexical environment. For example, a counter function can continue reading and updating a variable created by its factory after that factory returns.'),
 ('Why can an arrow function be wrong as an object method?','It captures this from its surrounding scope rather than receiving the object as this from method-call syntax. Use the function form that matches the intended receiver contract.')],
 ('What determines a closure\'s outer scope?',['Where the function is defined','Only where it is called','The current HTML colour','The last imported CSS file'],0,'Closures follow lexical scope, which is determined by definition context.'),
 ('javascript','function makeCounter(){\n  let count = 0;\n  return () => ++count;\n}\nconst a = makeCounter(), b = makeCounter();\nconsole.log(a(), a(), b());','1 2 1'),skills=[33])
 lesson(c,'js-dom','DOM selection, events and accessible interactions',r'''
## The DOM is the live document
querySelector finds the first matching element; querySelectorAll returns a static collection of matches. Create elements, set properties and append them to update the page. Use textContent for plain text. Assigning untrusted text to innerHTML can create an injection vulnerability; sanitisation is required when HTML rendering is an intentional feature.

## Events carry context
addEventListener attaches behaviour without overwriting every other listener. The event target is where the event began; currentTarget is the element whose listener is running. Many events bubble to ancestors, so a container can delegate actions for dynamically added children. Use closest with a bounded container check when selecting an action element.

preventDefault cancels a default browser action when cancelable; stopPropagation affects event propagation. They solve different problems. Do not use either as a universal fix for a confusing click path.

## A task-list workflow
Keep tasks in data, add one through a form submit event, render stable IDs, update completion through a button/checkbox, then persist the data. Handle empty and invalid states. A keyboard user should complete every action, and a live status region can announce a save or validation result.

Do not attach a fresh global listener every time you render without removing the previous one. Duplicate listeners can cause double saves and confusing behaviour. Store state once and derive visible output from it.
''','Build a task list with add, complete and delete. Use a labelled form, event delegation and textContent for task names. Verify a task name containing HTML stays text.',[
 ('How do target and currentTarget differ?','target is the element where the event originated. currentTarget is the element whose listener is currently executing, which may be an ancestor during bubbling.'),
 ('Why is textContent safer for a user-provided title?','It inserts text without interpreting it as HTML. innerHTML parses markup, so untrusted content needs a suitable sanitisation policy when HTML is genuinely required.')],
 ('Which inserts an untrusted task title as plain text?',['element.textContent = title','element.innerHTML = title','eval(title)','new Function(title)()'],0,'textContent does not interpret the title as HTML or executable code.'),
 ('html','<h1>Local task demo</h1><form id="f"><label for="task">Task</label><input id="task" required><button>Add</button></form><ul id="list"></ul>\n<script>document.getElementById("f").addEventListener("submit",e=>{e.preventDefault();const input=document.getElementById("task");const li=document.createElement("li");li.textContent=input.value;document.getElementById("list").append(li);input.value="";});</script>','Each submitted title is appended as text; HTML-looking input is not executed.'))
 lesson(c,'js-async','Promises, async/await and explicit error handling',r'''
## A promise represents a future outcome
A promise is pending, fulfilled or rejected. then transforms a fulfilled result; catch handles rejection. Returning a promise from a callback chains its result. Forgetting to return/await work can make an operation appear complete before its real work finishes.

An async function always returns a promise. await pauses that async function's continuation; it does not block the browser thread while a genuinely asynchronous operation waits. try/catch handles a rejection only when the promise is awaited within the try or returned through a suitable chain.

## Choose sequencing deliberately
Await one operation before another when the second depends on the first. Use Promise.all for independent work when any failure should reject the group. Use Promise.allSettled when every outcome must be inspected. Neither automatically limits how many operations are started; use a bounded queue for large batches.

## Make failure a visible state
An interface needs loading, success, empty and error states. Translate technical failures into a useful action while preserving diagnostic context for logs. A typed result or discriminated status can make expected failures explicit instead of throwing for every branch. Do not catch an error merely to return fake success.

finally is useful for releasing a loading state, but it should not overwrite a useful return value or mask the original failure. Cancel work that is no longer relevant when the underlying API supports cancellation.
''','Simulate two independent data calls, one failing. Compare all and allSettled, then create UI state objects that distinguish loading, empty, error and successful data.',[
 ('Why does try/catch sometimes miss a promise rejection?','If asynchronous work is started without awaiting or returning it through the handled chain, the try block ends before the rejection occurs. Await inside the try when that is the intended control flow.'),
 ('When is allSettled preferable to all?','When independent outcomes all matter, such as importing several unrelated files. Inspect every settled result and report partial failure rather than ignoring rejected items.')],
 ('What does an async function return?',['A promise','Always a string','Always undefined','A browser tab'],0,'Even a directly returned value is wrapped in the async function\'s promise.'),
 ('javascript','async function load(){\n  const results = await Promise.allSettled([Promise.resolve(7), Promise.reject(new Error("unavailable"))]);\n  console.log(results.map(r => r.status));\n}\nreturn load();','["fulfilled","rejected"]'),skills=[34,39])
 lesson(c,'js-event-loop','Event loop, microtasks and workers',r'''
## One thread can schedule many waits
The browser runs JavaScript tasks on a main thread that also participates in rendering and input handling. A task runs to completion before another ordinary task can interrupt its JavaScript execution. A long loop therefore delays interaction even if a timer was scheduled to fire sooner.

Promise continuations are microtasks. After a task completes, the event loop drains relevant microtasks before moving on to later tasks and rendering opportunities. A timeout delay is a minimum scheduling threshold, not an exact execution time. Repeatedly adding microtasks can also starve other work.

## Move the right work away
A Web Worker can execute code off the main thread and communicate by messages. It does not have direct access to the document DOM. Data is cloned or transferred according to the messaging API; transferring a buffer changes ownership rather than magically making every object shared.

Use a worker for expensive parsing or a code runner and terminate it when cancellation or a time limit requires it. Node.js has its own event-loop phases and worker-thread APIs; do not assume every browser-specific ordering statement transfers unchanged.

When diagnosing lag, identify the long task first. Adding async to a CPU loop does not make the loop nonblocking. Break work into suitable chunks or use a worker, and keep cancellation and error messages part of the design.
''','Predict the example output before running it. Then describe how this app can stop an infinite JavaScript loop without freezing its interface.',[
 ('Why does setTimeout(fn,0) not run immediately?','The callback becomes eligible for a later task after the current work finishes and relevant scheduling rules are satisfied. A zero delay is not an interruption of the current call stack.'),
 ('Can a worker directly modify a button in the page?','No. It communicates with the main thread through messages. The main thread can validate the result and update the DOM.')],
 ('What normally runs first after synchronous code: a promise continuation or a timer task?',['The queued promise microtask','The timer always','They execute simultaneously on the DOM','Neither can run'],0,'Relevant microtasks are drained before later timer tasks are taken.'),
 ('javascript','console.log("A");\nPromise.resolve().then(() => console.log("B"));\nconsole.log("C");\nreturn Promise.resolve();','A\nC\nB'),skills=[35])
 lesson(c,'js-browser','Fetch, cancellation, streams and browser storage',r'''
## Fetch is only the beginning of validation
fetch resolves to a Response for many HTTP error statuses; check response.ok or the expected status before reading a successful payload. Parsing JSON can fail, and parsed data can still have the wrong shape. A weather interface should distinguish invalid search input, no result, a rejected request and a provider outage.

AbortController can cancel a supported request. When a user changes a search quickly, cancel stale work or ignore results that no longer match the current request. Otherwise an older, slower response can overwrite the latest search. Streams let a client process chunks before the whole response is available; chunk boundaries do not necessarily match JSON or line boundaries.

## Choose storage by the data
localStorage stores strings synchronously within an origin. Use JSON serialisation for structured data, handle quota errors and keep writes small. IndexedDB supports larger structured asynchronous storage. Cookies travel with matching HTTP requests and can have server-set HttpOnly/Secure/SameSite controls. Browser JavaScript-readable storage is exposed to successful script injection.

Origins include scheme, host and port. GitHub Pages, localhost and different localhost ports have separate storage. Offline browser saving does not automatically become cloud sync. Export/import or a configured backend is needed to move progress.

Design migrations for saved data: include a format version, validate imported keys and avoid silently replacing current work with an incompatible file. Never place a server API secret in frontend code just because it is minified.
''','Design a weather search state machine with cancellation and a cached last successful result. For an offline-only task app, specify storage keys, a versioned export format and quota-failure behaviour.',[
 ('Why check response.ok after fetch?','An HTTP response such as 404 or 500 can still fulfil the fetch promise. Treating every fulfilled response as successful can turn an error page into an unexpected parsing or application failure.'),
 ('Why does saved progress differ between localhost ports?','The port is part of the origin. Browser storage is isolated by origin, so moving to another port requires a deliberate transfer or a shared local/cloud backend.')],
 ('What is included in a web origin?',['Scheme, host and port','Only the page heading','Only the repository name','Only the browser brand'],0,'Changing scheme, host or port changes the storage/security origin.'),
 ('javascript','const text = JSON.stringify({version:1, tasks:[{id:1, title:"Revise"}]});\nconst restored = JSON.parse(text);\nconsole.log(restored.version, restored.tasks[0].title);','1 Revise'),skills=[42,43])

 c=course('typescript','TypeScript','Frontend engineering','Use types to express contracts, then validate data where it crosses runtime boundaries.','1-2 weeks after JavaScript','Share typed API contracts between a task dashboard and its backend without trusting unvalidated JSON.',['typescript','mdn'])
 lesson(c,'ts-types','Types, unions, narrowing and generics',r'''
## TypeScript checks JavaScript before execution
TypeScript adds a static type system and compiles to JavaScript. Most type annotations are erased; they do not turn external JSON into safe runtime values. Start with strict checking and allow inference where the value is clear.

Use object types/interfaces for shapes, unions for alternatives and literal types for restricted states. An optional property can be absent, which is different from asserting that it always exists. Prefer unknown for untrusted data and narrow it before use; any opts out of useful checking.

## Represent states that cannot be confused
A discriminated union gives each variant a common tag, such as status: loading, error or ready. A switch on that tag lets the checker narrow the available fields. This prevents a component from accidentally reading data from an error state.

Generics preserve a relationship between types: an identity function can return the same type it receives. They are not a reason to make every function abstract. Utility types such as Pick, Omit, Partial and Readonly derive useful shapes, but Readonly is a static view, not a deep runtime freeze.

## A careful boundary
Receive a payload as unknown, validate its shape with code or a schema, then expose a typed internal value. A cast such as `payload as Invoice` asserts your belief; it does not prove that a field exists. Keep missing, loading and failed states visible in the model.
''','Model a request as a discriminated union of loading/error/ready. Write a function that renders every variant and explain how an exhaustive check catches a newly added variant.',[
 ('How do unknown and any differ?','unknown requires narrowing before most operations, so it preserves a safety boundary. any permits unchecked operations and can spread that loss of checking through other code.'),
 ('What is a good use of generics?','To express a meaningful type relationship, such as returning the same element type that an input array contains. A generic with no useful relationship often adds complexity without improving the contract.')],
 ('What does a type assertion do at runtime?',['It performs no automatic validation','It validates every field','It encrypts the object','It converts every string to a number'],0,'Type assertions are erased and do not prove the runtime shape.'),
 ('typescript','type Load<T> =\n  | { status: "loading" }\n  | { status: "error"; message: string }\n  | { status: "ready"; data: T };\nfunction label(state: Load<string[]>): string {\n  if (state.status === "ready") return `${state.data.length} tasks`;\n  if (state.status === "error") return state.message;\n  return "Loading";\n}','Compile in a TypeScript project. Each branch sees only the fields valid for its status.'),skills=[36])
 lesson(c,'ts-contracts','Shared contracts, runtime schemas and monorepos',r'''
## One contract, several consumers
A frontend and backend should agree on field names, nullable values, error shapes and pagination. A shared package can export TypeScript types and runtime schemas. Keep this package free of server-only secrets and dependencies so importing a request type cannot accidentally bundle database code into the browser.

Types reduce accidental disagreement in one codebase, but callers outside that codebase can still send arbitrary values. Use a runtime validator such as Zod at request/response boundaries and derive types from the schema when that reduces duplication. Separate a database entity from a public response so sensitive fields never become public merely through object spreading.

## Evolve safely
Prefer additive optional fields when backward compatibility requires it. Define when old clients stop being supported and how breaking changes are versioned. Generated OpenAPI clients can help with contracts across different languages, but generated code still needs integration checks.

## Repository structure
A monorepo stores related packages together. It needs explicit package boundaries, build ordering and compatible tooling. Path aliases are a developer convenience, not a complete runtime module-resolution policy. A frontend build may resolve an alias that Node does not understand without configuration.

Test the actual serialised request and response, not only that two source files import the same type. Dates, big integers and undefined values have important JSON representation rules that a static type name can hide.
''','Define separate internal User and public UserSummary contracts. Add runtime validation for a task creation body and design one backwards-compatible response change.',[
 ('Why not return a database user object directly?','It may contain password hashes, internal flags or fields never intended for clients. Create an explicit response contract and select only the allowed fields.'),
 ('What does sharing types fail to guarantee?','It does not validate external callers, deployed version compatibility or actual serialisation. Runtime schemas and integration tests are still needed at the boundary.')],
 ('Which belongs in a browser-safe shared contract package?',['Public request/response schemas','A private database password','A server signing key','A production session cookie'],0,'Shared frontend imports must contain public contracts, never server secrets.'),skills=[37,38])

 c=course('git','Git, Linux & Tooling','Engineering workflow','Track changes, collaborate through branches and build a reproducible project.','Git basics: 3-5 days','Publish a portfolio repository with a clear README, useful commit history and a passing CI build.',['git','node','docker'])
 lesson(c,'git-basics','Working tree, staging and useful commits',r'''
## Git records snapshots
The working tree contains files you edit. The index or staging area selects the changes for the next commit. A commit records a snapshot with metadata and parent history. GitHub hosts repositories and collaboration features; Git itself also works offline.

## A normal change cycle
1. Inspect `git status` and `git diff` before editing and before committing.
2. Stage a coherent change with `git add`, then inspect the staged diff.
3. Commit with a message that explains the outcome. Several unrelated changes are harder to review and undo together.
4. Fetch/pull according to the team's workflow, resolve conflicts deliberately and push the intended branch.

Use .gitignore for build output, local environments and secrets. Ignoring a file does not remove a secret already committed in history; rotate exposed credentials and follow a deliberate cleanup process. A README should explain the project, setup, execution, testing and limitations without inventing results.

Remote-tracking references describe fetched remote state. They are not a live view that changes without network communication. Check the branch and remote before a push. Avoid a force push on shared history unless the team has explicitly agreed to that operation.

GitHub Pages serves static assets. A browser app can use it, but it does not run your Python/Node backend or native compiler merely because the files are in the repository.
''','Create a practice repository, commit an About Me page, add a README and ignore a local settings file. Inspect the staged diff before each commit and explain what is and is not being published.',[
 ('How do add, commit and push differ?','add selects changes in the local index, commit records a local snapshot, and push transfers relevant commits/references to a remote. A commit can exist and be useful without any network connection.'),
 ('Does adding a secret to .gitignore remove an earlier leak?','No. The earlier commit can still contain it. Revoke or rotate the credential, then handle history cleanup according to the repository\'s collaboration policy.')],
 ('Which command reviews exactly what is staged?',['git diff --cached','git push --all','git init --force','git checkout --delete'],0,'The cached/staged diff compares the index with the current commit.'))
 lesson(c,'git-branches','Branches, merging, rebasing and conflict resolution',r'''
## A branch is a movable reference
A branch name points to a commit. New commits advance the current branch. Use a feature branch to keep work reviewable without mixing it into a stable branch prematurely. A pull request is a collaboration/review workflow around proposed changes, not a different kind of Git commit.

Merging integrates histories and can preserve their structure with a merge commit. Rebasing replays commits onto another base and creates new commit identities. Rebasing unpublished local work is common; rewriting shared history requires coordination because other people may depend on the old identities.

## Resolve a conflict from intent
1. Read the conflicting versions and understand both changes.
2. Decide the desired combined behaviour, rather than choosing every line from one side automatically.
3. Edit the file, remove conflict markers, stage it and continue the operation.
4. Run the checks relevant to the combined result.

Use `git log --oneline --graph` to understand history. `git restore` and reset have different effects on working tree/index/history, so inspect their scope before using them. Revert makes a new commit reversing an earlier change and is often suitable for a shared branch.

A clean merge does not prove semantic correctness. Two changes can combine without textual conflicts while breaking an API contract or duplicating a side effect.
''','Create two branches that edit the same lesson title, merge them and resolve the conflict intentionally. Then describe why a revert is often easier to collaborate on than rewriting a published main branch.',[
 ('Why does rebasing change commit IDs?','A commit includes its parent and other metadata. Replaying the change onto a new parent creates a new commit object even when the patch looks similar.'),
 ('Can a conflict-free merge still break a feature?','Yes. Textual compatibility does not prove behavioural compatibility. For example, one change may rename a field while another adds a consumer that still expects its old meaning.')],
 ('What is generally appropriate for undoing a bad shared commit?',['A reviewed revert commit','Deleting every teammate\'s branch','A hidden force push without discussion','Editing the remote object database manually'],0,'A revert preserves shared history while recording an explicit reversal.'),skills=[45])
 lesson(c,'tooling-build','Build tools, linting and repeatable commands',r'''
## Separate source, dependencies and output
A package manifest declares scripts and dependencies; a lockfile records resolved versions. Install the project's expected versions rather than relying on a global tool that happens to be installed. A reproducible CI command should work in a fresh checkout.

Vite provides a development server and production build workflow. Bundling groups dependencies for delivery; tree shaking can remove unused exports when the module structure and side-effect information permit it. Source maps support debugging. Minification reduces representation size but does not protect embedded secrets.

## Quality gates have different jobs
Formatting keeps style consistent. Linting catches selected mistakes and enforces conventions. Type checking catches certain contract errors. Tests check behaviour. A build proves that production output can be produced; it does not prove every user journey works.

Define named scripts such as dev, lint, typecheck, test and build so teammates and CI use the same commands. Keep generated output separate from source. Deployment should promote a reviewed build, and environment configuration should identify the intended backend without exposing private server credentials.

## Terminal fluency
Learn your current directory, relative/absolute paths, quoting and exit codes. Linux pipes connect one process's output to another's input; redirection writes or reads streams. Use focused search commands and inspect a path before deleting files. Shell syntax differs between PowerShell and Bash, so copy a command only after identifying its intended shell.
''','Add documented lint, test and build scripts to a sample project. Explain what each check catches, which output folder is deployable and why a frontend environment variable cannot hold a private API secret.',[
 ('Why commit a lockfile?','It records the resolved dependency graph so a clean install can reproduce the reviewed versions. It supports reproducibility, while updates still need testing and security review.'),
 ('Does a successful build prove the app works?','It proves the build pipeline completed. Runtime configuration, permissions, network failures and user workflows can still be wrong, so meaningful tests and deployment checks remain necessary.')],
 ('Which is safe to expose in a frontend bundle?',['A public non-secret API base URL','A database administrator password','A private signing key','A payment webhook secret'],0,'Frontend code and its configuration are delivered to users and must not contain server secrets.'),skills=[44,46])
