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
