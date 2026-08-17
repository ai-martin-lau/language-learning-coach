# Universal Sound–Script Foundation Lane Design

## Context

The current Skill correctly says that sound and writing should progress together, that transliteration is temporary, and that a learner should not have to finish an alphabet before communicating. It does not yet define a repeatable sequence or persistent state for this foundation work. In practice, a tutor can therefore drift toward one of three weak extremes: front-loading a complete chart, postponing writing indefinitely, or inserting isolated letters without cumulative review.

The approved scope is universal. Every supported language should connect reliable language input to its normal written form. The concrete learning unit changes by language: Hangul jamo and syllable blocks, kana and contextual kanji readings, Arabic joining forms, Chinese words and character components, or spelling–sound, stress, and connected-speech patterns in Latin-script languages. “Universal” means shared invariants, not one alphabet lesson copied across languages or goals.

## Goals

- Preserve the Kazuma-inspired order: a useful complete chunk and its sound come first for spoken goals; a small form-focused step follows and returns immediately to the chunk.
- Give every language a cumulative sound–script foundation lane without delaying the first real communication task.
- Keep transliteration temporary and record an explicit fade action.
- Revisit introduced units or patterns in later no-answer tasks.
- Keep listening, reading, writing, spoken production, interaction, and pronunciation evidence separate.
- Preserve the existing four-file learner workspace.

## Non-goals

- Do not create a fixed alphabet, kana, character, or phonics curriculum shared by all languages.
- Do not require learners to memorize a complete chart before using the language.
- Do not make a chart or isolated-symbol score a travel A2 gate.
- Do not treat typed transliteration, target-script copying, TTS rehearsal, or self-report as audible speech or pronunciation evidence.
- Do not add a fifth workspace file or duplicate phrase-bank mastery evidence.

## Approaches considered

### 1. Instruction-only guidance

Add a clearer lesson loop to the adaptation reference but save no new state. This is the smallest edit, but a future session cannot reliably know which symbols or spelling patterns have already been introduced or what must be retested. Rejected because it does not solve cumulative foundations.

### 2. Lightweight lane in `progress.md`

Add one planning table that records a small unit or rule group, its known phrase anchor, the current transliteration support, the first lesson date, and the next no-answer retest. Keep actual ability evidence in `phrase-bank.md`. This makes continuation deterministic without creating a second mastery system. Selected.

### 3. Separate script curriculum file

Add a fifth file with a full language-specific sequence. This can model a formal literacy course, but increases onboarding, migration, validation, and duplication for a travel-first self-use Skill. Rejected as unnecessary for the current goal.

## Universal lesson loop

For spoken goals with playable sound, run the following sequence:

1. Present one complete, useful expression as verified playable sound before showing target text, transliteration, translation, or the answer.
2. Ask for one meaning or task response.
3. Reveal the normal target text and, only when needed, a temporary transliteration aid.
4. Extract one small high-value sound–form unit or rule from that already understood expression. A group contains one to five learning units or one compact pattern, not necessarily one to five characters.
5. Return immediately to the expression for one recognition, segmentation, reconstruction, or substitution action. Isolated contrast practice may be brief, but it cannot replace the whole chunk.
6. Remove or reduce transliteration in the same lesson when feasible.
7. Schedule a later no-answer task that tests the unit or pattern in a changed position, word, sign, or nearby expression.

Pure reading, writing, accessibility, and audio-unavailable cases change the entry medium according to the existing adaptation rules. They still connect form to a real task and do not fabricate sound or pronunciation evidence.

Only one new foundation micro-target should normally appear in a travel-first lesson. Reading-focused goals may increase the amount when the learner’s performance supports it.

## Language-specific interpretation

