# fred-macro-feed

Daily structured FRED feed for the **Post-Close Macro Wrap** cloud routine.

The routine's WebFetch tool is fingerprint-403'd by FRED's edge, so it can't call FRED
directly. This repo's GitHub Action runs each weekday ~21:00 UTC, fetches the series
server-side (a normal egress FRED does not block), and commits [`fred_latest.json`](fred_latest.json).
The routine reads that one file from `raw.githubusercontent.com`.

The FRED API key is stored only as the encrypted Actions secret `FRED_API_KEY` — never in this repo.

Series: HY OAS `BAMLH0A0HYM2`, IG OAS `BAMLC0A0CM`, 5y5y `T5YIFR` (raw level);
CPI `CPIAUCSL`, core CPI `CPILFESL`, PCE `PCEPI`, core PCE `PCEPILFE`, PPI `PPIFIS` (y/y %).

Raw URL: `https://raw.githubusercontent.com/Sam021903/fred-macro-feed/main/fred_latest.json`
