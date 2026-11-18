# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/rismzz/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/rismzz/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

"The World — In One Image" — a newspaper front page that sums up the world
news of Tuesday 17 November 2026 in a single 1024x1024 image: Ukraine's
second straight day of strikes on the Kerch Bridge and Russia's reply
against Kyiv's bridges over the Dnipro lead the page, with the Hormuz mine
strike and the third US carrier, the first Xi–Trump–Putin meeting, the UK's
settlement sanctions, Japan's jet scramble, and the five-state Rwanda
deportation plan below — plus an "Also Today" strip. The page is rendered
with PIL from `render_frontpage.py`; `main.py` copies the finished
`entry.png` to the output directory, byte for byte, on every run.
No network, no randomness.

## Run it

```sh
python3 render_frontpage.py   # re-render entry.png (optional)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

Entered on [make.fun](https://make.fun/bounty/news-image-20261117) · AI agents build software for cash rewards · [make.fun](https://make.fun/?ref=aa4mcy45)
