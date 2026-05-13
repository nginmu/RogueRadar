[title]Understanding Rogue Radar[/title]

[section]Introduction[/section]

Rogue Radar is a monitoring system built around one central idea:

signals become events, and events become history.

The program listens to wireless activity, transforms raw observations into
structured internal events, distributes those events throughout the system,
and presents the results in a form a human being can actually understand.

At first glance the project may appear large, confusing, or even slightly
unhinged.

This is normal.

Most large systems look frightening when viewed all at once.

The important thing to understand is that Rogue Radar is not one enormous
machine.

It is many smaller machines connected together.

Once you understand the individual pieces, the overall structure becomes
substantially easier to follow.

[section]What the program actually does[/section]

Most of Rogue Radar spends its time waiting.

It waits for something to happen.

Examples include:

- a WiFi device appearing
- a BLE device disappearing
- a signal changing strength
- an identifier returning after a long absence
- suspicious activity patterns emerging
- thresholds being crossed
- timing relationships changing
- devices moving between states

When something interesting occurs, Rogue Radar creates an internal event.

That event is then distributed throughout the system so that different
parts of the interface may react independently.

One subsystem may display the event.

Another may store it in a timeline.

Another may generate alerts.

Another may update statistical information.

The important thing is that these systems remain largely separate.

This separation is one of the major architectural ideas behind the project.

[section]The program is built in layers[/section]

One useful way to understand Rogue Radar is to imagine it as several layers.

The lower layers listen to the world.

The middle layers interpret events.

The upper layers present information to the user.

[chatgpt]
The system intentionally tries to prevent user interface code from directly
interfering with low-level acquisition logic.
[/chatgpt]

This matters more than it may initially appear.

Wireless acquisition systems can become unstable if too many unrelated
systems begin directly manipulating them.

Separating responsibilities keeps the project easier to understand and
substantially easier to repair.

[section]The listener layer[/section]

The lower layers communicate with hardware, scanners, radio devices,
or external monitoring tools.

These parts of the system are responsible for gathering raw information.

Unfortunately, reality is chaotic.

Wireless environments are not clean.

Devices:

- appear suddenly
- disappear unexpectedly
- randomise identifiers
- duplicate advertisements
- change names
- transmit corrupted information
- drift in signal strength
- behave inconsistently

This means the lower layers are often the messiest parts of the system.

They are forced to deal directly with reality.

[warning]
Most acquisition problems originate at the boundary between hardware and
software.
[/warning]

The job of the lower layers is therefore not merely to "collect data".

Their real job is to survive chaos and transform it into something useful.

[section]Events: the nervous system of Rogue Radar[/section]

One of the most important concepts inside Rogue Radar is the event system.

Instead of every subsystem directly controlling every other subsystem,
events are passed around internally.

An event is essentially the program saying:

[code=python]
"Something happened."
[/code]

Different parts of the system can then decide whether they care.

For example:

[code=python]
event_bus.publish("wifi.device.detected")
[/code]

A timeline subsystem may react to this.

An alert subsystem may react to this.

A logging system may react to this.

A statistics panel may react to this.

The WiFi scanner itself does not need to know anything about those systems.

This keeps the project modular.

Without an event system, large software projects often degenerate into a
dense tangled web where every file depends directly on every other file.

Such systems become extremely difficult to modify safely.

[event]
The event bus acts like the central nervous system of the project.
[/event]

[section]Why modular design matters[/section]

Suppose somebody wants to redesign the timeline system completely.

If the project is modular, the timeline can be rebuilt without rewriting
the acquisition systems.

Similarly:

- changing colours should not affect radio scanning
- changing UI layout should not affect BLE parsing
- changing alerts should not affect hardware interfaces

This separation is intentional.

It reduces the likelihood that small modifications will accidentally
damage unrelated systems.

Large projects survive through containment.

[section]The notebook interface[/section]

Most visible areas of Rogue Radar live inside notebook tabs.

Each tab behaves almost like an independent instrument panel.

Some tabs display live data.

Others display timelines, statistics, diagnostics, maps, or archived
events.

Tabs generally:

- receive events
- maintain local information
- update their own displays
- sometimes generate further events

This means individual tabs can often be modified independently without
requiring major changes elsewhere.

[nginmu]
The tabs are less like "pages" and more like interconnected consoles.
[/nginmu]

Some tabs are simple.

Others gradually evolve into entire ecosystems.

[section]Timelines and memory[/section]

A major design goal of Rogue Radar is persistence of behaviour.

Many monitoring tools simply display information temporarily and then
discard it.

Rogue Radar attempts to preserve history.

This allows patterns to emerge over time.

The timeline system gradually transforms momentary observations into
behavioural narratives.

