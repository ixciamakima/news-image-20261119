# The World in One Day — Thursday 19 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261119)
[![Prize $250](https://img.shields.io/badge/prize-%24250-green)](https://make.fun/bounty/news-image-20261119)
[![Top 50 paid](https://img.shields.io/badge/top_50-paid-orange)](https://make.fun/bounty/news-image-20261119)

Entry for the make.fun competition
[news-image-20261119](https://make.fun/bounty/news-image-20261119) —
"Sum up 19 November's world news in one image" ($250, top 50 paid,
deadline 21 November 2026 07:00 WIB).

## The image

A single front page, **"The World in One Day"**, summing up Thursday
19 November 2026 in one 1024×1024 picture:

- **Masthead + date, big and unmistakable:** "THURSDAY 19 NOVEMBER 2026".
- **Lead story:** the first-ever trilateral summit of Trump, Xi and
  Putin in Shenzhen, ending in a joint "peace declaration".
- **40 stories from 7 regions** — Europe, the Middle East, Asia, North
  America, South America, Africa and Oceania — across politics, conflict,
  markets, technology, science, climate, culture and sport.
- **A numbered world map** (equirectangular, lat -58° to 84°), every
  story pinned where it happened, colour-coded by region.
- **Four drawn scene panels:** GTA VI launch day, the ICJ genocide
  verdict, Voyager 1 one light-day out, Cyclone Akvan.
- **Markets strip:** Dow -2.19%, S&P -2.02%, Nasdaq -2.25%, gold, Brent,
  Bitcoin and the VIX at Thursday's close.

Every story was first reported on 19 November 2026 (Reuters, BBC, AP,
ATP Tour, Investopedia and others); uncertain claims are attributed,
never stated as fact. All text is rendered programmatically with PIL and
DejaVu fonts — no garbled text, nothing AI-generated.

## Stories in the image

1. Summit of three powers — Trump, Xi, Putin meet in Shenzhen
2. GTA VI is out — Rockstar epic launches to 99 on Metacritic
3. Myanmar guilty of genocide — ICJ rules on 2017 crackdown
4. Anthropic's record IPO — $81bn raised, valued at $1.5tn
5. Wall Street sinks — Dow -2.2%, S&P -2.0%, Nasdaq -2.3%
6. COP31 draft drops fossil fuels — Deal text thins in Antalya
7. Missile hits Riyadh tower — Houthi strike on PIF building, reports say
8. Israel pushes into Gaza — Ground op goes beyond the Yellow Line
9. Europe open to Russia talks — Leaders coordinate in Berlin
10. UK sends 1,000 drones — Long-range kit pledged to Kyiv
11. Putin vows painful reply — After new strikes on the Crimean Bridge
12. Crimean Bridge hit again — Russia reports a fresh attack
13. Boat sinks off Senegal — Dozens missing, about 100 aboard
14. Venezuela signs US deal — Military pact months after Maduro's fall
15. Haiti army battles gangs — Push to retake a key corridor
16. Kenya picks US miners — Mrima Hill deal beats Chinese bid
17. Uganda landslide justice — Survivors take their case to the UN
18. Cyclone Akvan nears India — 300,000 evacuated in Odisha
19. Takaichi meets Putin — Japan PM talks at APEC sidelines
20. Kim stays home — North Korea leader skips APEC summit
21. Two Americans raised — Trump aide presses China on detainees
22. Pete Rose pardoned — Trump clears baseball's banned hit king
23. Fiona the hippo dies — Cincinnati Zoo star after swallowing hat
24. Voyager 1, a light-day out — NASA probe phones home
25. Chase data leaked — Thousands of emails in cyberattack
26. Iran war bill: $48bn — Senate blocks bid to end the war
27. UK-EU summit — London and Brussels try to patch ties
28. Covid inquiry reports — UK findings on testing and tracing
29. Italy hit by hoaxes — Hacking wave 'aims to destabilise'
30. California probes Nvidia — Over AI chips reaching China
31. Alibaba cloud soars 53% — But shares slip on earnings miss
32. China chip fears grow — Tech firms dread US AI curbs
33. Bank of Japan hints hike — Chief plays down soft spending
34. Train heist busted — $22m cargo ring charged in LA
35. Shelton, Zverev advance — ATP Finals semi-finalists set
36. Kangaroos reach final — Australia beats Samoa 44-12 in Sydney
37. Iglesias faces court probe — Inquiry over alleged offences
38. Ancient library reopens — Rome treasure restored to public
39. Susan Smith denied parole — 32 years after her sons' deaths
40. Pastor guilty in Haiti plot — Role in president's killing

## How it works

- `render.py` draws `entry.png` deterministically with Pillow
  (no network, no randomness, no timestamps).
- `main.py` (Python standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) and verifies the
  copy byte for byte.

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verification

- `entry.png`: 1024×1024, RGB, 231,938 bytes (limit 1,048,576)
- SHA-256: `4ddb6ae014afa6d1d266c9850ba09b83f4c09e554da15ca76d29e3791d5d9f40`
- `main.py` run twice to different directories: identical SHA-256
- Smallest text 13 px; composition (masthead, date, lead headline, map
  with numbered pins, story grid) checked legible at 300 px wide
- All 40 grid lines fit their columns with nothing truncated

## Licence

MIT — see `LICENSE`.
