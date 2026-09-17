# Long-video parsing: bounded memory and resumable analysis

## Scope

This changes parsing, not upload bandwidth or the browser's upload selection.
Use the same faster-whisper base/int8 model, beam size 5, and full-duration
acoustic coverage. No original-video downsampling or pitch subsampling.

## Implementation

- ASR: ten-minute cores with two seconds of left/right context. Each segment
  belongs to its core by midpoint; timestamps are clipped and offset globally.
  A fresh child process loads the model per core, then exits to release native
  allocations. Successfully completed cores are saved atomically, including
  silent cores. Source/model/settings changes invalidate checkpoints.
- Audio extraction: unchanged source reuses the WAV, keeping source identity
  stable across worker restarts rather than invalidating all ASR checkpoints.
- Acoustic features: bounded reads, full-duration RMS/pause/envelope statistics,
  thirty-second pYIN cores with overlapping context. RMS retains global framing
  and pause state. Only scalar per-frame pitch/RMS arrays survive, not large
  full-duration probability matrices. pYIN block estimates may differ slightly
  at boundaries because Viterbi context is local, not a two-hour global decode.
- Acoustic analysis runs in its own child process; successful pitch blocks and
  complete features are checkpointed. Failures omit pitch scalar metrics rather
  than presenting unavailable measurements as zero. Partial results are not
  cached as complete.
- Punctuation: per-batch checkpoints, batch progress, 180-second total budget
  for starting LLM calls, maximum 60-second request waits; rule fallback if the
  budget is exhausted or responses fail. The budget is not a hard process
  deadline (network connect/read timeouts are separate).
- Complete evidence is saved before scoring. A resumed scoring attempt need
  not rerun audio, frames, or VLM. Evidence identity includes source/config and
  optional material identities. Scoring itself is not checkpointed.
- Crash recovery: at most three automatic worker claims; repeated worker
  interruption becomes an explicit failure. Child failure does not kill the
  main worker. Polling checks cancellation during native inference and kills
  and reaps the child. ASR core timeout: 30 minutes; acoustic stage: one hour.
- Progress: ASR 15–40, punctuation 40–45, acoustic features 46–49; show phase
  and completed audio minutes instead of one opaque 45% stage.
- Worker logs phase/progress/elapsed/cgroup memory at transitions and every
  thirty seconds. One evaluation worker remains serial; CPU threads capped at 4.
- Deleting a task also removes its WAV/analysis checkpoints and generated frames.

## Verification

Local commands:

```sh
NUMBA_CACHE_DIR=/private/tmp/pku2-chunked-numba python -m unittest discover -s tests -v
python -m scripts.check_features
cd frontend && npm run build
```

`scripts.check_chunked_quality` compares whole-clip ASR/pYIN with chunked
inference on real audio around a ten-minute boundary. Transcript agreement is
not accuracy against ground truth. `scripts.benchmark_chunked_evaluation`
creates a labeled hard-linked copy of an existing upload in a new task and
observes the real queue/worker through completion, saving manifest/events and
result summary. Restarting the observer does not duplicate the test task.

Compare parsing success, time, peak worker cgroup memory, ASR tail timestamps,
complete pitch coverage, keyframes, five dimensions and report. Do not claim
upload throughput improved: the benchmark reuses an already-uploaded source.
Do not attribute time improvements solely to code when hardware also changed.

## Deployment and rollback

Apply only to `/opt/AskEdu-upload-benchmark`, with a backup Git branch and
PostgreSQL dump before deployment. Do not push GitHub or change `/opt/AskEdu`.
Roll back by switching to the preserved pre-optimization branch and rebuilding
backend/worker/web images, only after stopping active evaluations. No database
migration is required; source videos and reports are preserved. Checkpoints are
additional files and old code ignores them.
