# Audio-first lesson design

Date: 2026-08-13

## Problem

The coach can currently begin a spoken-language lesson with written text even when the learner is a complete beginner and can play audio. It also has no deterministic check that a locally generated audio file contains playable audio rather than only a container header.

## Approved behavior

For an audible language when listening or speaking is in scope and playback is available:

1. Deliver playable sound before revealing the written form, transliteration, phonetic transcription, or answer for a new spoken chunk.
2. Prefer verified native or official audio. Permit TTS as a fallback only when it is labeled beside the player as synthetic speech.
3. Validate local audio before delivery. A filename, successful download, or nonzero file size is not sufficient.
4. Do not deliver files that are empty, undecodable, zero-duration, truncated, or digitally silent.
5. If playable sound cannot be delivered, state the limitation and pause listening and pronunciation work. Switch to a non-audio task only with the learner's agreement.
6. Keep video-first handling for signed languages and allow explicit reading-only or writing-only goals to bypass the audio gate without claiming listening or pronunciation progress.

## Implementation

- Put the non-bypassable rule in `SKILL.md`.
- Add the detailed interaction and failure protocol to `references/session-protocols.md`.
- Clarify modality boundaries in `references/language-adaptation.md`.
- Add `scripts/validate_audio.py` for deterministic validation of classic RIFF PCM WAV files using only the Python standard library. Resolve it from the installed Skill directory, never from the learner workspace.
- Add focused tests that generate their own fixtures at runtime.
- Add a media-delivery field to the phrase-bank template so source reliability and technical playability remain separate evidence.

## Validation

- A classic RIFF PCM WAV with sufficient duration and signal passes.
- A zero-frame WAV, silent WAV, truncated WAV, corrupt `.wav`, and empty file fail; unsupported formats are reported separately. CLI outcomes `0`, `3`, `4`, and `5` are covered.
- The Skill passes `quick_validate.py`.
- A fresh-agent forward test begins a zero-beginner spoken-language lesson with audio before target-language text and labels TTS locally when used.
