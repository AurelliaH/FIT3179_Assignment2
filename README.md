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
data/dotdensity_sa4_2021.csv Figure 4 dots, one row per dot
data/bivariate_sa4_2021.csv Figure 5 classes: each region's rate and count tercile
data/au_sa4_2021.topo.json SA4 boundaries
scripts/build_acnc.py      builds the Figure 14 data from the raw ACNC files
scripts/build_dotdensity.mjs builds the Figure 4 dots from the SA4 boundaries
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
question blank. It appears **only** in Figures 6, 11, 12, 13 and two axes of 14, because the age tables
carry no population count per age group. Those charts say so in their subtitles, and the
page explains it once in the "Why do some percentages look a little different?" box.

Never plot the two against each other, and never quote a range without saying which one
it is on. Figures checked from the data:

- SA4 regions, `rate_pop15plus`: **6.3%** (Sydney – South West) to **24.0%** (WA Wheat Belt)
- State and territory falls 2016→2021, same denominator in both years:
  **3.0 to 5.9 percentage points**. Victoria furthest (−5.9); NT smallest (−3.0)
- Greater capital cities **13.2%**, rest of state **16.1%**
- 2,929,554 volunteers in 2021; **686,103 fewer** than in 2016

## The 14 charts

Specs are numbered in story order; `js/charts.js` maps each one to its `div` id.

| Fig | Spec | Idiom | Advanced? | Denominator |
|---|---|---|---|---|
| 1 | `01_trend_line.vg.json` | annotated line chart (GSS, 2006-2020) | basic | survey, 18+ |
| 2 | `02_waffle.vg.json` | faceted waffle / unit chart, 2016 vs 2021 | **advanced** | all 15+ |
| 3 | `03_choropleth_sa4.vg.json` | choropleth map, 88 SA4 regions | **advanced** | all 15+ |
| 4 | `04_dotdensity_sa4.vg.json` | dot density map, one dot = 4,000 volunteers | **advanced** | count |
| 5 | `05_bivariate_sa4.vg.json` | bivariate choropleth, rate x count, 3x3 key | **advanced** | both, see below |
| 6 | `06_agemaps_sa4.vg.json` | small-multiple choropleths, 4 age bands | same idiom as Fig 3 | respondents |
| 7 | `07_ranked_regions.vg.json` | lollipop chart, top and bottom 10 | **advanced** | all 15+ |
| 8 | `08_scatter_size_rate.vg.json` | scatterplot, population vs rate | basic | all 15+ |
| 9 | `09_dumbbell_state.vg.json` | connected dot plot (dumbbell) | **advanced** | all 15+ |
| 10 | `10_cartogram_state.vg.json` | hexagon tile cartogram on a real base map | **advanced** | all 15+ |
| 11 | `11_pyramid.vg.json` | population pyramid | **advanced** | respondents |
| 12 | `12_heatmap_age_state.vg.json` | heatmap, age x state | **advanced** | respondents |
| 13 | `13_ridgeline_ageband.vg.json` | ridgeline (kernel density) with medians | **advanced** | respondents |
| 14 | `14_purpose_bars.vg.json` | split bar chart by charitable purpose | basic | ACNC, self-reported |

**Ten advanced idioms, counting duplicates once.** The unit's rule (Ed, "Clarification
on Basic and Advanced Visualisation Idioms") is that anything not on the basic list counts
as advanced. The basic list is: bar charts (including stacked and grouped), dot plots
*excluding connected dot plots*, single- and multi-line charts, area charts, pie and donut
charts, scatterplots, bubble charts and packed bubble charts.

| # | Idiom | Figure |
|---|---|---|
| 1 | waffle chart | 2 |
| 2 | choropleth map | 3, repeated as small multiples in 6 |
| 3 | dot density map | 4 |
| 4 | bivariate choropleth | 5 |
| 5 | lollipop chart | 7 |
| 6 | connected dot plot (dumbbell) | 9 |
| 7 | tile cartogram | 10 |
| 8 | population pyramid | 11 |
| 9 | heatmap | 12 |
| 10 | ridgeline | 13 |

