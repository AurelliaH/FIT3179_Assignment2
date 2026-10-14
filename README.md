# Who Still Shows Up?

Volunteering in Australia is falling. Where do people still show up?

A single-page visual story built with Vega-Lite, for FIT3179 Data Visualisation 2,
Monash University, Semester 2 2026.

**Live page:** https://aurelliah.github.io/FIT3179_Assignment2/

**Repository:** https://github.com/AurelliaH/FIT3179_Assignment2

## Running it locally

Open `index.html` through a web server, not by double-clicking it — the charts fetch
their data files, and browsers block that over `file://`.

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Vega, Vega-Lite and Vega-Embed come from jsDelivr
and the fonts from Google Fonts, so the page needs an internet connection; everything
else is in this repository.

**While editing:** browsers cache `.vg.json` and `.csv` aggressively. After changing a
chart, hard-reload (Cmd+Shift+R / Ctrl+Shift+R) or you will keep seeing the old version.

## Project structure

```
index.html                 the page itself
css/style.css              layout, typography, colour tokens
img/au-sa4-outline.svg     hairline SA4 outline used in the hero
js/vl-config.js            shared Vega-Lite styling for every chart
js/charts.js               maps each spec to its div id
js/NN_name.vg.json         one Vega-Lite specification per chart
data/*.csv                 the data each chart reads
data/au_sa4_2021.topo.json SA4 boundaries
scripts/build_acnc.py      builds the Figure 13 data from the raw ACNC files
sketch/                    the hand-drawn A4 layout sketch
```

## How a rate is worked out — read this before changing a number

Two denominators are possible, and mixing them silently is the easiest way to put a
wrong figure on the page. Each data file carries **both**, under names that say which
is which:

| Column | Meaning |
|---|---|
| `rate_pop15plus` | volunteers ÷ **everyone aged 15 and over** |
| `rate_respondents` | volunteers ÷ **people who answered the question** |

**`rate_pop15plus` is the measure the page uses.** Nationally it is 14.1% in 2021 and
19.0% in 2016 — 14.1% is the figure the ABS publishes. Every map, every regional chart,
the state comparison and the tile cartogram use it, in both years.

`rate_respondents` is about one point higher, because roughly 6% of people left the
question blank. It appears **only** in Figures 5, 10, 11 and 12, because the age tables
carry no population count per age group. Those charts say so in their subtitles, and the
page explains it once in the "Why do some percentages look a little different?" box.

Never plot the two against each other, and never quote a range without saying which one
it is on. Figures checked from the data:

- SA4 regions, `rate_pop15plus`: **6.3%** (Sydney – South West) to **24.0%** (WA Wheat Belt)
- State and territory falls 2016→2021, same denominator in both years:
  **3.0 to 5.9 percentage points**. Victoria furthest (−5.9); NT smallest (−3.0)
- Greater capital cities **13.2%**, rest of state **16.1%**
- 2,929,554 volunteers in 2021; **686,103 fewer** than in 2016

## The 13 charts

Specs are numbered in story order; `js/charts.js` maps each one to its `div` id.

| Fig | Spec | Idiom | Denominator |
|---|---|---|---|
| 1 | `01_trend_line.vg.json` | annotated line chart (GSS, 2006–2020) | survey, 18+ |
| 2 | `02_waffle.vg.json` | faceted waffle, 2016 vs 2021 | all 15+ |
| 3 | `03_choropleth_sa4.vg.json` | choropleth, 88 SA4 regions | all 15+ |
| 4 | `04_symbolmap_sa4.vg.json` | proportional symbol map | count |
| 5 | `05_agemaps_sa4.vg.json` | small-multiple choropleths, 4 age bands | respondents |
| 6 | `06_ranked_regions.vg.json` | ranked dot plot, top and bottom 10 | all 15+ |
| 7 | `07_scatter_size_rate.vg.json` | scatter, population vs rate | all 15+ |
| 8 | `08_dumbbell_state.vg.json` | dumbbell / connected dot plot | all 15+ |
| 9 | `09_cartogram_state.vg.json` | tile-grid cartogram | all 15+ |
| 10 | `10_pyramid.vg.json` | diverging population pyramid | respondents |
| 11 | `11_heatmap_age_state.vg.json` | heatmap, age × state | respondents |
| 12 | `12_beeswarm_ageband.vg.json` | beeswarm with interactive medians | respondents |
| 13 | `13_purpose_bars.vg.json` | split bar chart by charitable purpose | ACNC, self-reported |

Three map idioms: choropleth (Fig 3), proportional symbol map (Fig 4) and tile cartogram
(Fig 9). Fig 5 repeats the choropleth idiom as small multiples.

