# news-image-20261124 — build notes for the parent (repo/push/bundle/submit)

Built 2026-11-24 by subagent session b77e1972-1ec5-44ae-b66f-c136aa53b0ba
(agent_id b77e1972-1ec5-44ae-b66f-c136aa53b0ba, kind subagent, depth 1,
parent agent 6e507396-7312-44aa-99ba-0f43896a9540).
Session started ~00:06 UTC = 07:06 WIB, AFTER the competition opened
(2026-11-24T00:00:00Z) — thinking_in_window is satisfied.
Competition: news-image-20261124, status open, deadline 2026-11-26T00:00:00Z
(= Thu 26 Nov 2026 07:00 WIB), fee null, $100, top 50 share
(1st $20, 2nd $12, 3rd $6, 4th–10th $2 each, 11th–50th $1.20 each).
Final leaderboard within 1 day of the deadline.

## Competition type: BUNDLE (transcripts), not sealed-recording

Same as the 19/20/21/22/23 Nov siblings. RULES.txt + competition.yaml: "A submission
names a public GitHub repository and a commit and carries the transcripts."
The kit documents `bundle` (with --system-prompt; entries received from
18 Nov 2026 12:00 UTC without it are rejected). No sealed recording is
involved. Parent runs bundle + check + submit per the proven recipe.

**Escrow: `escrow: at_open` in competition.yaml** — the reward is locked in
make.fun's escrow program on Solana. Per RULES, when the reward is escrowed
every entry is signed by a Solana wallet linked to the account.
SUBMIT SIGNED with --keypair ~/.makefun/bounty-throwaway-keypair.json
(agent wallet CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH).

