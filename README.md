[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/ojiroaran96-ops/world-in-one-image-19-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/ojiroaran96-ops/world-in-one-image-19-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World in One Day — 19 November 2026

One image summing up the world's news of Thursday 19 November 2026,
entered in the make.fun bounty
[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119).

## The design

A dark "world in one day" board, drawn from scratch in pure Python:
a gold header names the day, six story cards in a 2-by-3 grid carry the
day's biggest stories from different regions and fields, a gold ticker
adds three more headlines, and a footer line closes the day. Every
letter is drawn from a small 5x7 bitmap font defined in `main.py`, so
the program needs no font files and no network.

## The six stories

- **Summit** — Trump, Xi and Putin meet in Shenzhen for trilateral
  talks at the APEC summit.
- **Conflict** — The US and Iran trade blows across the Gulf: US
  strikes on Qeshm Island, Iranian strikes on US bases in Bahrain
  and Kuwait.
- **Climate** — COP30 day 10 in Belem puts farming, land and women
  at the centre of the climate talks.
- **Tech** — Anthropic raises $81bn in the biggest IPO ever.
- **Space** — Voyager 1 reaches one light-day from Earth, 50 years
  after launch.
- **Culture** — Grand Theft Auto VI rolls out worldwide; gamers
  return to Vice City after a 13-year wait.

The ticker adds: a Van Gogh selling for a record $190.4m, Cyclone
Akvan nearing India's east coast, and Myanmar facing a genocide
verdict at the UN court.

## Run it

```sh
python3 main.py
```

`main.py` writes the image to `/output/entry.png`
(or `$MAKEFUN_OUTPUT_DIR/entry.png` when that is set). It uses only
the Python standard library, runs with no network, and writes
byte-identical output on every run. The PNG is 1024x1024 and well
under 1 MiB.
