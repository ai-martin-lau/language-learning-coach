# Forward-test scenarios

Use these prompts with fresh agents that have access to the installed Skill but no prior audit conclusions. Treat each prompt as a real learner request, keep every workspace isolated, and inspect the raw messages, audio, and saved state afterward. Do not tell the tutor what answer or failure mode is expected.

These are protocol tests, not evidence that a human learner acquired A2. A human learning-effect pilot needs genuine time gaps and observable tasks with unfamiliar material and, where feasible, real people.

## Shared acceptance checks

For every scenario, verify that the tutor:

1. uses information already present instead of repeating intake questions;
2. reaches one useful task within the first three tutor turns;
3. gives playable, labelled audio before target text when spoken goals and playback are available;
4. records expression/register verification separately from the audio engine or file;
5. asks for one action at a time and reaches an observable victory condition;
6. uses prompt levels consistently and records the actual response medium;
7. does not upgrade waiting tasks, self-reports, romanization, TTS rehearsal, or AI simulation into unsupported abilities;
8. maps every passed mission to exact `phrase:dimension:role` requirements and distinguishes same-session success, changed-condition transfer, delayed retention, and independent real-world confirmation;
9. writes and validates the workspace without stale contradictory summaries;
10. ends a declared five-minute lesson after one compact win.

Also verify that the learner-level A2-style screen stays `not_ready` unless its full conservative gate is met; one mission, one high-ranked phrase, or AI simulation must never unlock the claim.

## F01 — French hotel, no recording

> I know no French. I am going to Paris in 30 days and can study 15 minutes a day. I first need to check into a hotel. I can play audio but cannot send a recording. Start now.

Stress points: neutral placeholder instead of invented identity; audio-first delivery; no pronunciation claim; one likely front-desk follow-up; delayed retest must not be simulated by changing the date inside the same session.

## F02 — Japanese restaurant, unfamiliar script

> I know no Japanese and cannot read kana. I am going to Tokyo in 21 days and have 10 minutes a day. Teach me to order one meal. I can play audio. Start.

Stress points: audio before Japanese text; temporary romanization with a fade plan; romanization is not writing or audible speech; one item substitution and one likely restaurant response.

## F03 — Egyptian Arabic taxi

> I am a complete beginner in Egyptian Arabic. I am going to Cairo in 45 days and want to tell a taxi driver my destination and understand the next question. I cannot read Arabic, but I can play audio. Start.

Stress points: Egyptian colloquial variety rather than MSA; traceable expression and register source; destination response, one follow-up, and a repair action; Arabic script and romanization remain separate evidence media.

## F04 — Korean convenience store, five minutes

> I know no Korean and cannot read Hangul. I am going to Seoul next month and first want to buy something at a convenience store. I have only five minutes and can play audio. Start.

Stress points: one core learner-required phrase plus at most one response or repair phrase; no habit questionnaire after the five-minute win; self-reported repetition remains practice completion, not spoken ability.

## F05 — German platform change, prior exposure

> I studied a little German but can hardly speak. Tomorrow I will take a train in Munich and I am most worried about a platform change. I have five minutes, can hear audio, and cannot send a recording. Practise directly.

Stress points: short baseline without a questionnaire; detail choices use at least `partial`; an explicit full meaning cue uses `intent/cued`; an unseen changed platform can support listening transfer but not real-station listening or spoken confirmation.

## F06 — Brazilian Portuguese, audio unavailable

> I am a complete beginner in Portuguese. I am going to Brazil next month and first want to take a taxi. Audio will not play today, but my final goal is listening and speaking. Start directly.

Stress points: the explicit request to continue permits a clearly labelled reading-only task; listening, speech, and pronunciation stay `new`; later spoken work waits for verified Brazilian Portuguese audio; text simulation is not a real taxi interaction.

## Human pilot gate

Before making a learning-effect claim, run a small human pilot that includes:

- an intake baseline and predeclared personal travel missions;
- multiple sessions with real elapsed time;
- unseen voices, texts, numbers, locations, and follow-ups;
- separate listening, spoken production, interaction, reading, practical writing, and pronunciation observations;
- delayed no-answer retests;
- at least one real-person or real-world checkpoint where safe and feasible;
- dropout, audio failure, and time-on-task reporting;
- conclusions limited to the sampled tasks and participants.
