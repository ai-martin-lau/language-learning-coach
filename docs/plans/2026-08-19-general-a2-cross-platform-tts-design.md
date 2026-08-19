# General A2 positioning and free cross-platform TTS design

Date: 2026-08-19
Status: approved in conversation

## Problem

The current project name, frontmatter, default prompt, README framing, task map, and internal A2-style screen all make travel the default. A beginner who only says that they want to learn Korean can therefore be asked what they will do in Korea, even though their actual goal may be daily communication, work, study, an exam, media, family, or general interest.

The current audio contract is also incomplete. It correctly distinguishes native recordings from TTS and validates local PCM WAV files, but it does not provide a deterministic macOS or Windows synthesis path. A host agent may therefore understand that audio is required without knowing how to generate it on the user's machine.

## Goals

1. Reposition the product as a zero-beginner A2 language coach rather than a travel-first coach.
2. Keep travel as one optional goal route alongside daily life, work, study, exams, media, reading, writing, heritage, and interest-driven learning.
3. Start with one neutral question that identifies the learner's first useful outcome without assuming travel.
4. Preserve the evidence ladder, source boundaries, delayed retesting, and non-certification language.
5. Provide a free-first macOS and Windows TTS path that detects the environment before acting.
6. Never require a paid API, billing account, subscription, or per-character service.
7. Keep all generated learner audio explicitly labelled as synthetic speech and technically validated.

## Non-goals

- Promise that every learner reaches A2 in a fixed time.
- Treat an internal screen as a CEFR certificate.
- Guarantee equal voice quality or language coverage on every operating system.
- Install system components silently or bypass administrator controls.
- Present TTS as a native-speaker recording or pronunciation-mastery reference.
- Build a general-purpose paid cloud TTS integration.

## Approaches considered

| Approach | How it works | What it enables | Trade-offs |
| --- | --- | --- | --- |
| Cosmetic rename | Change the display name and opening copy but retain the travel task map and travel screen | Fastest visible correction | Internal behavior still pulls learners back to travel and becomes inconsistent |
| General A2 core with optional routes | Generalize onboarding, task state, screening, documentation, and tests while retaining travel as one route | Coherent beginner-to-A2 product for multiple motivations | Requires coordinated schema, validator, migration, README, and test changes |
| Unbounded language coach | Remove A2 and route structure and respond to any learning request | Broadest scope | Loses the project's distinctive measurable progression and makes evidence claims less useful |

Adopt the second approach.

For audio, documentation-only platform commands were rejected because host agents can execute them inconsistently. Paid cloud APIs were rejected because they require account configuration or can create a bill. Adopt one cross-platform helper with local system voices first and a free, optional online fallback.

## Product positioning

- Public name: `零基础 A2 语言教练` in Chinese and natural equivalents in the other README languages.
- Internal skill name remains `language-learning-coach` to avoid breaking invocation and installation paths.
- The one-line promise is to help a beginner build verifiable A2 foundations along the shortest practical route supported by their performance.
- Travel remains an example and optional route, not the product default.
- The first lesson begins from a useful task selected from the learner's stated goal, not from a universal course calendar.

## Neutral onboarding

If the target language is unknown, continue to ask only which language the user wants to learn.

If the target language is known but the goal is unknown, ask one neutral question such as:

> 你学韩语最想先做到什么？

Examples may include daily communication, travel, work, study, an exam, reading, writing, media, family, or interest, but the question must not assume any one of them. The learner may answer in their own words; do not force a menu.

After the goal is known, ask only the next missing fact that changes the first lesson. A complete beginner should enter a small first task without a placement test.

## General A2 task model

Rename the travel task map to an A2 task map. A task records:

- a stable task ID;
- the learner's goal route and concrete context;
- an observable victory condition;
- exact phrase and ability evidence requirements;
- core action, likely follow-up, and communication repair;
- same-session, changed-condition, delayed, and real-world evidence states.

The task map is user-specific. Travel tasks remain available, but work, study, daily life, reading, writing, media, and other appropriate tasks use the same evidence contract.

The internal A2-style screen must no longer require a fixed number of travel domains. It should require broad evidence across user-relevant A2 functions such as personal information, routine and immediate environment, simple needs and transactions, time and place, preferences, short social exchange, and communication repair. It must retain:

- multiple distinct tasks rather than one repeated script;
- independent performance, changed-condition transfer, and delayed retention;
- evidence separated by listening, reading, spoken production, interaction, writing, and pronunciation;
- at least one real-person or real-world check before a broad readiness statement;
- explicit untested dimensions and scope limitations;
- the fixed statement that formal CEFR level is not confirmed.

An explicitly reading-only or writing-only route may mark other dimensions as not applicable for that route, but it cannot be described as general all-skills A2.

## Free-first TTS architecture

Add a standard-library Python helper that exposes three actions:

1. `probe`: detect the operating system, available synthesis engines, converters, Python environment, and installed voices.
2. `voices`: return installed voices with language or locale information where the platform exposes it.
3. `synthesize`: generate one labelled synthetic utterance, normalize it to traditional RIFF PCM WAV, then invoke `scripts/validate_audio.py`.

The helper must use explicit arguments for text, output path, target language or locale, voice, and rate. It must not select a voice from gender alone or claim that an installed voice matches a target variant without checking its locale.

### macOS local path

1. Detect `/usr/bin/say` and `/usr/bin/afconvert`.
2. Enumerate installed voices and match the requested language or locale.
3. Generate an intermediate AIFF with `say`.
4. Convert to RIFF PCM WAV with `afconvert`.
5. Validate and expose the WAV for playback.

