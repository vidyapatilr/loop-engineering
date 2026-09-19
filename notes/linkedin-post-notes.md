# Notes for the LinkedIn post

Running list of real observations from building this, for the writeup.

## The Reviewer approved a weak example (real finding, not hypothetical)

- Iteration 2 was APPROVED by the Reviewer. The rubric line for "concrete example" only
  checked "does it include at least one worked example?" - a yes/no box.
- The worked example it approved was a generic multi-turn chat (planning a trip: "tell me
  more about Paris" -> "what about hotels" -> ...). That's a conversation, not an agent loop:
  no visible tool call, no observed result fed back in, no stopping condition being checked.
- The automated judge passed it anyway, because it was only checking for presence of an
  example, not whether the example actually demonstrated loop mechanics.
- Caught by manual review after "approval" - i.e. verification loops reduce how much you
  have to check by hand, they don't eliminate the need for it. "Approved" != "correct."
- Good honest angle for the post: this is the verification-debt point the article itself
  raises - a loop that "passes" can still ship something wrong if the rubric doesn't check
  the right thing.

## Screenshot idea for the post
- Before: the generic trip-planning example (site/index.html from iteration 2, or
  iterations/iteration_2/index.html)
- After: the tightened example once the rubric is fixed and the loop re-runs
- Caption idea: "My own verification loop approved this - and it was still wrong."

## Credits
- Akshat: shared the demo/doc link that got this whole thing started - thank in the post.

## Diagram before/after (second pair for the post)
- Before: original "simple diagram" from the current site/index.html or
  iterations/iteration_2/index.html - generic/decorative, doesn't show distinct loop
  stages or the stop/continue paths.
- After: once the GOAL and Reviewer rubric are tightened to require labeled stages
  (context -> model -> tool calls -> results -> stop check) connected in a cycle, with
  stop/continue paths visually distinguished.
- Same narrative as the example fix: the rubric only checked "is there a diagram?" not
  "does the diagram actually show the mechanism?" - another concrete instance of the same
  underlying lesson (a judge is only as good as what it actually checks for).

## Stale copyright year (another real finding)
- The Builder's first draft included a footer with "(c) 2023 ..." even though nothing in
  the GOAL asked for site boilerplate at all.
- Why: the model doesn't know today's date, but has seen countless real websites with a
  copyright footer in training - so it pattern-matches "this is what a real webpage looks
  like" and adds one anyway, defaulting to some plausible-sounding but arbitrary year.
- Fix: had to explicitly tell the Builder in the GOAL not to add site-wide boilerplate
  (no fake copyright, no placeholder nav bar, no About/contact footer) - the model won't
  omit it just because it's irrelevant to the actual task; it has to be told.
- Good angle for the post: this is a small, concrete example of "context engineering" /
  prompt design - even a single-purpose content-generation loop inherits the model's
  learned habits about what a "complete" output looks like, and the loop designer has to
  explicitly rule those out rather than assuming the model will only do what was asked.

## The Reviewer hallucinated verification it never actually did (strongest finding)
- After tightening the rubric, the Builder's very first draft was APPROVED with zero
  revision - and the page was worse than the earlier version: the worked example was
  completely absent, and the diagram's stage labels were invisible.
- Root cause of the invisible labels: the Builder used SVG <title> (a hover tooltip,
  never rendered visibly) instead of <text> for the box labels. It "labeled" the boxes
  in the markup, just not in a way that shows on screen.
- The Reviewer's approval message explicitly claimed the page "includes a concrete
  example" and the diagram "clearly shows the distinct stages" - neither was true.
- Why: the Reviewer only ever reads raw HTML/SVG source text. It never sees a rendered
  page. It reasoned from the presence of a label string in the markup and concluded it
  was "shown," with no way to know a <title> tag is invisible to an actual viewer.
- This is the sharpest example of the article's own "reward hacking" / verification-debt
  warning: a text-based LLM judge can be fully confident and articulate about a claim
  that is simply false, because it is verifying against the wrong artifact (source code)
  for a question that's actually about the rendered result. A judge's confidence is not
  evidence.
- Practical fix for a "real" system: either render the page (e.g. headless browser
  screenshot) and have the Reviewer look at the rendered image, not just the source, or
  add a deterministic/rule-based check (e.g. "reject any <title> used as a label
  substitute") alongside the LLM judge - matching the article's point that loops often
  need BOTH a deterministic guardrail AND an LLM judge, not just one.

## Closing lesson: not every task is a good fit for a self-correcting loop
- After tightening the Reviewer's rubric to demand a "detailed" SVG diagram, the diagram
  broke in a NEW way on almost every subsequent run: invisible labels (<title> instead of
  <text>), then an unconstrained size that blew up the page, then the diagram's position
  shuffled in the page, then arrows that crossed randomly with a disconnected box.
- Each fix addressed the specific failure from the last run, but the loop never converged
  on a genuinely good diagram - it kept trading one problem for a different one.
- Why: precise SVG geometry (box positions, line coordinates, label placement) is a task
  neither side of the loop can actually verify by looking at it. The Builder writes
  coordinates blind, without ever seeing the rendered result; the Reviewer reads the same
  raw markup, also without ever seeing it rendered. Two blind participants can't catch
  what only becomes obvious once you look at the actual page.
- Decision: stop iterating on the diagram through the loop and hand-place a simple,
  known-good flowchart instead, keeping the loop for what it's actually good at (the
  prose content: clarity, examples, jargon).
- This is the real, honest closing point for the post: knowing when to stop trusting a
  loop to self-correct - and recognizing which tasks are and aren't a good fit for one -
  is itself the skill, not just building the loop in the first place.
