# Adversarial travel-A2 assurance design

## Goal

Make the Skill easy to start in one short session while preventing its saved state or user-facing summaries from claiming more than was actually observed. Give travel learners a visible path from one successful micro-task to broad, delayed, real-world readiness without presenting an internal course as an official CEFR assessment.

## Evidence from the adversarial run

Six isolated scenarios exercised French hotel check-in, Japanese ordering, Egyptian Arabic taxis, Korean convenience-store shopping, German platform changes, and Brazilian Portuguese taxis with no audio. The runs showed that the current lesson loop can start quickly, deliver a small task, adapt to script and dialect, and preserve separate limits for TTS, pronunciation, and AI simulation.

They also exposed four assurance gaps:

1. A task marked as `direct_task` can pass validation while its performance still says that the audio is ready and the learner has not answered.
2. A self-reported “I said it” can upgrade spoken production even though no spoken form was observed.
3. Romanized text can be stored as writing, although it proves neither target-script writing nor audible speech.
4. Individual phrases and Kazuma starter functions do not form a cross-scenario travel-readiness gate, so the workspace cannot support an A2-level conclusion.

The agent runs test protocol behavior and state integrity, not human language acquisition. A genuine learning-effect claim requires a longitudinal human pilot with delayed and preferably real-person tasks.

## Considered approaches

### Documentation-only guardrails

Add more prose to `SKILL.md` and the references. This has the smallest diff, but the six runs demonstrate that soft instructions do not consistently prevent evidence inflation. Rejected.

### Structured observation contract and mission gate

Record how the learner responded, validate that the response medium can support the claimed ability, and add a compact mission map with staged readiness. This keeps the interaction simple while making state claims machine-checkable. Selected.

### Full CEFR scoring engine

Assign numeric scores across descriptors and produce an A2 verdict. This creates false precision, increases maintenance, and risks confusing an internal screen with an official assessment. Rejected.

## Observation contract

Add a `回答媒介` column to every per-skill evidence row. Allowed values are:

- `meaning_response`: a meaning choice, paraphrase, translation, number, or other comprehension response;
- `target_text`: text written in the target language's normal writing system;
- `romanization`: learner-entered romanization or transcription used as an oral-form scaffold;
- `audio`: an audible learner response available to the tutor;
- `action`: an observable task action;
- `self_report`: the learner reports doing something that the tutor did not observe;
- `not_applicable`: no observed response.

The validator will enforce the following minimum logic:

- unresolved or future language such as “waiting for the learner” cannot be substantive evidence;
- `self_report` cannot raise any ability above `new`;
- spoken production and pronunciation require `audio` for a result above `new`;
- writing above `new` requires `target_text`; romanization may be recorded as a scaffold but not writing ability;
- an untested `new` row uses `not_applicable`; a failed observed attempt may remain `new` with its actual medium and a substantive performance note;
- text interaction may support an AI-simulation interaction result, but it does not support spoken production, pronunciation, or real-person interaction.

The user never has to fill this field. The coach records it from the actual response.

## Source assurance

Keep the existing source classes, but require every delivered TTS model to distinguish three facts in the saved source fields:

1. the expression and its usage or register were checked;
2. the selected engine or voice supports the target language and variety;
3. the delivered file or player was technically verified.

TTS remains a labelled rehearsal fallback. A workspace may use it for listening tasks, but TTS-only core material creates a native-model debt that must be resolved before the Skill describes broad readiness.

## Travel mission map

Add a compact `旅行任务地图` table to `progress.md`. It tracks user-selected missions rather than pretending that one universal phrase list is A2. Each mission has a stable `M01`-style ID, task domain, observable victory condition, linked phrase IDs, and one of these states:

- `planned`
- `training`
- `same_session_passed`
- `changed_condition_passed`
- `delayed_passed`
- `field_checked`
- `not_selected`

The default template exposes the high-value domains: transport, lodging, eating, shopping, directions/local geography, communication repair, and basic help. The coach selects only the learner's relevant missions.

State advancement is evidence-bound:

- `same_session_passed` requires an observable independent success;
- `changed_condition_passed` requires a `flexible` result under a meaningful changed condition;
- `delayed_passed` requires a later `retained` result without the answer visible;
- `field_checked` requires successful `real_person` or `real_world_task` interaction evidence;
- no mission state, by itself, is an official CEFR level.

## A2 claim ladder

Use three distinct public conclusions:

1. **Task result:** “You completed this task in the current lesson / under a changed condition / after a delay.”
2. **Internal travel screen:** “Your evidence is consistent with A2-style performance in the tested travel tasks.” This requires multiple unseen tasks across listening, spoken interaction/production, reading, and practical text, sampled across common travel domains and more than one session. Weak or missing dimensions must be named.
3. **Official level:** only an appropriate external assessment can establish a formal CEFR result.

The Skill must not equate selected-mission success with “travel without problems.” Council of Europe descriptors place simple, predictable exchanges at A2 and most travel situations at B1.

## Short-session behavior

For a declared five-minute lesson, introduce at most one learner-required core expression plus one response or repair expression, reach one observable victory condition, summarize only demonstrated evidence, and stop. Habit setup is deferred unless it can replace rather than extend the closing turn. If audio is unavailable and the learner has already explicitly asked to continue with text, the coach may switch to a clearly labelled reading task; otherwise it asks permission before changing modality.

## Repeatable evaluation

Add regression tests for:

- a delivered-but-unanswered task being rejected as evidence;
- self-reported speaking remaining `new`;
- romanization not satisfying writing or spoken-production requirements;
- audio supporting spoken production but not automatically pronunciation;
- mission-state advancement without matching evidence being rejected;
- a valid changed-condition and delayed mission path passing;
- the current template and migrated Korean workspace remaining valid.

Maintain six forward-test personas covering familiar and unfamiliar scripts, a dialect/variety choice, prior knowledge, five-minute constraints, no recording, and no audio. Agent simulations remain protocol tests; human pilots remain the criterion for learning-effect claims.

## Files in scope

- `SKILL.md`
- `references/session-protocols.md`
- `references/evidence-and-guardrails.md`
- `references/language-adaptation.md` only if response-medium handling needs language-specific clarification
- `assets/learning-workspace/phrase-bank.md`
- `assets/learning-workspace/progress.md`
- `scripts/validate_workspace.py`
- `tests/test_validate_workspace.py`
- the existing Korean workspace used as the migration fixture
- READMEs only for the new A2 claim ladder and workspace contract

## Acceptance criteria

- A fully specified beginner can receive the first useful task immediately without repeated intake.
- Spoken goals get playable, labelled audio before text when audio is available.
- The validator rejects future, self-reported, or wrong-medium evidence inflation.
- The saved state distinguishes target-script writing, romanized retrieval, audible speech, and text-only interaction.
- A learner can see which travel missions are planned, trained, changed, delayed, or field-checked.
- The Skill cannot claim an internal A2 screen without broad, multi-session evidence and cannot present that screen as certification.
- Five-minute and no-audio paths end with an honest, useful result.
- All automated tests, templates, migrated workspaces, and audio validation checks pass.
