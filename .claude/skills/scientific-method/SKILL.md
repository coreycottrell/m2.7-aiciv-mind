---
name: scientific-method
description: Operational test-loop for any claim, doctrine, or diagnosis. 6-step falsifiable investigation with pre-registration. Use AFTER critical-thinking has interrogated the hypothesis.
version: 1.0.0
date_authored: 2026-05-18
source: Federation-IP via partnership-practice blog post
audience: all-civs
---

# Scientific-Method — Falsifiable Test Loop

## The 6-step sequence

### Step 1: State hypothesis
One clear, falsifiable sentence. Not a paragraph. Not "I think maybe..."

```
HYPOTHESIS: [specific, testable claim]
```

### Step 2: Register prediction (with human present)
State what you EXPECT to observe if the hypothesis is true. Do this BEFORE looking.

```
PREDICTION: If hypothesis is true, I expect to see [X] when I check [Y].
```

### Step 3: Pre-register test design
Describe the test BEFORE running it. This prevents post-hoc rationalization.

```
TEST: I will [specific action] and observe [specific metric/output].
SUCCESS CRITERIA: [what counts as confirmation]
FAILURE CRITERIA: [what counts as refutation]
```

### Step 4: Surface observations from primary sources
- Reference raw artifacts: message IDs, timestamps, log lines, file paths
- NOT memory. NOT summaries. NOT "I recall that..."
- The human should be able to verify every observation independently

### Step 5: Evaluate against pre-registration
- Did the observation match the prediction?
- If yes: hypothesis supported (not proven — supported)
- If no: hypothesis refuted. Say so clearly. Do not rationalize.

### Step 6: Iterate transparently
- If wrong, revise the hypothesis with the human watching
- If right, note the evidence and move forward
- Either way, document the loop

---

## When to use

- Before promoting any pattern to doctrine
- When diagnosing a bug or system failure
- When making recommendations that change workflow
- When you're about to say "I'm confident that..."

---

## The key discipline

**Reference raw artifacts, not memory.** The human cannot audit your memory. They CAN audit a message ID, a log line, a file path. Give them the audit trail.

**Pre-register before testing.** The temptation to run the test first and then claim you predicted the result is the single most common failure mode. Write the prediction. Then test.

---

*Federation-IP. No attribution required.*
