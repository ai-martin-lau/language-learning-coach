# Travel A2 README visual refresh design

## Goal

Reposition the project around a clear first use case: learners who want the shortest practical route into predictable travel communication in a well-resourced modern language. Present that route visually in all five READMEs without turning an executable Skill into a long textbook.

The Chinese-facing positioning may use “主流小语种” as the audience shorthand. Other languages should use natural local wording such as “travel languages” or name representative languages rather than translate the Chinese category literally.

## Claim boundary

The primary promise is:

> Build verifiable foundations for simple, predictable travel communication as efficiently as the learner's starting point, target language, practice time, and demonstrated performance allow.

The course uses common CEFR A2 can-do descriptors as a reference for tasks such as asking directions, buying tickets, checking in, ordering, shopping, and making simple requests. “Travel A2” is a project route, not an official CEFR sub-level or a certificate.

Do not claim:

- a fixed number of days to A2;
- that completing the course itself proves A2;
- stress-free travel in every situation;
- the ability to handle most unexpected travel problems, which is closer to the CEFR B1 global descriptor;
- equivalent source quality or learning speed across languages.

Use “faster practical route”, “build the foundations quickly”, or “more confidently in common, predictable situations” only alongside the evidence and variability boundary.

## Information architecture

Keep installation, privacy, evidence, and repository details, but move the learner's decision path before them:

1. Language switcher.
2. Original travel hero and one-sentence positioning.
3. Scope, A2 boundary, and non-affiliation notice.
4. Six travel outcomes: transport, accommodation, food, directions, shopping, and communication repair.
5. Quick start.
6. Adaptive route from goal to delayed transfer.
7. One real lesson storyboard.
8. Separate skill evidence and A2 interpretation.
9. Sound-source trust model.
10. Installation, workspace, method, privacy, repository, contribution, and license.

The README remains a map to the Skill. It should not duplicate the full protocols already stored in `references/`.

## Visual system

Use a hybrid system with one generative illustration and four deterministic SVG groups:

1. `travel-hero.webp`: an original, text-free editorial illustration linking a train station, hotel desk, and restaurant. It creates emotional context but is not presented as a real learner or testimonial.
2. `travel-scenarios.svg`: six compact, text-free scene tiles for the prioritized travel tasks.
3. `adaptive-loop.svg`: the course loop from real task through reliable input, retrieval, interaction, focused feedback, redo, and delayed transfer.
4. `lesson-storyboard.svg`: a four-panel example showing model, learner attempt, one focused correction, and changed-condition retry.
5. `evidence-ladder.svg`: separate evidence dimensions and the progression from supported performance to delayed transfer.

All SVGs should use explicit dimensions, accessible shapes, restrained gradients, and no embedded localized copy. Localized Markdown headings, alt text, captions, and legends carry the language. The five README variants therefore share one asset set without text drift.

The visual language should be original: travel-route lines, passport-stamp geometry, rounded cards, and a navy/coral/teal/sand palette. Do not copy `byoungd/up` artwork, wording, color assignments, or layout details. The transferable pattern is only its scannable visual navigation and progressive disclosure.

## Learning route

The README should expose the same protocol the Skill actually runs:

1. Pick a real travel task and target variety.
2. Hear a complete, classified model before reading when the goal is spoken.
3. Understand the intent and one critical detail.
4. Acquire one to three complete phrases with replaceable slots.
5. Retrieve and transform them with fading prompts.
6. Complete a short interaction with a likely follow-up and a repair expression.
7. Receive one or two task-critical corrections and redo immediately.
8. Retry later with a changed city, time, item, person, or condition.

The route should prioritize transport, accommodation, food, directions, shopping, numbers and time, and communication repair. Serious medical, legal, immigration, and safety emergencies remain outside any A2 sufficiency claim.

## A2 evidence

README copy must distinguish course direction from demonstrated performance. Listening, spoken production, reading, writing, interaction, and pronunciation remain separate. A task may count only for the dimension, prompt level, environment, transfer, and delay actually observed.

The minimum public description of progress is:

- supported rehearsal;
- independent completion of the same task;
- completion under a changed condition;
- delayed retention;
- optional confirmation with a real person or real-world task.

AI role-play is practice evidence, not proof of human interaction. TTS is a labelled rehearsal fallback, not native-speaker or pronunciation evidence.

## Files in scope

- `README.md`
- `README.zh-CN.md`
- `README.ja.md`
- `README.ko.md`
- `README.es.md`
- `assets/readme/`
- `SKILL.md` and reference files only if a README promise is not already enforced by the runtime contract

## Acceptance criteria

- A new visitor can identify the travel A2 audience, supported language scope, six core scenarios, first command, lesson loop, and claim boundary before reaching installation details.
- All five READMEs have equivalent meaning and use the same visual assets.
- No image impersonates a real learner, testimonial, result, partner, or Kazuma endorsement.
- All image paths render on GitHub and all SVGs parse and rasterize successfully.
- The README does not claim fixed-time A2 attainment or universally stress-free travel.
- Existing Skill and workspace validation tests continue to pass.
- The final diff stays limited to the visual/readme positioning task and any strictly necessary runtime alignment.