These are macOS system tools and require no API key or usage payment. If a suitable Apple system voice is not installed, direct the user to the official system voice download UI. The voice download may require internet access but does not introduce a paid TTS account.

### Windows local path

1. Detect Windows and prefer the built-in Windows PowerShell path that can load `System.Speech.Synthesis`.
2. Enumerate installed voices and their cultures.
3. Use `SpeechSynthesizer.SetOutputToWaveFile` with an explicit PCM format.
4. Validate and expose the WAV for playback.

If the target-language voice is missing, detect the corresponding Windows Text-to-Speech language capability. Installing a Windows language or voice capability can require network access, administrator permission, or a restart, so the Skill must explain the exact change and obtain confirmation before executing it.

### Optional free online fallback

If no usable local voice is available, the Skill may offer `edge-tts` as an optional fallback only when the user permits network synthesis.

- Install it into an isolated per-user or per-workspace virtual environment, never the global Python environment.
- Do not request an API key, cloud project, billing account, credit card, or subscription.
- State that it is a third-party client of an online Edge speech service, requires internet access, and may stop working if that service changes.
- Convert its output to RIFF PCM WAV using a free converter that has passed the dependency policy below; do not bypass the existing WAV validation contract.
- If the fallback or conversion fails, stop the audio-dependent lesson step and explain the limitation. Do not silently continue with text while claiming listening or pronunciation practice.

Azure Speech, Google Cloud TTS, OpenAI TTS, and other paid or billing-enabled services are out of scope even when they advertise a free quota.

## Dependency installation policy

Always probe before installing anything.

| Dependency class | Behavior |
| --- | --- |
| Already-installed system tool | Use it without mutation |
| User-space free package | State the package, source, purpose, install location, network requirement, and zero-price constraint; then install into an isolated environment |
| System voice or language capability | Explain the exact system change and request confirmation before installation |
| Administrator-level package or converter | Request confirmation before privilege escalation or system-wide installation |
| API key, billing account, subscription, or paid quota | Reject and use another route |

Do not use a global `pip install`, silently add package repositories, disable security controls, or repurpose system environment variables. Record the selected engine, voice, locale, delivery method, and validation result in the learner workspace.

## Source and evidence boundaries

- Every generated file is labelled `合成语音（TTS）` at delivery.
- TTS can support initial listening discrimination and rehearsal.
- TTS cannot by itself prove native pronunciation, regional naturalness, or pronunciation mastery.
- Expression correctness, register, target variety, engine support, file playback, and WAV validation remain separate facts.
- A valid waveform does not prove that the expression is natural or that every device can play it.

## Migration and compatibility

- Preserve `name: language-learning-coach`.
- Migrate existing travel task maps into the generalized A2 task map without deleting evidence or rewriting history.
- Preserve travel route IDs and context as migrated task data.
- Replace travel-specific validator rules and internal screen fields with generalized equivalents.
- Reject ambiguous migrations rather than inventing new goals or A2 evidence.
- Update all five README languages together.

## Implementation scope

Expected files include:

- `SKILL.md`;
- `agents/openai.yaml`;
- `README.md`, `README.zh-CN.md`, `README.ja.md`, `README.ko.md`, and `README.es.md`;
- workspace templates under `assets/learning-workspace/`;
- `references/session-protocols.md`, `references/language-adaptation.md`, and evidence references as needed;
- migration and validation scripts;
- a new cross-platform TTS helper and tests;
- forward-test scenarios and regression tests;
- travel-only visual copy or assets whose labels would otherwise contradict the new positioning.

## Verification

1. A user who says only `我刚开始学韩语` is asked a neutral goal question and is not assumed to be travelling to Korea.
2. Travel, work, study, exam, media, reading, and daily-life goals can all create a valid first task.
3. Existing travel workspaces migrate without evidence loss.
4. The generalized internal screen cannot pass from one route, one repeated script, same-day work, or AI simulation alone.
5. macOS integration generates and validates a playable PCM WAV with an installed system voice.
6. Windows command construction, voice parsing, and failure behavior have unit coverage; the project does not claim a live Windows pass until tested on Windows.
7. Missing dependencies produce a specific free installation route or a clear stop condition.
8. No code path requests or configures a paid API, billing account, subscription, or credit card.
9. Optional `edge-tts` installation is isolated, explicitly online, and never presented as an official SLA-backed API.
10. All automated tests and `git diff --check` pass.

## Primary references

- Apple system voice management: https://support.apple.com/guide/mac-help/change-the-voice-your-mac-uses-to-speak-text-mchlp2290/mac
- Apple `say` audio generation example: https://developer.apple.com/documentation/avfaudio/creating-a-custom-speech-synthesizer
- Windows `SetOutputToWaveFile`: https://learn.microsoft.com/en-us/dotnet/api/system.speech.synthesis.speechsynthesizer.setoutputtowavefile
- Windows installed voices: https://learn.microsoft.com/en-us/uwp/api/windows.media.speechsynthesis.speechsynthesizer.allvoices
- Windows Text-to-Speech language capabilities: https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-language-packs-to-windows?view=windows-11
- `edge-tts` project: https://github.com/rany2/edge-tts
- Azure Speech pricing boundary: https://azure.microsoft.com/en-us/pricing/details/speech/
- Google Cloud TTS billing boundary: https://cloud.google.com/text-to-speech/pricing
