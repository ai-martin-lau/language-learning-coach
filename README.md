[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

# Language Learning Coach

An adaptive Codex Skill that turns language learning into a continuing practice: reliable input, useful chunks, active production, real interaction, focused feedback, and delayed review.

It changes the lesson according to the language, variety, modality, goal, and the learner's observed performance. It can support spoken and written languages, signed languages, classical languages, constructed languages, and low-resource languages when reliable materials are available.

> [!IMPORTANT]
> This is an independent open-source project inspired by Kazuma's publicly shared learning practices. It is not official, authorized, affiliated with, or endorsed by Kazuma.

## Why it is different

Many AI language sessions end as isolated chats. Language Learning Coach is designed as a persistent course:

- **Real tasks before abstract progress:** goals become observable actions such as ordering a meal or answering follow-up questions.
- **Useful chunks, then flexible use:** complete expressions are learned with context, response patterns, and replaceable slots—not as frozen scripts.
- **Practice before the lecture:** the coach starts with input and interaction, then explains one high-value grammar pattern from what you just used.
- **Evidence instead of streaks:** mastery depends on unaided recall, transfer, interaction, and delayed performance—not time spent or cards reviewed.
- **Language-specific adaptation:** tones, writing systems, rich morphology, register, signing space, and historical traditions change the lesson design.
- **Persistent local state:** profile, phrase bank, performance evidence, and the next review queue can be maintained as readable Markdown.

## Core capabilities

- First-time onboarding that starts with one exact question: **`你要学习什么语言？`** (“What language do you want to learn?”)
- Adaptive daily lessons, five-minute maintenance, deep study, and real-world debrief modes.
- Listening and pronunciation practice with reliable audio and honest tool limitations.
- Video-first adaptation for signed languages, including manual and non-manual features.
- Practical grammar, active vocabulary, conversation, reading, writing, and exam-focused work.
- Delayed retrieval and transfer checks with six evidence states from `new` to `retained`.
- One active language plus maintenance rotation for additional languages by default.
- Optional Anki export built around situation-to-expression retrieval, not isolated word pairs.
- Source verification and explicit `needs_confirmation` handling for low-resource or sensitive languages.

## Requirements and installation

You need Codex with local Skill support. Python 3 is required for the bundled installer method, while the clone method requires Git.

### Install with the bundled Skill installer

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ai-martin-lau/language-learning-coach \
  --path . \
  --name language-learning-coach
```

### Install with Git

```bash
git clone https://github.com/ai-martin-lau/language-learning-coach.git \
  ~/.codex/skills/language-learning-coach
```

Alternatively, download the repository and copy its contents to:

```text
~/.codex/skills/language-learning-coach
```

Start a new Codex task after installation so the Skill is discovered.

## Quick start

Invoke the Skill directly:

```text
Use $language-learning-coach to help me learn a language.
```

If you have not named a language, its first reply contains only:

```text
你要学习什么语言？
```

You can also begin with a concrete goal:

```text
Use $language-learning-coach. I am starting Japanese from zero and have
15 minutes a day. I want to handle basic conversations on a trip to Japan.
```

```text
Use $language-learning-coach. Help me introduce myself at an American Sign
Language community event. I can watch and record short videos.
```

```text
Use $language-learning-coach. Continue yesterday's Brazilian Portuguese
lesson. I only have five minutes today.
```

The coach asks only for information that changes the next lesson, then starts a small real task instead of returning a long questionnaire or generic study plan.

## How lessons adapt

| Language or goal feature | Adaptation |
|---|---|
| Tone, pitch accent, length, or stress contrasts | Perception contrasts before production, followed by sentence-level practice |
| A new or complex writing system | Sound and script progress together; transliteration receives a fade-out plan |
| Rich inflection or agglutination | Whole chunks plus early stem/affix analysis and controlled generation |
| Register, honorifics, dialect continua, or diglossia | Relationship, region, and medium are attached to each expression |
| Signed languages | Reliable video, signing space, movement, orientation, and non-manual markers replace pronunciation work |
| Classical, historical, or liturgical languages | Text tradition, morphology, corpus evidence, and a named pronunciation tradition take priority |
| Low-resource or community-sensitive languages | Community or institutional sources are preferred; uncertain content is not invented |
| Exams, reading, writing, work, travel, or heritage goals | The skill balance and assessment task change to match the real target |

There is no fixed “supported languages” list. Support depends on the requested modality and the quality of available sources, and the coach must say when something cannot be verified.

## Learning state and privacy

When the current workspace is writable, the coach can maintain:

```text
language-learning/<language-slug>/
├── profile.md
├── phrase-bank.md
└── progress.md
```

These files store only course-relevant information: goals and constraints, contextualized expressions and sources, observed performance, corrections, and scheduled reviews. They remain in the user's workspace and are never written into the installed Skill directory.

The repository contains no telemetry, account integration, or background service. Codex and any tools the user authorizes may still access external sources when a lesson requires current or reliable language material; their own privacy rules continue to apply.

## Method and evidence

The operational loop is:

```text
reliable input → contextual chunk → perception and imitation → generation
→ interaction → focused feedback → delayed retrieval
```

The design draws from Kazuma's public discussions of sound-first imitation, useful phrases, active vocabulary, practical grammar, consistent task-based habits, and interest-driven immersion. See [the method summary and primary sources](references/kazuma-method.md).

Those practices are not treated as a scientifically validated package. The Skill checks individual choices against second-language acquisition research on pronunciation instruction, formulaic sequences, explicit grammar, interaction and corrective feedback, spacing and retrieval, meaning-focused input, and self-regulation. See [the evidence matrix and guardrails](references/evidence-and-guardrails.md).

The coach does **not** promise fluency in a fixed number of days, a native accent, identical resource quality across languages, or mastery based only on streaks, time spent, same-day success, or Anki accuracy.

## Repository structure

```text
.
├── SKILL.md                         # Main behavior and routing instructions
├── agents/openai.yaml              # Codex display metadata
├── assets/learning-workspace/      # Persistent course templates
├── references/
│   ├── kazuma-method.md             # Public method sources and boundaries
│   ├── evidence-and-guardrails.md   # SLA research and scientific limits
│   ├── language-adaptation.md       # Cross-language feature adaptation
│   └── session-protocols.md         # Lessons, feedback, review, and state
└── docs/plans/                      # Design records
```

## Contributing

Issues and pull requests are welcome, especially for:

- corrections supported by primary or community-recognized sources;
- better adaptation for underrepresented language types or learner goals;
- clearer safety, cultural, accessibility, and evidence boundaries;
- natural improvements to any of the five README translations.

Use English `README.md` as the content source of truth and update all affected translations in the same pull request. Do not add unsupported fluency promises, invented native-speaker consensus, or claims of Kazuma affiliation.

## License

Released under the [MIT License](LICENSE).
