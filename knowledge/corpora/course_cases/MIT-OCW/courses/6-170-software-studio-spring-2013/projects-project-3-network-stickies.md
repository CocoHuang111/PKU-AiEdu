- Source: https://ocw.mit.edu/courses/6-170-software-studio-spring-2013/pages/projects/project-3-network-stickies/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects Project 3: Network Stickies

### Overview

Sticky notes have been used for a long time to keep track of small snippets of information in an accessible manner. First introduced in 1980, they were marketed by 3M as [Post-it](http://en.wikipedia.org/wiki/Post-it_note) notes. The idea was carried over to the virtual desktop, with Apple’s [Stickies](http://en.wikipedia.org/wiki/Stickies_%28software%29) and later Windows 7’s [Sticky Notes](http://windows.microsoft.com/en-US/windows7/products/features/sticky-notes). The idea was to create small windows on the screen like Post-it notes where the users can place reminders, notes, clippings, etc.

Now there are note-taking applications on the web (such as [listhings](http://listhings.com/) and [onlinestickynotes](https://www.mural.co/use-case/online-whiteboard?utm_medium=paid-search&utm_source=adwords&utm_campaign=11416478157&utm_campaign_id=11416478157&utm_term=virtual%20sticky%20note%20board&gad_source=1&gclid=Cj0KCQiA0fu5BhDQARIsAMXUBOJuiwJBpSw82dOrjcfalEhSI_c7PyCJ8w6VmVfxBx6shZ_OMykcoaMaAp2bEALw_wcB)) that persist notes on a central server, allowing you to retrieve and update them on any device with internet access. [EverNote](http://www.evernote.com/) is similar, but runs as a standalone app, is more structured, and includes a widget for extracting snippets from web pages.

In this project, you will design and implement your own sticky note application as a JavaScript program running client side, with state persisted on a web server.

### Deliverables

There are four phases to the project. In the first phase, you will lay the groundwork for the second and third phases by constructing a design for both versions. The second phase is an implementation of a “minimal viable product”—a very basic stickies app. The third phase is an extension of your implementation with some features of your own invention. In the fourth phase, you will review your work and the work of a peer.

This is the first project that requires you to include unit tests. You are required to write tests only for controller actions that correspond to Ajax requests.

**Minimal requirements.** Your minimal viable product, implemented in the second phase, should run as a client-side application; that is, it should load as a single web page and should subsequently issue only asynchronous calls.

Furthermore, it should allow the user at least to:

- Create, view and edit a collection of textual notes
- Persist the notes on a centralized server
- Keep notes private from other users

**Extension.** It is entirely up to you what feature or features you choose to add in the third phase. A portion of your grade will be allocated to the quality of your feature(s); emphasis will be placed on clarity and integrity of design and implementation. Novelty will be rewarded, with bonus points that will compensate for lost functionality points, but is not required. Examples of suitable features might include: specialized note types (such as calendar reminders); a search mechanism; automatically arranging notes visually in some way; or excerpting content from web pages.

#### Phase 1: Design of Minimum Viable Product

In the first phase, you will construct a design for both the minimal viable product and for your extension. Your design must very clearly separate the two parts.

**Checklist items.** Of the items specified on the project checklist, you should include in this phase:

- Design: all parts, except for Design/Evaluation, and notes on code design (under Design/Challenges)

#### Phase 2: Implementation of Minimum Viable Product

In the second phase, you will implement your minimal viable product. You will need to revise your design as you discover flaws during implementation. Your revised design document must include clear indications of which parts have changed.

**Checklist items.** Of the items specified on the project checklist, you should include in this phase:

- Programming: all parts, including unit tests
- Design: all parts (except for design critique)

#### Phase 3: Implementation of Extension

In the third phase, you will implement your extension. As before, your revised design document must include clear indications of which parts have changed.

**Checklist items.** Of the items specified on the project checklist, you should include in this phase:

- Programming: all parts, including unit tests
- Design: all parts (except for design critique)

#### Phase 4: Critique

**Minimal requirements.** This phase involves no new design or implementation work. Instead, you will write two short critiques: one of your own work, and one of your peer’s work. In addition to checking the critiques into your own repository, you should post your peer critique as one or more issues in your peer’s repository.

**Checklist items.** You should include in this phase:

- Design/Evaluation/Critique for each of the two projects
- Design/Evaluation/Reflection for your own project
