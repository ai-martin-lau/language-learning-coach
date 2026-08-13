# Multilingual README design

Date: 2026-08-13

## Goal

Prepare the repository for a public open-source launch with a useful README in five languages and an explicit open-source license.

## Approved languages

- English
- 简体中文
- 日本語
- 한국어
- Español

## Considered approaches

1. **Minimal install page** — fastest to scan, but it hides the project's language adaptation, persistent learning state, and research boundaries.
2. **Product-oriented README** — leads with value, installation, and examples, then explains adaptation and evidence. Best fit for a first public release.
3. **Research-oriented README** — strongest methodological detail, but too much friction for learners who want to install and start.

Use approach 2, with research transparency as the second layer.

## File structure

- `README.md` — English and source of truth.
- `README.zh-CN.md` — 简体中文.
- `README.ja.md` — 日本語.
- `README.ko.md` — 한국어.
- `README.es.md` — Español.

Every file uses the same language switcher:

```md
[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)
```

This follows common open-source practice found in repositories such as Wails and giscus: English is GitHub's default page, locale suffixes are explicit, language names are written in their own language, and flags are avoided.

## Shared chapter contract

All five READMEs keep the same order and meaning:

1. Value proposition and non-official disclaimer.
2. What makes the coach different.
3. Core capabilities.
4. Requirements and installation.
5. Quick start and example prompts.
6. Adaptation across language types.
7. Learning state and privacy.
8. Method, evidence, and scientific boundaries.
9. Repository structure.
10. Contributing and license.

Commands, paths, filenames, source links, and `$language-learning-coach` remain identical across translations.

## Installation design

Document two methods:

1. Install with Codex's bundled skill installer from the public GitHub repository.
2. Clone or copy the repository into `~/.codex/skills/language-learning-coach`.

Avoid claiming support in products or clients that have not been verified.

## Open-source release

- Add an MIT `LICENSE` with copyright attributed to `ai-martin-lau`.
- Keep the explicit statement that this is inspired by Kazuma's public material and is not official, authorized, or endorsed by Kazuma.
- Merge all README translations and the license together so translations do not drift at launch.
- Change repository visibility from private to public only after the documentation commit has reached `main`.

## Acceptance criteria

- Five README files exist and cross-link correctly.
- Headings, commands, paths, and factual claims remain aligned.
- Installation instructions refer to the real repository.
- Every README contains the non-official disclaimer, privacy behavior, and MIT license notice.
- The Skill still passes `quick_validate.py`.
- Git diff checks pass, `main` is clean, and GitHub reports public visibility.
