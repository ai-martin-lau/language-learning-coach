# Recurring Errors and Micro-Immersion Design

**Date:** 2026-08-17  
**Status:** Approved by the user after the public GitHub Skill comparison

## Goal

Adopt the strongest lightweight ideas found in public language-learning Skills without weakening this project's fast travel-task start, audio provenance, evidence separation, or A2 claim boundaries.

The approved change has four parts:

1. Track recurring error patterns across lessons instead of treating one mistake as a permanent weakness.
2. Interleave at most two active, confusable patterns inside one realistic task.
3. Offer an optional micro-immersion action attached to an existing daily trigger.
4. On continuation, show one next task and its completion condition before summaries or menus.

## Alternatives considered

### A. Protocol text only

Add guidance to `SKILL.md` and `session-protocols.md`, without changing workspace state or validation.

- Advantage: smallest diff and no migration.
- Cost: recurring errors and opt-in state can drift or disappear between sessions.

### B. Small structured extension — selected

Keep the existing four-file workspace. Add one recurring-error table and two micro-immersion fields to `progress.md`, validate only machine-checkable constraints, and strengthen the continuation protocol.

- Advantage: persistent, readable, and testable without introducing a scoring engine.
- Cost: existing workspaces need a small additive migration.

### C. Adaptive scoring engine

Add rolling accuracy, fixed thresholds, automated scheduling, streaks, and per-item difficulty scores.

- Advantage: more automated decisions.
- Cost: higher complexity and false precision; it can turn limited chat samples into unjustified mastery claims.

## State contract

### Recurring error patterns

Add this table to `progress.md`:

```text
| 模式编号 | 类别 | 观察日期 | 关联语块 | 观察到的问题 | 下一辨别任务 | 状态 |
```

- IDs use `E01` or higher.
- Categories use `meaning`, `form_retrieval`, `register`, `script`, `interaction_repair`, `pronunciation`, or `other`.
- States use `observing`, `recurring`, or `resolved`.
- `observing` requires at least one real lesson date.
- `recurring` and `resolved` require observations on at least two distinct real lesson dates.
- `resolved` is a queue-priority state after a successful no-answer changed-condition task, not a permanent mastery claim; its truth still requires the recorded lesson evidence and cannot be proven from the row alone.
- Observation dates must exist as lesson headings, must not be in the future, and may not be duplicated.
- Linked phrase IDs must exist.
- The observed problem and next discrimination task must be substantive.

One error creates an observation and a next test, not a learner label. Only repeated evidence across lessons can change the state to `recurring`.

### Optional micro-immersion

Reuse the existing `生活嵌入与真实使用` section and add:

```text
- 微沉浸状态：off
- 微沉浸触发与单项动作：—
```

The status is `off` or `on`. `on` requires a concrete trigger and one action. The coach may offer this option after a useful task, but must not enable it without user agreement. Completion by self-report remains practice history, not ability evidence.

### One visible next action

Keep the existing `下次学习` fields. Once a workspace has a real lesson entry, `本次唯一重点` and `最小完成任务` must remain substantive. A continuation response starts directly with that single task:

1. choose one due retest if present;
2. otherwise choose the saved next task;
3. if an active recurring pattern blocks it, fold at most two patterns into that same task;
4. do not front-load a profile summary, progress report, menu, or full lesson plan.

## Interleaving rule

Interleaving is not random mixing and does not use a global accuracy threshold. Select one or two active patterns only when the learner must discriminate between them in a plausible task. Preserve the normal evidence contract: an interleaved task upgrades only the exact ability and response medium actually observed.

Do not show a worked answer before a delayed retest. For genuinely new production, a short model may precede supported practice, but the later evidence task must withdraw the model according to the existing prompt ladder.

## Files in scope

- `SKILL.md`
- `references/session-protocols.md`
- `references/evidence-and-guardrails.md`
- `assets/learning-workspace/progress.md`
- `scripts/validate_workspace.py`
- `tests/test_validate_workspace.py`
- five synchronized README files
- the current Korean learning workspace, migrated additively

No new state file, scoring system, streak, fixed review interval, or CEFR estimate is introduced.

## Acceptance checks

1. Template workspace passes validation.
2. Current Korean workspace passes after additive migration.
3. Validator rejects invalid IDs, enums, dates, phrase references, future observations, duplicated dates, and a `recurring` state based on one lesson.
4. Validator rejects `on` micro-immersion without a concrete trigger/action.
5. A started workspace cannot leave the unique focus or minimum completion task unresolved.
6. Existing audio tests, workspace tests, quick validation, Python compilation, and `git diff --check` all pass.
7. A fresh continuation forward-test presents one task rather than a progress dump.
