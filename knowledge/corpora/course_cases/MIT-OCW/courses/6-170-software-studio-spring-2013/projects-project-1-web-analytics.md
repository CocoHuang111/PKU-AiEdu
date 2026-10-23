- Source: https://ocw.mit.edu/courses/6-170-software-studio-spring-2013/pages/projects/project-1-web-analytics/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects Project 1: Web Analytics

### Overview

In this project, you will build a web analytics service that provides people who run websites with data about the type and frequency of visits. Two kinds of analytics tools are available. One kind, which you will build, is a service such as [Google Analytics](http://www.google.com/analytics) or [Stat Counter](http://statcounter.com/) that provides a code snippet to insert in any web page, and then tracks visits to that page. Another kind, such as [AWStats](http://awstats.sourceforge.net/), operates purely on the server side, and tracks requests either by running as part of the application, or by processing web server log files. Open source implementations such as [Piwik](http://piwik.org/) and [OWA](http://www.openwebanalytics.com/) offer one or both forms of tool.

### Deliverables

#### Phase 1: Getting Going

**Minimal requirements.** In this phase, you will implement only the server side of the service. It should support two kinds of HTTP requests:

- `http://myanalytics.com/sites/123/visits`registers a visit to site 123.
- `http://myanalytics.com/sites`returns a simple HTML page listing the identifier numbers of visited sites and the number of visits to each site.

Feel free to add other requests (*e.g*., to create a site) if you need them, and (just for now) to abuse the HTTP verb conventions by using GET for both of these requests, so they can be easily tested by just typing them into a browser’s address bar. Note that “123” is some number representing the site; it is not something more complicated (like a URL).

**Checklist items.** Of the items specified on the project checklist, you should include in this phase:

- Programming/Basic Coding

#### Phase 2: Minimum Viable Product

**Minimal requirements.** In this phase, you will add enough features for a basic, working analytics engine:

- Page-specific data: Your service should be able to track visits to individual pages within a site.
- JavaScript snippet: You should provide a JavaScript snippet that can be inserted into any webpage to notify the service of visits automatically. (We will give you an example of a suitable snippet.)
- Visit duration: Your service should track the average visit duration for each page that it tracks.

**Checklist items.** In addition to refining the items already present from the previous phase, include additionally:

- Programming/Modularity, Design/Overview, Design/Concepts, Design/Challenges

#### Phase 3: (not required for this project)

#### Phase 4: Critique

**Minimal requirements.** This phase involves no new design or implementation work. Instead, you will write two short critiques: one of your own work, and one of your peer’s work. In addition to checking the critiques into your own repository, you should post your peer critique as one or more issues in your peer’s repository.

**Checklist items.** You should include in this phase:

- Design/Evaluation/Critique for each of the two projects
- Design/Evaluation/Reflection for your own project

### Hints

**Get going early.** We very strongly recommend that you get going as soon as you can, so you can get help from the teaching staff and from your colleagues using the Piazza forum, and make good use of the lab hours over the weekend. Whatever you do, do not leave work until the night of the deadline!

**Continuous deployment.** All phases of all projects are to be checked in to your repository and deployed on Heroku. We recommend that you work in a “continuous deployment” mode, pushing to GitHub and deploying repeatedly. This will give you confidence and make it easier for you to assess your progress.

**Exploit Rails support for REST.** If you think of this application in RESTful terms, you will be able to exploit the built-in support for REST in Rails. In particular, in the first phase, you will be able to generate most of the code with a single scaffolding command.

**Transitioning to Phase 2.** Do not expect to keep your code from Phase 1 when you build Phase 2; it might be easier just to start again. In particular, Phase 1 is intended just to get you going, and not to bias you towards any particular way of representing sites or visits.

**JavaScript Snippet.** We are providing you with a [sample JavaScript snippet](https://ocw.mit.edu/courses/6-170-software-studio-spring-2013/pages/projects/project-1-web-analytics/cors-and-js-snippets/), which you can modify and use in your code.

**[JS] Getting information about the current page.** You can find information about the current page in JavaScript via the location variable. For example, try opening a console on a page like [http://www.reddit.com/r/mit](http://www.reddit.com/r/mit) and see what `location.pathname` gets you. (You can also just type location and click the dropdown on the returned object to explore the other properties.)

**[JS] Running code when a user leaves the page.** You will find the following snippet useful to run code right before leaving the page:

```
window.onbeforeunload = function() { // Your code here! }
```

**[JS] Synchronous AJAX requests.** In order to force the browser to wait for the request to complete before leaving the page, inside the `onbeforeunload` handler you will need to set the `async` parameter of the `open()` call to `false`:

`xhr.open('POST', '/your/url', false);`

If you do not, the browser will (most likely) unload the page before the request is able to finish.