Waffle, lollipop, connected dot plot, population pyramid and heatmap are named outright in
the unit's list of advanced examples. The four map idioms and the ridgeline are advanced
because no entry on the basic list covers them.

Only three charts are basic: Figure 1 (line and area), Figure 8 (scatterplot) and Figure
14 (stacked bar). Figure 6 repeats Figure 3's idiom, so it adds a chart but not an idiom.

A cautious marker might fold the bivariate choropleth (5) into the plain choropleth (3),
which would leave nine. Either way the work is clear of the eight required.

A parallel coordinates plot of all 88 regions across five measures was built and then
dropped: it was legible only after heavy highlighting, and the count did not need it. The
spec and its data file are in `_superseded/`.


Four map idioms: choropleth (Fig 3), dot density (Fig 4), bivariate choropleth (Fig 5)
and tile cartogram (Fig 10). Fig 6 repeats the plain choropleth idiom
as small multiples, so it counts as one chart and adds no new idiom.

Interactions: Figures 4, 8 and 14 filter on a legend click. Figure 13 has a menu that
redraws every density for capital-city regions or the rest of the country on their own,
and its median lines recompute with it. Hovering gives region-level detail on 3, 4, 5, 6,
8, 12, 13 and 14.

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

### Figure 4 - how the dots are placed

`scripts/build_dotdensity.mjs` reads the SA4 boundaries, works out how many dots each
region needs (its volunteer count divided by 4,000) and rejection-samples that many points
inside the region's own polygons, picking a part in proportion to its area so multi-part
regions fill evenly. The generator is seeded, so the same map comes out every time it runs.
736 dots for 2,928,701 volunteers; no region fell short of its quota.

**The caveat is on the page, and it should stay there:** the dots are placed at random
inside each region. They show how many volunteers a region has, not where those people
live, and in the very large outback regions they spread over country where almost nobody
does. That is the known cost of a dot density map, and the figcaption says so rather than
hiding it.

An earlier version of this figure was a proportional symbol map positioned from
`data/sa4_centroids_2021.csv` (poles of inaccessibility, not plain centroids). It was
replaced because the circles for the east-coast capital regions overlapped too heavily to
read. Both that spec and the centroid file are in `_superseded/`.

### Figure 5 - how the nine classes are cut

Both variables are split into terciles of the 88 regions, so each class holds roughly the
same number of regions rather than the same width of values. Cut points, from the data:
rate **13.84%** and **16.54%**; volunteers **25,151** and **35,004**. The nine colours run
light-to-dark for the rate and teal-to-gold for the count, so a pale gold region is high
on both and a dark teal region is low on both. The scheme was checked for separation
between neighbouring classes and against the panel colour before use.

### Figure 14 - read before changing it

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
the repository. To rebuild Figure 14's data, download them again from
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
  <https://data.gov.au/data/dataset/acnc-register> (Figure 14; second data source)

## Acknowledgement

Generative AI was used throughout this project. The detail below is deliberately specific
rather than a blanket statement.

**Claude (Anthropic)** was used to:

- validate and reshape the downloaded ABS Census tables, and recalculate the volunteering
  rates and the 2016-2021 changes from them
- write the derivation scripts in `scripts/` and the small data files they produce
  (`acnc_purpose_split_2024.csv`, `dotdensity_sa4_2021.csv`, `bivariate_sa4_2021.csv`)
- write and debug the Vega-Lite specifications for every chart
- build the page layout and stylesheet, and choose and contrast-check the colour palettes
- draft and edit the wording of the headings, chart subtitles and the note under each chart
- check each chart idiom against the unit's basic and advanced lists

**ChatGPT (OpenAI)** was used to help plan the story structure, to prepare and check data,
to debug chart specifications, and to review wording.

**The coastline image in the page header (`img/hero-coast.png`) is AI-generated**, not a
photograph. `img/au-sa4-outline.svg` is not AI-generated: it is drawn from the ABS SA4
boundary file.

Every number quoted on the page is calculated from the files in `data/`, and those files
come from the ABS and ACNC sources listed above with no figures altered by hand. The
story, the choice of charts and every judgement about what to show and what to leave out
are mine; the wording was drafted with AI assistance and edited by me.