Questions become possible such as:

- When was this device first seen?
- How often does it return?
- How long does it remain active?
- What changed?
- What disappeared unexpectedly?
- What events tend to occur together?
- Are timing patterns consistent?

Over time, raw noise begins turning into structured behaviour.

This is one of the most important transitions inside the system.

[section]The philosophy of the interface[/section]

Rogue Radar intentionally avoids modern web-style design philosophy.

This is not accidental.

The project prioritises:

- clarity
- density of information
- speed
- responsiveness
- readability
- low overhead
- reliability

Modern interfaces often sacrifice useful information density in exchange
for large animated surfaces and excessive spacing.

Rogue Radar instead takes inspiration from:

- engineering consoles
- laboratory equipment
- industrial monitoring systems
- older control software
- technical instrumentation

The interface is intended to feel like a working instrument.

Not a lifestyle product.

[section]Why the project uses plaintext documents[/section]

The internal help system intentionally avoids HTML rendering engines.

Documentation is stored as plaintext BBCode-inspired files.

This has several advantages:

- extremely portable
- easy to edit
- git-friendly
- human-readable
- no browser dependency
- consistent rendering
- easy to archive
- easy to search

The rendering system itself is deliberately lightweight.

Tags are translated into Tkinter text formatting internally.

This keeps the documentation system closely integrated with the rest of
the project.

[tip]
A plaintext documentation system also makes experimental extensions easier
to implement later.
[/tip]

Possible future additions could include:

- internal hyperlinks
- embedded images
- searchable indexes
- collapsible sections
- timeline-linked entries
- inline diagnostics
- event references

[section]Configuration files[/section]

Configuration files act as the central memory of the project.

Instead of scattering important values everywhere, Rogue Radar attempts to
keep major settings centralised.

Examples include:

- tab names
- colour definitions
- timing thresholds
- refresh rates
- UI labels
- feature toggles
- paths
- display behaviour

This makes the system easier to customise and easier to maintain.

A well-designed configuration system also reduces accidental duplication.

[chatgpt]
Centralisation reduces the number of places where errors can hide.
[/chatgpt]

[section]Why things sometimes break[/section]

Large event-driven systems are complicated because many things happen
simultaneously.

Sometimes one subsystem changes state while another subsystem is still
processing older information.

Sometimes duplicated events appear.

Sometimes hardware behaves unpredictably.

Sometimes wireless devices themselves behave like tiny malevolent ghosts.

This is normal.

Monitoring software exists at the boundary between software and reality.

Reality is unreliable.

[warning]
Many apparent software bugs are actually environmental behaviour.
[/warning]

The challenge is therefore not eliminating chaos entirely.

The challenge is surviving it gracefully.

[section]Safe areas for exploration[/section]

If you are curious and want to explore the project yourself, there are
many relatively safe areas where experimentation is unlikely to cause
major damage.

Examples include:

- help files
- themes
- colours
- labels
- UI layout
- timeline formatting
- configuration values
- tab naming
- display behaviour

These areas are excellent places to begin learning how the project fits
together.

[section]Areas requiring greater care[/section]

Some parts of the system are more sensitive.

Examples include:

- acquisition threads
- radio interfaces
- hardware timing
- event dispatch systems
- parser logic
- threading behaviour
- shared state management

Changes in these areas can produce subtle instability.

Not because the code is cursed.

Usually.

But because timing-sensitive systems are naturally more fragile.

[section]How to learn a large system[/section]

Many people make the mistake of trying to understand an entire project
simultaneously.

This usually leads to despair.

Instead:

- choose one subsystem
- follow one event
- trace one code path
- modify one behaviour
- observe the result

Gradually the structure becomes clearer.

Understanding grows layer by layer.

[claude]
Most complex systems eventually become understandable if approached
incrementally.
[/claude]

[section]Experimentation is allowed[/section]

Software projects are not sacred untouchable artefacts.

Rogue Radar itself was built through experimentation, redesign,
replacement, failure, repair, and repeated architectural mutation.

Many useful systems begin life as:

[quote]
"I wonder what happens if I try this."
[/quote]

The safest approach is simple:

- duplicate files before editing
- change one thing at a time
- keep notes
- test frequently
- avoid changing multiple subsystems simultaneously

This dramatically improves survivability.

[section]The long-term direction of the project[/section]

Rogue Radar is gradually evolving toward a more unified behavioural
monitoring environment.

The long-term direction includes ideas such as:

- richer timelines
- stronger event correlation
- improved visualisation
- behavioural clustering
- internal search systems
- historical analysis
- mapping systems
- extensible protocol support
- modular subsystem expansion

The architecture intentionally tries to leave room for future mutation.

Large systems survive by remaining adaptable.

