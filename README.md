# news-image-20261121-entry

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Vellocatta/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Vellocatta/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Saturday 21 November 2026: 50 stories, 6 continents, one front page. One image summing up the world news of Saturday 21 November 2026.

## The image

A front-page poster, "Saturday 21 November 2026", with a lead story (missiles fall on Poland; NATO calls it a grave violation), three hero stories (Wall Street rout, Palisades arsonist convicted, Cyclone Akvan), 12 featured stories (each with a headline and a deck), and 38 one-line briefs — 50 stories across 6 continents:

1. **Poland · NATO** — Missiles fall on Poland; NATO calls it a grave violation
2. **Wall Street · Markets** — Stocks plunge; S&P and Dow enter correction
3. **Ukraine · Kyiv** — Kryvyi Rih strike kills 2, injures 42
4. **Los Angeles · Justice** — Palisades arsonist convicted at retrial
5. **Odisha · Weather** — Akvan weakens; rains roll on after landfall
6. **Brussels · Europe** — UK and EU sign food, carbon and youth deals
7. **Shenzhen · Summit** — Trump–Xi–Putin summit ends with few results
8. **Berlin · Diplomacy** — Europe presses for a place in peace talks
9. **Washington · Courts** — Second judge blocks Trump's triumphal arch
10. **Washington · Sanctions** — US sanctions four Iranians over oil revenues
11. **The Hague · Justice** — World backs ICJ genocide ruling on Myanmar
12. **California · Tech** — California subpoenas Nvidia over ex-CEO, China ties

Plus 38 more briefs (HIMARS strike, EU €1bn aid, GTA VI sales pass $1.8bn in a day, and 35 others) — see `news-notes.md` for the verified story list and sources.

## How it was made

`gen_frontpage21.py` draws the poster with PIL from the verified story list in `news-notes.md`, so every headline is spelled correctly and legible. No downloaded images, no AI image generation, no network, no clock, no randomness — the same inputs produce the same bytes. Eight layout variants were rendered and judged pairwise; the winner (v5, navy, no map — the only layout where all 12 featured stories are fully legible) is `entry.png`.

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`.

## Verify

```sh
python3 gen_frontpage21.py v5-navy-nomap   # re-render the winner (byte-identical)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # entry.png -> out/entry.png
```
