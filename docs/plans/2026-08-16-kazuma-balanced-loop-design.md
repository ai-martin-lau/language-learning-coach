# Kazuma-balanced learning loop design

## Goal

Keep the coach recognizably based on Kazuma's public learning sequence while closing the gaps that make a prompt-only method unreliable in real lessons. Validate the revision first with a zero-beginner Korean travel learner.

## Non-goals

- Do not claim official, authorized, or exhaustive reproduction of Kazuma's method.
- Do not add automatic pronunciation scoring without a trustworthy observation tool.
- Do not require Anki, a paid course, or a fixed sequence of all 30 starter functions.
- Do not turn every lesson into a long intake form or a rigid checklist shown to the learner.

## Lesson contract

For spoken-language listening or speaking goals, run this adaptive loop:

1. Retest a due item without revealing the answer.
2. Deliver a playable complete-phrase model before target-language text.
3. Let the learner infer the communicative meaning.
4. Have the learner imitate the whole phrase and, when possible, record it.
5. Build the learner's own answer, a replaceable slot, a likely follow-up, and a repair expression.
6. Require retrieval or transformation with decreasing support.
7. Run a short task-based interaction.
8. Explain one useful pattern from examples already used.
9. Schedule delayed retest and one life-embedded action.

The order may change for sign languages, reading-only goals, classical languages, accessibility needs, or a learner-specific reason recorded in the profile.

## Audio evidence hierarchy

Classify every delivered spoken model as one of:

1. `native_official`: an official or institutional recording by a target-variety native speaker.
2. `native_traceable`: a traceable native-speaker recording in suitable context and register.
3. `tts`: clearly labelled synthetic speech used only as a fallback.

Record source, target variety, delivery method, and what the source actually supports. TTS can support initial perception and rehearsal, but cannot by itself establish native-model imitation or pronunciation mastery. Technical WAV validation remains separate from linguistic reliability and actual playback.

## Learning evidence model

Track evidence separately for:

- listening comprehension;
- spoken production;
- reading;
- writing;
- interaction;
- pronunciation or visual production.

For each tested dimension, store the task, prompt level, result, date, and next retest. Never infer production from comprehension, pronunciation from self-reported repetition, or retention from same-session success.

Each phrase entry also stores its starter-function mapping, learner version, replaceable slot, likely follow-up, and repair expression. A separate function map tracks the 30 Kazuma-style starter functions without forcing a universal order.

## Habit and real-use loop

Do not block the first lesson on habit setup. By the end of the first completed micro-task, fill or explicitly defer:

- a stable daily trigger;
- a minimum five-minute task;
- material that can be opened immediately;
- a fallback action for low-motivation days.

Use solo talk, scenario rehearsal, short diary entries, and interest-linked input as recurring production options. AI role-play is practice, not proof of human interaction; schedule an optional real-person or real-world checkpoint when practical and record only observable evidence.

## Deterministic support

Add a small workspace validator that checks the Markdown state contract without pretending to judge the truth of learner evidence. It should catch missing files or fields, duplicate phrase/function IDs, invalid dimension states, unresolved placeholders paired with advanced mastery, and TTS entries presented as native recordings.

Keep the existing audio validator. Add unit tests for the workspace validator and run the normal Skill validation. Use fresh-agent forward tests for behavior that cannot be proven deterministically.

## Korean evaluation

Continue the existing Korean travel workspace instead of resetting it.

- `T0`: audio-only comprehension, whole-phrase rehearsal, and a hotel interaction.
- `T+24h`: unrevealed retrieval in a shop or restaurant and one changed condition.
- `T+72h`: a different valid audio model plus an unexpected follow-up or repair need.

Judge the Skill by protocol compliance and evidence integrity. Judge learning only from listening, unsupported production, transfer, interaction, and delayed retention samples; do not promise improvement from a single lesson.

## Files in scope

- `SKILL.md`
- `references/session-protocols.md`
- `references/kazuma-method.md`
- `references/evidence-and-guardrails.md`
- `assets/learning-workspace/`
- `scripts/validate_workspace.py`
- `tests/test_validate_workspace.py`
- all five user-facing READMEs
- the current Korean learner workspace, migrated without erasing prior evidence

## Acceptance criteria

- Spoken lessons do not reveal a new target phrase before validated playable audio.
- Every spoken model has a source class and TTS cannot count as native pronunciation evidence.
- Phrase evidence is separated by skill dimension and prompt level.
- The 30 starter functions are trackable but remain goal-adaptive.
- Habit setup, solo production, real-use checkpoints, and delayed tests have explicit protocol steps.
- Workspace and audio validators pass their unit tests.
- Fresh-agent tests cover spoken zero-beginner, reading-only, sign-language, and low-resource exceptions.
- The Korean `T0` lesson can begin from the migrated learner state without inventing mastery.
