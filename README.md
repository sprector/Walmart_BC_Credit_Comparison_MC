# Walmart_BC_Credit_Comparison_MC
MFIN2250 Fixed Income Project: Comparing a Boston College-backed bond with a similar Walmart-backed bond from a quantitative investment lens.

# BC vs. Walmart: A 30-Year Bond Credit Analysis

Quantitative credit analysis comparing a hypothetical $200mm investment in a 30-year senior bond issued by Boston College versus one issued by Walmart. Both bonds priced at par with a 5% coupon, non-callable, taxable, senior, with rights to all assets. Hold-to-maturity mandate.

**Conclusion:** Invest in the Boston College bond.

The analysis argues that at identical par-to-par pricing, Boston College offers a materially better risk-adjusted profile for a 30-year non-callable bondholder than Walmart, despite Walmart's one-notch rating advantage. The case rests on three legs: reference-class default base rates (outside view), asset-cushion analysis (inside view balance sheet), and structural alignment between the issuer and bondholder incentives.

## Repository Contents

### Written analysis
- `BC_vs_Walmart_Credit_Analysis.docx` — the paper itself (~3,700 words, 11 pages)
- `BC_vs_Walmart_Credit_Analysis.pdf` — PDF export

### Quantitative work
- `monte_carlo_v3.py` — Monte Carlo simulation with published Aa cumulative default rates and systematic stress-factor correlation
- `nacubo_correlation.py` — same, using NACUBO endowment index (better proxy for BC's actual holdings)

## Analytical Framework

### The Four Cs

Character, Capacity, Capital (Collateral), and Conditions. Each C is analyzed with parallel treatment of both issuers under both inside-view and outside-view lenses.

- **Character** — governance alignment with bondholders; BC has structural insulation from equity-holder pressure that Walmart lacks over a 30-year horizon.
- **Capacity** — flow-based coverage; Walmart wins by a wide margin (13x ICR), BC wins on wealth-to-debt cushion (endowment ≈ 4x debt).
- **Collateral** — the key insight: BC's asset base is uncorrelated with its revenue stream; Walmart's is highly correlated (housing-2008 mechanism applied to retail). Empirical Sears precedent quantifies this at ~28% real estate recovery in retail liquidation.
- **Conditions** — bifurcated higher-ed sector outlook (Moody's negative overall but positive/stable for well-resourced schools) versus non-linear retail disruption risk.

### Inside vs. Outside View (Kahneman & Lovallo)

- **Inside view** favors Walmart on virtually every snapshot metric — higher rating, larger revenue, deeper coverage.
- **Outside view** favors BC by two orders of magnitude — the reference-class 30-year cumulative default rate for Aa-rated public finance issuers is ~25-100x lower than for Aa-rated corporates, and empirically the top-decile endowed university cohort has zero modern-era defaults.

Reference classes constructed:
1. Aa-rated public finance (Moody's 2013-2022 CDR: 0.03%)
2. Aa-rated corporates (Moody's 1983-2022 CDR: 0.96%)
3. Top-decile endowed U.S. private universities (empirical: no defaults since founding)
4. 1995 cohort of large U.S. general merchandise retailers (empirical: 35% default rate by 2025)

### Monte Carlo Simulation

10,000 paths × 30 years × $200mm notional for each issuer. Uses:

- **Annual hazard rate**: base default probability derived from Moody's published Aa cumulative default rates (0.03% muni, 0.96% corporate)
- **Recovery distribution**: Beta distribution parameterized by mean and standard deviation
  - BC: Beta(mean=57%, std=20%) — based on 67% issuer-weighted muni recovery, 47% corporate senior unsecured recovery
  - Walmart: Beta(mean=35%, std=22%) — based on 37% trading-price recovery, 30-54% retail-specific range from LSTA
- **Systematic stress factor**: each year draws S_t ~ N(0,1); coupling parameter controls how strongly stress affects both hazard rate and recovery
  - BC coupling = 0.25 (empirically calibrated from tuition-vs-NACUBO correlation)
  - Walmart coupling = 0.60 (empirically calibrated from Moody's R² = 0.55-0.65 corporate default-recovery regression, applied to the retail sector)

### Key Results

| Metric | Boston College | Walmart | Ratio |
|---|---|---|---|
| Default rate (30yr) | 0.14% | 3.59% | 26x |
| Mean recovery given default | 47% | 30% | 0.6x |
| Mean loss | $0.15mm | $5.0mm | 34x |
| 99th percentile loss | $0 | $178mm | ∞ |

## Class Topics Integrated

Covers all quantitative concepts from the fixed income course:
- Spot rates and forward rates (§2.1, with bootstrapped 1-year forwards)
- Real yields (§2.2, TIPS breakeven analysis)
- Duration, DV01, and convexity (§2.3, Macaulay 15.83, mod duration 15.45, DV01 $309K/bp on $200mm)
- Binomial tree and Monte Carlo (§5, formalized premortem)
- Credit and CVA (§4, deterministic and stochastic)
- ABS-style asset coverage (§3.3, over-collateralization framing)
- CDS (§4.4, hazard-rate implied from spreads, basis argument)
- LDI and portfolio management (§6, duration matching and Markowitz)

## Sources

### Financial data
- Boston College audited financial statements FY24 (bc.edu FVP office)
- Boston College FY25 financial statement summary (via *The Heights*, Nov. 5, 2025)
- Walmart Form 10-K for fiscal year ended January 31, 2025 (SEC EDGAR accession 0000104169-25-000021)
- Walmart Q3 FY26 Form 10-Q (SEC EDGAR)
- NCES Digest of Education Statistics (via Statista, private nonprofit tuition 1969-2023)
- NACUBO-Commonfund Study of Endowments (aggregate returns 2001-2025)

### Credit and default data
- Moody's, "US Municipal Bond Defaults and Recoveries, 1970-2022" (July 2023)
- Moody's, "Corporate Default and Recovery Rates, 1920-2023" (annual default study)
- Moody's, "Default and Recovery Rates of Corporate Bond Issuers, 1920-2004" (Jan 2005) — for R² = 0.65 default/recovery regression
- LSTA, "Recoveries: Past, Present and Future" (June 2019) — retail-specific recovery data
- Retail Dive bankruptcy tracker; CNBC 2020 retail bankruptcy summary

### Sector outlook
- Moody's Higher Education Sector Outlook (March 2025, November 2025)
- S&P U.S. Not-For-Profit Higher Education Outlook 2026
- Federal Reserve Bank of Philadelphia Working Paper 24-20 (Dec 2024) on college closures
- Tarrant, Bray & Katsinas (2018), "The Invisible Colleges Revisited," *J. of Higher Education* 89(3)

### Rates and market data
- U.S. Treasury Daily Par Yield Curve (April 28, 2026)
- Federal Reserve H.15 Selected Interest Rates
- FRED DFII30 (30-year TIPS)
- S&P 500 historical returns via Damodaran / NYU Stern

### Frameworks
- Kahneman & Lovallo, "Timid Choices and Bold Forecasts," *Management Science* 39:1 (1993)
- Kahneman, *Thinking, Fast and Slow* (2011) — inside/outside view
- Klein, "Performing a Project Premortem," *Harvard Business Review* (September 2007)

## Methodology Notes

**Reference class construction.** BC's true peer set is top-decile endowed U.S. private universities (empirically zero defaults). Walmart's true peer set is large U.S. general merchandise retailers, of which 35% defaulted over the 1995-2025 window. Using rating-class base rates (Moody's Aa muni and Aa corporate) provides the most defensible middle ground and is what the Monte Carlo uses.

**Stress coupling calibration.** The BC coupling of 0.25 comes from an empirical correlation analysis of private tuition growth vs. NACUBO endowment returns (r = 0.267 over 2001-2022). The Walmart coupling of 0.60 sits below the empirical ceiling from Moody's all-corporate default-recovery regression (R² = 0.55-0.65 implies correlation of 0.74-0.81); the discount reflects Walmart being the strongest issuer within the retail sector.

**What the model excludes.** Interest rate paths (irrelevant for hold-to-maturity); rating migration; partial impairment short of default; time-varying hazard rates; contagion across paths. Adding any of these would sharpen the asymmetry rather than narrow it.

## Reproducing the Analysis

```bash
pip install numpy pandas scipy matplotlib
python3 build_charts.py            # yield curve, DV01, basic charts
python3 reference_class_analysis.py # reference classes
python3 correlation_analysis.py    # S&P proxy
python3 nacubo_correlation.py      # NACUBO proxy (preferred)
python3 monte_carlo_v3.py          # main Monte Carlo simulation
```

All charts render to PNG at 180 DPI. Random seed 42 is set for reproducibility.

## Caveats

**The 99th-percentile framing.** The Monte Carlo shows a 99th-percentile Walmart loss of ~$178mm versus BC's ~$0. That's a striking number, but it depends on the stress-coupling assumption; the sensitivity table in the Monte Carlo output shows the ratio is robust across coupling values of 0-0.9.

**The reference class boundaries.** Whether BC belongs in the Aa muni reference class (0.03% 10-yr CDR) or the Aa corporate reference class (0.96%) is a judgment call. BC's bond is legally taxable corporate-style, but its issuer profile — nonprofit, large endowment, no shareholders, regulated revenue — sits closer to the muni end. The paper uses both and lets the reader see the range.

**The Boston College vs. Boston College High School distinction.** In the premortem section, references to "BC" mean the university. The 2002-2003 Catholic Church abuse scandal that surfaces on any casual search largely involves Boston College High School (a separate Jesuit secondary school in Dorchester) and the Archdiocese of Boston — both legally distinct from the Trustees of Boston College. The university itself was not implicated in the Spotlight investigation.

**Data vintage.** All financials are as of the most recent available reporting date (BC FY25 summary as of May 31, 2025; Walmart Q3 FY26 as of October 31, 2025). Rate data is as of late April 2026.
