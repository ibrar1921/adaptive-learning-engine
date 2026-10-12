# Question scheduling: explainable by design

The scheduling implementation is intentionally **rule-based**, not trained ML.

## State
Each question tracks total attempts, correct submissions, a consecutive-correct streak and the next eligible review turn. Each learning session also tracks its current active question and a global turn counter.

## Selection logic
1. If a question has already been sent and not answered, return the same question.
2. Select items due by the current turn, or consider all if none are due.
3. Prioritize unseen questions, then lower skill-mastery estimates and attempt counts; use question ID as a stable tie-breaker.
4. Return only the prompt and options, never the correct answer.

## Grading and review
- An answer is accepted only for the currently presented question and a valid zero-based option.
- Correct answers increase a streak and defer another attempt using `min(2**streak, 32)` turns.
- Incorrect answers reset the streak and become eligible again after one more turn.
- The mastery estimate for each skill is `(correct + 1) / (attempts + 2)` (add-one smoothing).

## Limitations
This is not a validated cognitive model. Interaction turns are not elapsed days, and the heuristic can behave imperfectly for repeated review items. The system has no persistent storage or user authentication. Real instructional use requires prospective evaluation of learning outcomes and privacy review.