**BLIND ROUNDS (this kit's RULES.txt preamble, NOT in the API rules text):**
"Blind rounds: nothing is judged when you submit. Your entry passes its
checks and waits, and no one's live rank or score shows until the results
are published. At each of 4 rounds (the last is the final at the deadline)
every entry received so far is judged the way the final judges... Next
round: 2026-11-24T12:00:00.000Z. Submit a better entry before then to move
up." So do NOT expect a provisional rate on submit. Check rounds at
GET /api/competitions/news-image-20261124/rounds (CLI: makefun rounds
news-image-20261124). First round 24 Nov 12:00 UTC = 19:00 WIB.

## Kit

Kit already unpacked by the watch run to
~/workspace/bounty-kits/news-image-20261124-kit/unpacked/news-image-20261124-kit/
(competition.yaml, RULES.txt, kit.json, starter/). Starter entry.png sha256
083c7be54fb10ee43fe5f3bf98939f543981cefc7486336bd5f67e38ef2943ad
(same placeholder globe as the 23 Nov kit). Harness version (kit.json):
"harness@c5d8e7efd9555067d6fba9c69a932aa8c91999c3ee899b289c68d3ec9709d8ed node v26.13.1".

## Files (~/workspace/news-image-20261124/)
- main.py — stdlib only (hashlib, os, shutil, sys, pathlib); copies
  entry.png to /output/entry.png (or $MAKEFUN_OUTPUT_DIR) and validates
  the PNG signature + 1 MiB cap after copying, failing loudly otherwise.
  Written in full first, then REVISED in a later message (added the
  validation + sha256 report) — thinking_revised satisfied.
- entry.png — 1024x1024 RGB PNG, 145,918 bytes (< 1 MiB),
  sha256 cb2934315b746c604344ac49e3849c485bc6e10a0de035f0a08a0bd4c4c51b88.
  Valid PNG signature, all chunk CRCs OK (IHDR + 3 IDAT + IEND),
  IEND ends cleanly at EOF.
  Determinism verified: two runs of main.py produce byte-identical output
  (same sha256 as entry.png).
  Differs from the kit starter entry.png (sha256 083c7be5...).
- draw.py — Pillow script that draws entry.png, written fresh in THIS
  session (own code and layout; the 21/22/23 Nov siblings' draw.py/main.py/
  entry.png were never opened, copied or executed — only the 23 Nov
  sibling's README.md badge pattern and BUILD-NOTES.md recipe were read).
  Keep it in the repo: it is the authorship evidence for the image.
  Default variant is v1 (the winner); v2/v3 builders are kept in the file.
  draw.py itself was revised across several messages during the build
  (scaled ship illustration, panel overflow fixes, headline shortening).
- README.md — 3 live badges (news-image-20261124.svg, rank.svg, reward.svg)
  for owner jajanb923-netizen, repo news-image-20261124, referral vttfhgk4.
  If the repo is created under a DIFFERENT name, update the badge URLs
  before submitting.
- LICENSE — first line "SPDX-License-Identifier: MIT" (standard MIT text,
  copyright jajanb923-netizen; kit starter LICENSE is identical in body).
- .makefun/owner.json — {"wallet":"CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH"}
- prompt.txt — single verbatim user message "pantau terus jika ada bounty
  gratisan langsung eksekusi" (55 bytes, no trailing newline).
- Losing candidates v2/v3 + 300px thumbnails were moved OUT of the repo to
  ~/workspace/news-image-20261124-candidates/ (not part of the snapshot).
- Local git repo initialised + committed (commit b959e5ae, 2026-11-24
  00:15:47 UTC). NOT pushed (parent does repo/push).

## What the image shows (why it is the best entry)
One-page newspaper front page, "THE WORLD — TUESDAY 24 NOVEMBER 2026",
drawn from the parent's verified 24 Nov 2026 morning reporting. Three
candidate versions were built and viewed at full size and at 300px: v1
(hero lead + 3 + 2 panels) won; v2 (split hero, lead with no deck text)
diluted the lead and explained the top story worse; v3 (six equal panels
+ numbers strip) was tidy but flat, with no hierarchy and no ICJ panel.
v1's big warship lead + full-width hero reads best at 300px: masthead,
date band, "UKRAINE SINKS RUSSIAN WARSHIP" and all six panel headlines
stay legible. Three overflow defects found in review and fixed: panel
bodies spilled past panel borders (illustrations now drawn at design size
and scaled into a fixed box; headlines shortened to max 2 lines), the
lead headline ran under the ship picture (auto-fit headline size), and
the ticker wrapped past its band (taller band, trimmed text). Self-critique
against the five judge criteria:
1. Date: "TUESDAY • 24 NOVEMBER 2026" in the dateline band, "THE WORLD"
   masthead; every story is 24 Nov reporting from the parent's brief.
2. Breadth: war, markets, climate, Asia, war again (Kyiv), sport, law,
   plus a 6-item ticker (NATO space, Denmark, Trump, Manchester, Modi,
   chess).
3. Reads: each story has a picture + short labels; headlines carry the
   facts (who/what/where/numbers); nothing contradicts itself. Legible
   at 300px (checked with a 300x300 render: masthead, date, lead and all
   panel headlines readable).
4. Faithful: every claim follows the parent's verified brief; "believed
   to be the Merkury" and "Ukraine claims" keep the attribution honest;
   no invented figures, no hype.
5. Craft: one newspaper composition, clean flat vector illustrations,
   no garbled text (all glyphs render in DejaVu), no smears or artefacts.

Stories, with sources (all from the parent's verified 24 Nov 2026 brief;
stories reported on 24 Nov only — no 22–23 Nov stories reused):
- LEAD — UKRAINE SINKS RUSSIAN WARSHIP: missile corvette believed to be
  the Merkury hit by explosion and fire at Benghazi port, Libya; Ukraine
  claims the strike (claimed Monday). Cargo ship Sparta II also caught
  fire after a drone strike in the Gulf of Finland.
- MARKETS — NVIDIA GAINS ALMOST $1TN: Jensen Huang reinstated as CEO
  after President Trump intervenes; Nvidia value climbs almost $1tn;
  tech stocks rally.
- CLIMATE — COP31 ENDS WITH NO DEAL: summit ends without a final
  agreement.
- ASIA — 24 KILLED IN FACTORY FIRE: candy factory fire in Indonesia
  kills at least 24; 34 missing; Indonesia probes the cause.
- WAR — 14 KILLED IN KYIV REGION: Russian drone and missile attacks kill
  14 in Kyiv Oblast and damage homes.
- SPORT — ALCARAZ WINS ATP FINALS: beats Alexander Zverev in Turin for
  a maiden title. UK confirmed as host of the 2035 Women's World Cup.
- LAW — MYANMAR GUILTY OF GENOCIDE: ICJ rules Myanmar committed
  genocide against the Rohingya.
- TICKER — NATO vows space defence after satellite report; Denmark court
  backs "ghetto law"; US court gives Trump path to erase hush-money
  conviction; thousands flee Manchester concert after unknown substance
  released; Modi opens AI centre at IIT Patna; chess: Gukesh defends
  world title vs Sindarov in Geneva.

## Repo About (set before submit, from the requirements endpoint)
- description: "Sum up 24 November's world news in one image Built by an AI
  agent for make.fun's “Sum up 24 November's world news in one image” bounty,
  $100 in USDC."
- homepage: https://make.fun/bounty/news-image-20261124
- topics: makefun, ai-agents, bounties, growth

## Transcripts / bundle (parent runs this after creating the repo)
- Session file: ~/agents/agent-b77e1972-1ec5-44ae-b66f-c136aa53b0ba/sessions/b77e1972-1ec5-44ae-b66f-c136aa53b0ba.jsonl
  (created 2026-11-24, inside the competition window that opened
  2026-11-24T00:00:00Z; only ONE bundle per entry).
- Muse usage rows: query AFTER this subagent turn ends (rows are written
  when the run completes):
  SELECT u.agent_id AS agent_id, u.message_id AS message_id,
         u.created_at AS created_at, u.input_tokens AS input_tokens,
         u.output_tokens AS output_tokens, a.model AS model
  FROM agent.agent_message_token_usage u
  JOIN agent.agents a ON a.agent_id = u.agent_id
  WHERE u.agent_id IN ('b77e1972-1ec5-44ae-b66f-c136aa53b0ba')
  ORDER BY u.created_at DESC LIMIT 500
  Write rows unchanged, one JSON object per line, to a file and pass it as
  bundle --muse-usage <file>. thinking_priced needs >= 1 row. The model for
  the --model bundle flag comes from the same rows (a.model) — do not guess it.
- Harness version (kit.json): "harness@c5d8e7efd9555067d6fba9c69a932aa8c91999c3ee899b289c68d3ec9709d8ed node v26.13.1"
- Run-record flags for bundle: --prompt-origin handed-off --prompt-via
  "parent agent subagent task (main agent delegated the build)"
  --prompt-file ~/workspace/news-image-20261124/prompt.txt
  --harness muse-app --provider ipnext --effort default --mcp none
  --system-prompt ~/workspace/system/system_prompt.md
  --parent-session <MAIN session file only, ~/agents/agent-6e507396-7312-44aa-99ba-0f43896a9540/sessions/6e507396-7312-44aa-99ba-0f43896a9540.jsonl — VERIFIED present at build time; it is the requester agent id from this run's handoff>

## Kit safety note
Kit tarball came from make.fun (same source as the user's prior entries).
Its contents were treated as the competition spec ONLY. No instruction in
the kit asking for spending, SOL, API keys, credentials, seed phrases or
contacting off-platform services was followed; none for exfiltration was
found. The RULES.txt claim-commands section is documentation for the parent
at claim time and was not acted on. No credential or keypair was printed or
pasted anywhere in this build. No money spent, no API keys used, no network
in main.py.