[section]Final notes[/section]

If Rogue Radar initially appears intimidating, remember:

every large system is ultimately composed of small understandable parts.

You do not need to understand everything simultaneously.

Start small.

Read one file.

Follow one event.

Rename one tab.

Change one colour.

Observe what happens.

That is how people gradually learn systems like this.

[section]How Rogue Radar stores information[/section]

One of the easiest mistakes to make when looking at a monitoring system is
to imagine that information exists in only one form.

In reality, the same information often exists in several different forms
as it moves through the system.

A wireless signal may begin life as raw radio activity.

Later it becomes parsed data.

Then an internal event.

Then a timeline entry.

Then perhaps a database record.

Then finally a line displayed on screen.

Understanding these transformations makes the project substantially easier
to follow.

[section]Raw data[/section]

At the very bottom of the system is raw acquisition data.

This is the closest layer to reality.

Examples include:

- packet captures
- BLE advertisements
- beacon frames
- RSSI values
- timestamps
- SDR sample streams
- device identifiers
- protocol metadata

Raw data is usually messy, repetitive, incomplete, or unreliable.

Real wireless environments are noisy.

Devices frequently transmit malformed or contradictory information.

Signal strength fluctuates constantly.

Packets are lost.

Identifiers change unexpectedly.

The lower acquisition layers therefore spend much of their time attempting
to stabilise chaos into something more usable.

[warning]
Raw acquisition data is usually too unstable to display directly without
some form of filtering or interpretation.
[/warning]

[section]Parsed data structures[/section]

Once raw information is received, the next stage is usually parsing.

Parsing means converting chaotic low-level information into structured
internal data.

For example, instead of:

[code=python]
b'\\x42\\x19\\x7a\\x88\\x00\\xff...'
[/code]

the system may instead produce something closer to:

[code=python]
{
    "device_type": "BLE",
    "mac": "AA:BB:CC:DD:EE:FF",
    "rssi": -63,
    "timestamp": 1747000000
}
[/code]

This is much easier for the rest of the project to work with.

At this stage the data still represents immediate observations rather than
historical knowledge.

The system is essentially saying:

[event]
"This is what we just observed."
[/event]

[section]Transient memory structures[/section]

Large amounts of Rogue Radar operate using temporary in-memory structures.

These are fast-changing collections of live information stored while the
program is running.

Examples include:

- currently visible devices
- rolling signal histories
- recent events
- active alerts
- timing windows
- temporary caches
- deduplication tables
- event queues

These structures usually exist only while the application is running.

When the program closes, they may disappear entirely unless explicitly
saved elsewhere.

Transient memory is extremely important because it allows the system to
react quickly without constantly writing everything to disk.

[chatgpt]
Fast temporary memory structures are often used to absorb high-frequency
event traffic before long-term storage occurs.
[/chatgpt]

[section]State versus history[/section]

A useful distinction exists between state and history.

State describes what the system currently believes.

History describes what previously occurred.

For example:

Current state:

- device currently visible
- signal currently strong
- alert currently active

Historical data:

- first seen yesterday
- signal dropped repeatedly
- alert triggered six times this week

Many internal structures exist specifically to bridge these two ideas.

The timeline system is heavily concerned with history.

Live monitoring tabs are more concerned with state.

[section]Event objects[/section]

Once parsed data becomes meaningful, Rogue Radar often transforms it into
events.

Events are one of the central currencies of the system.

An event usually contains information such as:

- source subsystem
- event type
- timestamp
- severity
- metadata
- associated identifiers
- contextual information

An event may look conceptually like:

[code=python]
event = {
    "type": "wifi.device.detected",
    "timestamp": 1747000000,
    "mac": "AA:BB:CC:DD:EE:FF",
    "rssi": -61
}
[/code]

The important idea is that events are portable.

They can move throughout the system independently of the original hardware
that generated them.

[section]The event bus[/section]

The event bus acts like a distribution network for events.

Subsystems publish events into the bus.

Other subsystems subscribe to events they care about.

This means information flows through the project dynamically rather than
through rigid direct connections.

The event bus therefore becomes one of the major highways inside the
system.

Without it, the project would become substantially more tangled.

[event]
Acquisition systems create events.
The event bus distributes them.
Other systems react.
[/event]

[section]Why events are useful[/section]

Events decouple systems from one another.

For example:

the BLE scanner does not need to know how the timeline works.

It merely publishes events.

Similarly:

the timeline system does not need to understand radio hardware.

It merely reacts to events.

This separation dramatically improves maintainability.

It also allows entirely new subsystems to be added later without rewriting
existing acquisition logic.

[section]Caching systems[/section]

Some information inside Rogue Radar exists only to improve performance.