Interactions: Figures 7 and 13 filter on a legend click; Figure 12's median lines
recompute for whichever group is selected, and answer a hover.

## Colour

The page is dark (deep teal-navy `#0C2426`, chart panels `#14383A`). Chart colours are
set in `js/vl-config.js` plus each spec:

| Role | Hex | Used for |
|---|---|---|
| sage | `#A5D8BC` | rest of state · 2016 · "all other charities" |
| ochre | `#D99A2B` | capital cities · 2021 · the one warm accent |
| teal | `#6FB8AE` | single-series marks |
| ramp | `#1C7A70` → `#DAFBEB` | every sequential scale — **dark = low, light = high** |

Every pair that shares a chart clears the colour-blind separation floor against the panel
colour, and the ramp is single-hue and monotone in lightness. If you change a colour,
re-check it rather than eyeballing it — on a dark background a light mark and a dimmed
mark can look identical.

### Boundary file — check this before submitting

`data/au_sa4_2021.topo.json` holds the 88 SA4 polygons plus the state outlines, derived
from the ABS `SA4_2021_AUST_SHP_GDA2020` shapefile. It was downloaded ready-made rather
than built from the ABS shapefile in this project, so **confirm the unit's position on
using a prepared boundary file**, and cite the ABS ASGS Edition 3 boundaries as the
source either way. All 88 codes join to `volunteer_sa4_2021.csv` with no mismatches.

`data/sa4_centroids_2021.csv` positions the circles in Figure 4. These are poles of
inaccessibility, not geographic centroids — a plain centroid falls outside the land for
crescent-shaped coastal regions, which put several circles in the sea.

### Figure 13 — read before changing it

Built by `scripts/build_acnc.py`, which joins two ACNC files on ABN: the 2024 Annual
Information Statement (volunteer counts) and the Charity Register (charitable purposes).
It keeps registered charities reporting at least one volunteer, then writes
`data/acnc_purpose_split_2024.csv` — one row per purpose per segment.

The Register lets a charity tick up to twelve purposes. To keep the chart a true
partition with no double counting: one purpose ticked goes under that purpose, several
go under "More than one purpose", none go under "Purpose not stated". Those two buckets
hold 38% of volunteers, so they are shown, not hidden. 271 charities in the AIS had no
Register match and are excluded.

Each bar splits into its single largest charity and everyone else, because in two
purposes one organisation is most of the total. Three caveats that must stay on the page:

- **4.42m is roles, not people.** Charities self-report, so someone helping at two clubs
  is counted twice. Not comparable with the Census 2.93m.
- **Environment is 88.2% one charity.** Clean Up Australia reports 1,077,127 roles,
  24.4% of the national total, counting one-day event participants rather than regular
  volunteers.
- **"More than one purpose" is 47.9% one charity.** The Queensland CWA's 608,743 looks
  like volunteer hours typed into a headcount field.

Both outliers are named on the chart rather than removed.

## Before pushing to GitHub

`data/datadotgov_ais24.csv` (37 MB) and `data/datadotgov_main.csv` (15 MB) are the raw
ACNC downloads. The page never loads them — `scripts/build_acnc.py` pre-aggregates them
into the small CSV the chart reads. They are listed in `.gitignore` so they stay out of
the repository. To rebuild Figure 13's data, download them again from
<https://data.gov.au/data/dataset/acnc-register> and run the script.

Always check the live URL in a private window before submitting — a file missing from the
repository makes the page look broken to the marker even though it works locally.

## Still to do

- The hand-drawn A4 sketch in `sketch/`.

## Data sources

- ABS 2021 Census, General Community Profile table G23 (voluntary work), SA4 DataPack
- ABS 2016 Census, General Community Profile table G19 (voluntary work), SA4 DataPack
- ABS Australian Statistical Geography Standard (ASGS) Edition 3, SA4 digital boundaries, 2021
- AIHW, *Australia's welfare: Volunteers* (ABS General Social Survey series). The
  comparable series here runs 2006–2020; no later figure has been added.
- ACNC 2024 Annual Information Statement + ACNC Charity Register —
  <https://data.gov.au/data/dataset/acnc-register> (Figure 13; second data source)

## Acknowledgement

Claude (Anthropic) was used to validate and reshape the downloaded Census tables, to
recalculate the volunteering rates and the 2016–2021 changes from those tables, to help
write and debug the Vega-Lite specifications and the page layout, and to review wording.

ChatGPT (OpenAI) was used to help plan the story structure, to prepare and check data,
to debug chart specifications, and to review wording.

All figures are unmodified ABS and ACNC data; every number quoted in the page text is
calculated from the files in `data/`. The design decisions and the final text are my own.