- **Hangul:** introduce a few jamo or one syllable-block construction from a known chunk, then recombine them in that chunk or a nearby block. Do not dump the full consonant and vowel charts.
- **Japanese:** introduce a small mora/kana contrast from a known chunk; teach kanji as a whole word form, meaning, and contextual reading. Do not force kanji through an alphabetic model.
- **Arabic:** fix region and register first; teach right-to-left direction and joining forms inside a verified word or chunk. Do not infer full pronunciation from an unvowelled spelling.
- **Chinese:** connect a known spoken word or chunk to its normal characters and a small high-value form distinction. Treat pinyin as temporary support, not target writing, and do not present characters as alphabetic spelling.
- **Latin, Cyrillic, Greek, Hebrew, Devanagari, and Thai scripts:** if the learner already knows the character inventory, use the lane for the target language’s spelling–sound mappings, stress, silent letters, segmentation, or connected-speech cues rather than reteaching the alphabet.

## Workspace contract

Add `## 声音—文字基础支线` to `progress.md` with this table:

| 支线编号 | 类型 | 学习单位或规律 | 锚定语块 | 当前转写支架 | 首学日期 | 复测任务 | 答案可见性 | 复测转写支架 | 变化条件 | 到期日 |
|---|---|---|---|---|---|---|---|---|---|---|

- IDs use `S01`, `S02`, and so on.
- Type uses `symbol_sound`, `spelling_sound`, `stress`, `connected_speech`, or `form_component`.
- `学习单位或规律` contains one to five semicolon-separated learning units or one compact rule description; it cannot be a placeholder.
- `锚定语块` references one existing phrase ID whose context, target expression, and communicative function are substantive. The foundation item must come from a real learned or planned chunk rather than an unrelated chart. Sound-related types require that phrase to carry a complete reliable audio-source record.
- `当前转写支架` and `复测转写支架` use `full`, `partial`, `none`, or `accessibility_required`. The retest must reduce non-accessibility support: `full` to `partial` or `none`, `partial` to `none`, and `none` remains `none`; `accessibility_required` may remain or become `none`.
- `首学日期` is an ISO date with a matching lesson heading and cannot be in the future.
- `复测任务` is concrete, `答案可见性` is exactly `hidden`, and `变化条件` records the changed position, word, sign, or nearby expression separately from the task.
- `到期日` is an ISO date later than the first-learning date.

The table tracks coverage and scheduling, not mastery. Reading, writing, listening, spoken-production, interaction, and pronunciation results remain in `phrase-bank.md` with their existing media and source gates. A foundation row cannot by itself advance a phrase, travel mission, or A2-style screen.

Legacy workspaces receive the section additively. Existing lessons, evidence, notes, and user-written content stay untouched. A missing section is added with an empty row; existing evidence must not be reverse-engineered into invented foundation history.

## Validation

Extend `validate_workspace.py` to check:

- exactly one correctly headed foundation table;
- empty template rows remain valid;
- unique `S01+` IDs;
- the type and transliteration enums;
- substantive, bounded learning units or a compact rule;
- a substantive existing phrase reference and complete audio source for sound-related types;
- ISO first-learning and due dates, a matching real lesson heading, no future first-learning date, and a due date later than first learning;
- a substantive retest, exact hidden-answer declaration, concrete changed condition, and transliteration-support reduction.

The validator will not infer whether a free-text retest accidentally reveals an answer or whether a linguistic explanation is correct. Those remain protocol and human-review boundaries.

## Documentation and forward tests

Update the core Skill, language adaptation, session protocol, evidence guardrails, workspace template, validator tests, and five README languages. Add forward-test scenarios for at least:

- Korean without Hangul;
- Japanese without kana;
- Egyptian Arabic without Arabic-script literacy;
- French or German with familiar Latin letters but unfamiliar spelling–sound patterns;
- Mandarin without Chinese-character literacy;
- a pure signage-reading exception and an audio-unavailable case.

Each spoken scenario must reach a useful travel task quickly, deliver sound before new target text, introduce no more than one new foundation micro-target in the lesson, include a transliteration fade action where applicable, schedule a later no-answer foundation retest, and keep response media from upgrading unrelated abilities.

## Acceptance criteria

- A fresh tutor can continue the travel task while building cumulative sound–script foundations in every supported language family.
- It never requires a full chart before communication and does not leave a learner indefinitely in transliteration.
- Existing workspace validation remains backward-migratable without invented evidence.
- All unit tests, quick validation, template validation, the current Korean workspace, audio checks, and fresh-agent forward tests pass.