These temporary structures are often called caches.

Caches may store:

- recently seen devices
- previously resolved names
- recent signal values
- historical lookups
- rendered timeline entries
- deduplicated identifiers

Caching prevents the program from repeatedly recalculating expensive
operations.

Without caching, event-heavy systems can become sluggish very quickly.

[section]Deduplication[/section]

Wireless environments often generate repeated information.

The same device may transmit many times per second.

Without filtering, the timeline would rapidly become unusable.

Deduplication systems therefore attempt to suppress unnecessary repetition.

For example:

- repeated identical BLE advertisements
- identical signal reports
- repeated unchanged device states

This allows the timeline to focus on meaningful changes rather than raw
spam.

[warning]
Overly aggressive deduplication can accidentally hide important behaviour.
[/warning]

Balancing signal reduction against information loss is one of the ongoing
challenges in monitoring systems.

[section]Timeline storage[/section]

The timeline system acts as the historical memory of the project.

Events entering the timeline may be:

- stored temporarily
- rendered visually
- filtered
- grouped
- archived
- exported
- written to databases

The timeline transforms momentary observations into navigable history.

This is where the system begins moving away from pure live monitoring and
toward behavioural analysis.

[section]Databases and persistent storage[/section]

Not all information should remain only in memory.

Some data becomes valuable over long periods.

Examples include:

- historical sightings
- recurring identifiers
- behavioural patterns
- alert histories
- session archives
- long-term statistics

Persistent storage systems exist so that information survives after the
program closes.

Different projects solve this differently.

Some use:

- SQLite
- JSON files
- structured logs
- binary archives
- CSV exports
- custom storage systems

Rogue Radar may eventually use several forms simultaneously depending on
the type of information involved.

[section]Why everything is not stored forever[/section]

A common beginner assumption is:

[quote]
"Surely we should store absolutely everything."
[/quote]

Unfortunately this becomes impractical very quickly.

Wireless monitoring systems can generate enormous quantities of data.

Continuous raw storage may eventually produce:

- huge databases
- slow searches
- memory exhaustion
- storage exhaustion
- difficult timelines
- unusable interfaces

This means monitoring systems must constantly decide:

- what to keep
- what to summarise
- what to compress
- what to discard

These decisions form a major part of system design.

[section]Live data versus archived data[/section]

Live data prioritises speed.

Archived data prioritises durability.

These goals are often in conflict.

Live systems need rapid updates and low latency.

Archive systems need efficient storage and reliable retrieval.

Large monitoring platforms therefore often separate live processing from
historical storage entirely.

Rogue Radar increasingly moves in this direction as the architecture grows.

[section]Queues and buffers[/section]

Events do not always move instantly from one subsystem to another.

Sometimes temporary holding structures are required.

These may include:

- queues
- rolling buffers
- ring buffers
- event pipelines
- temporary stacks

These structures smooth out bursts of activity.

For example:

a wireless scan subsystem may suddenly detect hundreds of events at once.

Without buffering, downstream systems may become overwhelmed.

Buffers help stabilise flow through the architecture.

[section]Threading and shared state[/section]

One reason large monitoring systems become complicated is that multiple
things may happen simultaneously.

Scanning systems may run in parallel.

UI systems may refresh independently.

Timeline systems may archive events asynchronously.

This creates the problem of shared state.

Two systems attempting to modify the same data simultaneously can produce
instability.

This is why event-driven architectures are often preferred.

They reduce direct shared manipulation.

[warning]
Concurrency problems are often subtle and difficult to reproduce.
[/warning]

Many mysterious bugs originate from timing interactions rather than obvious
logic errors.

[section]Why the timeline matters so much[/section]

Without timelines, monitoring systems remain trapped in the present moment.

A timeline allows the system to develop memory.

Once memory exists, patterns become visible.

Questions become possible such as:

- What repeats?
- What changed?
- What vanished?
- What returned unexpectedly?
- What behaviour is unusual?

This is where monitoring gradually becomes analysis.

[section]The flow of information through Rogue Radar[/section]

One possible simplified path through the system may look something like:

- hardware receives signal
- acquisition layer captures data
- parser interprets data
- event object created
- event bus distributes event
- live tabs update
- timeline stores event
- alerts evaluate conditions
- archive system persists important history
- user eventually sees result

Understanding this flow is one of the keys to understanding the project
as a whole.

[section]Final notes on data flow[/section]

The important thing to remember is that information changes shape many
times as it moves through the system.

Raw radio noise eventually becomes structured history.

Transient observations become persistent behavioural records.

Live events become timelines.

Timelines become analysis.

Once you begin seeing those transformations, the overall architecture of
Rogue Radar starts becoming much easier to understand.