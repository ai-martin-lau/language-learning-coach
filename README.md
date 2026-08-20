[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

# Language Learning Coach

**Start from zero. Prepare free audio, choose one real goal, and build verifiable A2 foundations through the shortest practical route your performance supports.**

Language Learning Coach is an adaptive Codex Skill for learning well-resourced modern languages through real tasks, reliable input, useful phrases, active recall, interaction, focused feedback, and delayed retests.

It supports well-resourced modern languages such as French, German, Italian, Spanish, Portuguese, Korean, Japanese, Arabic, and English. Daily life, travel, work, study, exams, reading, writing, media, heritage, and personal interest are all valid routes. The language, regional variety, writing system, goal, time available, and what you can actually do all change the lesson.

> [!IMPORTANT]
> The internal A2-style screen is not an official CEFR sub-level or certificate. A2 covers simple, direct exchanges in familiar and routine situations. For an optional travel route, note that the CEFR places coping with most situations likely to arise while travelling at B1; this Skill never promises stress-free handling of every trip or emergency. See the Council of Europe's [global scale](https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale) and [spoken-language descriptors](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use).

> [!NOTE]
> This is an independent open-source project inspired by Kazuma's publicly shared learning practices. It is not official, authorized, affiliated with, or endorsed by Kazuma.

## Fast start, not a shortcut

The coach shortens the distance between “I want to learn” and completing one useful task. Once the target language is known, it checks a free voice environment before a spoken lesson, asks what you want to achieve without assuming travel, then teaches only what the first task needs.

It does not skip reliable input, changed-condition practice, or delayed retests. “Fast” means removing vocabulary lists, grammar sequences, generic calendars, and material unrelated to your current goal—not promising instant A2, a fixed completion time, or lower standards.

## A2 core tasks, with travel as an option

The internal task map uses seven broad A2 domains: personal information; routines and the immediate environment; needs and transactions; time, place, and directions; preferences and social exchange; communication repair; and short texts and writing. Your real goal can add custom tasks, while the conservative internal screen counts only these shared core domains.

![Optional travel practice areas: transport, accommodation, food, directions, shopping, and communication repair](assets/readme/travel-scenarios.svg)

If travel is your goal, the coach maps transport, accommodation, food, directions, shopping, repair, and basic non-emergency help into the relevant core domains. Serious medical, legal, immigration, and safety emergencies are not presented as situations that A2 alone makes safe to handle independently.

Each active phrase is stored with your version, a replaceable slot, a likely follow-up, and a repair expression when applicable. The goal is not a frozen phrasebook: it is completing the task when one detail changes.

## Start in one line

```text
Use $language-learning-coach. I am starting Korean from zero. Prepare a free
voice environment first, then help me choose a useful first goal.
```

If you have not named a language, the first reply contains only:

```text
What language do you want to learn?
```

Once the language is known, the coach checks the free voice environment and asks a neutral goal question such as “What do you most want to do first in Korean?” It asks only one question at a time—and only when the answer changes the next lesson.

Other useful starts:

```text
Use $language-learning-coach. Help me make polite requests in Egyptian Arabic.
Keep the local spoken variety distinct from Modern Standard Arabic.
```

```text
Use $language-learning-coach. Continue yesterday's Brazilian Portuguese.
I only have five minutes today.
```

## The shortest useful route is adaptive

![An eight-stage loop from a real task to reliable input, retrieval, interaction, feedback, and delayed transfer](assets/readme/adaptive-loop.svg)

For a spoken goal, a typical lesson moves through:

1. choose one real task and the target variety;
2. hear a complete, classified model before seeing the answer;
3. understand the intent and one critical detail;
4. learn one to three complete phrases with replaceable slots;
5. retrieve and transform them as prompts fade;
6. complete a short interaction with a follow-up and repair option;
7. fix one or two task-critical problems, then redo immediately;
8. retry later with a changed place, time, person, item, or condition.

Every continuation starts with one visible next task and a concrete completion condition. One mistake remains an observation; only the same pattern appearing across at least two real lesson dates enters the recurring-error queue. When two active patterns genuinely compete in one situation, the coach can interleave them inside that task instead of drilling each one in a block.

You can also opt into a roughly 30-second micro-immersion action attached to something you already do, such as opening a map or checking a booking. It adds no automatic new material, and reporting that you completed it records practice rather than upgrading ability evidence.

The order changes for reading-only or writing goals, accessibility needs, a new script, tone or pitch contrasts, rich inflection, honorifics, regional varieties, or diglossia. Travel, work, study, exams, reading, writing, media, heritage, daily life, and interest-led goals are peer routes when reliable resources exist.

## One micro-lesson, four visible moves

![A four-panel lesson: hear a complete model, attempt the task, receive one focused correction, and retry with a changed condition](assets/readme/lesson-storyboard.svg)

1. **Model:** hear the whole expression from a classified source; text follows when appropriate.
2. **Attempt:** use it inside the learner's current real task.
3. **Focused feedback:** preserve the exchange and correct only what most affects the task.
4. **Retry:** complete it again, then change one condition so recall—not copying—does the work.

AI role-play is useful simulation. It does not prove that you handled a native speaker, natural speed, background noise, a new accent, or an unpredictable real-world response.

## A2 direction, evidence by ability

![Six language abilities feeding into supported practice, independent completion, changed-condition transfer, and delayed retention](assets/readme/evidence-ladder.svg)

Listening, spoken production, reading, writing, interaction, and pronunciation are tracked separately. Hearing a phrase does not automatically count as speaking it; reading aloud does not prove interaction; same-session success does not prove retention.

The evidence ladder is:

```text
supported → independent → changed condition → delayed retention
```

The workspace records the task, prompt level, evidence environment, **response medium**, result, date, and next retest. That distinction prevents a typed romanization, an unobserved “I said it,” or a task still waiting for an answer from being stored as audible speech or writing. An A2 task moves from training to same-session, changed-condition, delayed, and real-world checks only when matching evidence exists.

One successful task is not A2. The internal A2-style screen passes only after at least five of the seven defined core domains reach delayed or real-world checks with distinct core phrases, communication repair is included, all six tracked abilities have retained evidence linked to exact task requirements, and at least one task passes a real-person or real-world check. Only then may the coach say that the evidence is consistent with A2-style performance **in the tested tasks** and name every gap. This is still not a CEFR result; only an appropriate external assessment can establish one.

## Sound sources are never hidden

For a spoken course, environment preparation is the first operational step:

- **macOS:** use the free built-in `say` voice and `afconvert`; if the target voice is missing, download a free system voice in macOS settings.
- **Windows:** use the free installed Windows voice through PowerShell `System.Speech`; if the target voice is missing, explain the exact Windows language speech capability and ask before installing it.
- **Optional online fallback:** only when local speech is unavailable, ask before creating an isolated workspace virtual environment with free `edge-tts` and its converter. It needs internet, is not Windows system speech, and may change or stop working.

No route requires an API key, credit card, paid cloud TTS, subscription, or global Python package install. The first complete phrase is generated and technically validated before the spoken lesson begins. Pure reading, pure writing, or explicitly text-only goals may skip this step.

For spoken goals, a new phrase is heard before its written answer when playable audio is available. Every model is classified:

| Source class | What it means | What it can support |
|---|---|---|
| `native_official` | Official or institutional recording by a speaker of the target variety | Strong model for the exact material the source covers |
| `native_traceable` | Traceable native-speaker recording with suitable variety, context, and register | Model within the source's documented scope |
| `tts` | Clearly labelled synthetic speech fallback | Initial listening and rehearsal, not native-model or pronunciation evidence |
| `pending` | A reliable model has not yet been delivered | The spoken or pronunciation step pauses instead of being invented |

For TTS, the workspace separately records the expression/register check, target variety, engine or voice, delivered file/player, and technical validation. A playable waveform does not verify that the wording is natural.

Local WAV files are structurally validated before delivery. Technical validity never substitutes for source reliability, correct variety, actual playback, or pronunciation assessment.

The coach does not require an MP3 or recording upload and does not advertise a pronunciation score. Only when the host explicitly supports audio input and the learner voluntarily supplies it may the coach give limited qualitative feedback on features it can actually hear.

## Installation

You need a host with local Skill support and Python 3 for the bundled TTS, audio, migration, and workspace tools. Spoken lessons also need either macOS system speech, Windows system speech, or user-approved access to the free isolated online fallback. The delivery validator accepts classic uncompressed RIFF PCM WAV. The Git method also requires Git.

### Bundled Skill installer

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ai-martin-lau/language-learning-coach \
  --path . \
  --name language-learning-coach
```

### Git

```bash
git clone https://github.com/ai-martin-lau/language-learning-coach.git \
  ~/.codex/skills/language-learning-coach
```

Alternatively, download the repository and copy its contents to:

```text
~/.codex/skills/language-learning-coach
```

Start a new Codex task after installation so the Skill is discovered.

## How the route changes by language

| Language or goal feature | Adaptation |
|---|---|
| Tone, pitch accent, length, or stress contrasts | Perception contrasts before production, followed by sentence-level practice |
| A new or complex writing system | Sound and script progress together; transliteration receives a fade-out plan |
| Rich inflection or agglutination | Whole phrases plus early stem/affix analysis and controlled generation |
| Register, honorifics, dialect continua, or diglossia | Relationship, region, and medium are attached to each expression |
| Reading, writing, work, exam, media, or heritage goals | Skill balance and evidence tasks change to match the real target |

### A sound–script foundation lane for every applicable written language

Every language in scope that has an applicable normal written form gets a cumulative sound–script foundation lane. For spoken goals with playable audio, it starts with the sound of one useful complete chunk, then reveals the normal target text and extracts only one small target from that chunk: for example, a Hangul jamo or syllable block, a kana contrast or contextual kanji reading, an Arabic joining form, a Chinese character distinction, or a spelling–sound, stress, or connected-speech pattern in French, German, or another language whose script is familiar. Practice returns immediately to the complete chunk; a whole chart never becomes a prerequisite for communication.

When transliteration is needed, it is reduced in the same lesson or given an explicit fade plan. Every introduced unit or pattern receives a later no-answer retest in a changed position, word, sign, or nearby expression. The lane tracks coverage and scheduling, not mastery. Reading-only, signage-reading, and accessibility cases start from the actual medium. If a spoken goal temporarily lacks playable audio, sound work pauses and switches to text only after the user agrees; neither path manufactures listening or pronunciation evidence.

The examples are not a permanent support list. Another modern spoken or written language is in scope when reliable audio, dictionaries, grammar references, and usage evidence are available. Signed, classical, constructed, and resource-scarce languages require specialist materials or coaching beyond this Skill's current scope.

## Local learning state and privacy

When the current workspace is writable, the coach can maintain:

```text
language-learning/<language-slug>/
├── profile.md
├── phrase-bank.md
├── function-map.md
└── progress.md       # A2 tasks, sound–script lane, retests, and lesson evidence
```

These readable Markdown files store course-relevant goals, constraints, habit anchors, contextualized expressions, audio source classes, per-ability evidence, starter-function coverage, sound–script foundation coverage, recurring-error observations, optional micro-immersion, and scheduled retests. They remain in the user's workspace, not the installed Skill directory. A bundled validator checks structure and internal consistency without claiming that the recorded learning result is true.

Before validating an older workspace, the bundled additive migrator renames the legacy travel-map heading, inserts a missing empty sound–script table, and preserves existing task rows, lessons, evidence, and notes. It never reclassifies old travel domains or infers past foundation learning.

The repository contains no telemetry, account integration, or background service. Codex and user-authorized tools may access external sources when a lesson needs reliable language material; those products' privacy rules still apply.

## Method and evidence

The design draws from Kazuma's public discussions of sound-first imitation, useful phrases, active vocabulary, practical grammar, consistent task-based habits, and interest-driven input. See [the method summary and primary sources](references/kazuma-method.md).

Those practices are not treated as one scientifically validated package. The Skill checks individual choices against second-language acquisition research on pronunciation instruction, formulaic sequences, explicit grammar, interaction and corrective feedback, spacing and retrieval, meaning-focused input, and self-regulation. See [the evidence matrix and guardrails](references/evidence-and-guardrails.md).

The README's use of visual navigation was informed by the language-learning section of [byoungd/up](https://github.com/byoungd/up). The recurring-pattern and interleaving interaction takes product-design inspiration from [m98/fluent](https://github.com/m98/fluent), the optional piggyback practice from [hamsamilton/lang-tutor](https://github.com/hamsamilton/lang-tutor), and the single visible next action from [learn-anything-skill](https://github.com/vesperchinn/learn-anything-skill). These repositories are interaction-design references, not research evidence. All implementation, copy, and artwork here are original.

## Repository structure

```text
.
├── SKILL.md                         # Main behavior and routing instructions
├── agents/openai.yaml              # Codex display metadata
├── assets/
│   ├── learning-workspace/          # Persistent course templates
│   └── readme/                      # Original README visual assets
├── references/
│   ├── kazuma-method.md             # Public method sources and boundaries
│   ├── evidence-and-guardrails.md   # SLA research and scientific limits
│   ├── language-adaptation.md       # Cross-language feature adaptation
│   └── session-protocols.md         # Lessons, feedback, review, and state
├── scripts/validate_audio.py        # Local PCM WAV delivery validator
├── scripts/generate_tts.py          # Free macOS, Windows, and optional online TTS
├── scripts/migrate_workspace.py     # Lossless legacy workspace migration
├── scripts/validate_workspace.py    # Markdown learning-state validator
├── tests/test_generate_tts.py       # Cross-platform TTS regression tests
├── tests/test_validate_audio.py     # Audio validator regression tests
├── tests/test_validate_workspace.py # Workspace validator regression tests
└── docs/plans/                      # Design records
```

## Contributing

Issues and pull requests are welcome, especially for source-backed corrections, better adaptation for mainstream language varieties and real A2 tasks, clearer safety and evidence boundaries, and natural improvements to the five README translations.

Use English `README.md` as the content source of truth and update all affected translations in the same pull request. Do not add fixed-time A2 claims, unsupported fluency promises, invented native-speaker consensus, fake testimonials, or claims of Kazuma affiliation.

## License

Released under the [MIT License](LICENSE).
