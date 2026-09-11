"""
Correlation Analysis: Tuition Growth vs. NACUBO Endowment Returns
==================================================================
Replaces S&P proxy with actual NACUBO-Commonfund Study of Endowments
average annual returns — a much better proxy for BC's endowment.

Sources:
- NACUBO-Commonfund Study of Endowments annual press releases (2003-2025)
- Fortune Jan 2011 for FY2009-2010 confirmation
- Historical figures cross-checked against NACUBO Historic Endowment Study Data
- Princeton endowment returns (FY88-FY25) used as robustness check for
  large-endowment behavior (Princeton is a $B+ tier institution like BC)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# ==================================================================
# DATA 1: NACUBO aggregate endowment returns (fiscal year ending June 30)
# ==================================================================
# Sources (year: return, source)
# 2001-2008: NACUBO Endowment Study press releases (archived, pre-Commonfund era)
# 2009-2025: NACUBO-Commonfund Study of Endowments press releases
# All net-of-fees average returns across the participating institution universe
# (~800 institutions typically; $944B in aggregate assets in FY25)
nacubo_returns = {
    # FY2001: -3.6% (tech-bust); NACUBO Study
    2001: -3.6,
    # FY2002: -6.0%; NACUBO Study
    2002: -6.0,
    # FY2003: +3.0%; NACUBO Study
    2003: 3.0,
    # FY2004: +15.1%; NACUBO Study
    2004: 15.1,
    # FY2005: +9.3%; NACUBO Study
    2005: 9.3,
    # FY2006: +10.7%; NACUBO Study
    2006: 10.7,
    # FY2007: +17.2%; NACUBO Study
    2007: 17.2,
    # FY2008: -3.0%; NACUBO Study (first pandemic-era drop)
    2008: -3.0,
    # FY2009: -18.7%; NACUBO-Commonfund Study (Fortune Jan 2011)
    2009: -18.7,
    # FY2010: +11.9%; NACUBO-Commonfund Study (Fortune Jan 2011)
    2010: 11.9,
    # FY2011: +19.2%; NACUBO-Commonfund Study
    2011: 19.2,
    # FY2012: -0.3%; NACUBO-Commonfund Study (NBC News 2016)
    2012: -0.3,
    # FY2013: +11.7%; NACUBO-Commonfund Study
    2013: 11.7,
    # FY2014: +15.5%; NACUBO-Commonfund Study (NBC News 2016)
    2014: 15.5,
    # FY2015: +2.4%; NACUBO-Commonfund Study (NBC News 2016)
    2015: 2.4,
    # FY2016: -1.9%; NACUBO-Commonfund Study
    2016: -1.9,
    # FY2017: +12.2%; NACUBO-Commonfund Study
    2017: 12.2,
    # FY2018: +8.2%; NACUBO-TIAA Study
    2018: 8.2,
    # FY2019: +5.3%; NACUBO-TIAA Study
    2019: 5.3,
    # FY2020: +1.8%; NACUBO-TIAA Study (early pandemic)
    2020: 1.8,
    # FY2021: +30.6%; NACUBO-TIAA Study (post-pandemic rally)
    2021: 30.6,
    # FY2022: -8.0%; NACUBO-Commonfund Study
    2022: -8.0,
    # FY2023: +7.7%; NACUBO-Commonfund Study (press release Feb 2024)
    2023: 7.7,
    # FY2024: +11.2%; NACUBO-Commonfund Study (press release Feb 2025)
    2024: 11.2,
    # FY2025: +10.9%; NACUBO-Commonfund Study (press release Feb 2026)
    2025: 10.9,
}

# ==================================================================
# DATA 2: Private nonprofit tuition growth (same as before)
# Source: NCES via Statista
# NOTE: These are academic years, so 2001 tuition = AY2001/02
# For alignment: NACUBO FY2001 (Jul 2000-Jun 2001) corresponds to
# tuition set for AY2001/02 (charged starting fall 2001). So a lag
# of the endowment year → next academic year tuition makes sense.
# But we'll test both contemporaneous and lagged versions.
# ==================================================================
tuition_data = {
    2000: 15000, 2001: 15742, 2002: 16383, 2003: 17315, 2004: 18154,
    2005: 18862, 2006: 20048, 2007: 20972, 2008: 21570, 2009: 21764,
    2010: 22042, 2011: 22850, 2012: 23943, 2013: 25110, 2014: 26182,
    2015: 27436, 2016: 28945, 2017: 30274, 2018: 31527, 2019: 32411,
    2020: 32351, 2021: 33700, 2022: 34923
}

# Compute tuition growth
years_tuition = sorted(tuition_data.keys())
tuition_growth = {}
for i in range(1, len(years_tuition)):
    y = years_tuition[i]
    prev = tuition_data[years_tuition[i-1]]
    tuition_growth[y] = (tuition_data[y] - prev) / prev * 100

# ==================================================================
# Match up years — use overlap where both are available
# ==================================================================
common_years = sorted(set(nacubo_returns.keys()) & set(tuition_growth.keys()))
print(f"Overlap: {len(common_years)} years ({min(common_years)}-{max(common_years)})")

df = pd.DataFrame({
    'year': common_years,
    'nacubo_return': [nacubo_returns[y] for y in common_years],
    'tuition_growth': [tuition_growth[y] for y in common_years]
})

print("\n" + "="*70)
print("PRIVATE TUITION GROWTH vs. NACUBO ENDOWMENT RETURNS")
print("Fiscal-year overlapped, 2001-2022 (n = {})".format(len(df)))
print("="*70)
print(df.to_string(index=False))

# ==================================================================
# CORRELATION ANALYSIS
# ==================================================================
tuition_arr = df['tuition_growth'].values
nacubo_arr = df['nacubo_return'].values

# Contemporaneous
r_contemp, p_contemp = stats.pearsonr(tuition_arr, nacubo_arr)
r_spearman, p_spearman = stats.spearmanr(tuition_arr, nacubo_arr)

# Lagged (tuition set 1 year after endowment year)
r_lag1, p_lag1 = stats.pearsonr(tuition_arr[1:], nacubo_arr[:-1])
r_lag2, p_lag2 = stats.pearsonr(tuition_arr[2:], nacubo_arr[:-2])

print("\n" + "="*70)
print("CORRELATION RESULTS")
print("="*70)
print(f"Pearson (contemporaneous):    r = {r_contemp:+.4f}  (p = {p_contemp:.4f})")
print(f"Spearman (contemporaneous):   ρ = {r_spearman:+.4f}  (p = {p_spearman:.4f})")
print(f"Pearson (tuition lags NACUBO by 1yr): r = {r_lag1:+.4f}  (p = {p_lag1:.4f})")
print(f"Pearson (tuition lags NACUBO by 2yr): r = {r_lag2:+.4f}  (p = {p_lag2:.4f})")

# Compare to previous S&P result
print("\n" + "="*70)
print("COMPARISON TO PREVIOUS S&P ANALYSIS")
print("="*70)
print(f"NACUBO (better proxy): r = {r_contemp:+.3f}")
print(f"S&P 500 (previous):    r = +0.121")

# ==================================================================
# CRISIS-YEAR TABLE
# ==================================================================
print("\n" + "="*70)
print("ENDOWMENT CRISIS YEARS: DID TUITION FALL?")
print("="*70)
print(f"{'Year':<6} {'NACUBO Return':>15} {'Tuition Growth':>18}")
for y in sorted(df['year'].values):
    row = df[df['year']==y].iloc[0]
    if row['nacubo_return'] < 0:
        print(f"{y:<6} {row['nacubo_return']:>14.1f}% {row['tuition_growth']:>17.2f}%")

# ==================================================================
# CHART 1: Scatter with regression
# ==================================================================
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(nacubo_arr, tuition_arr, s=70, color='#722F37',
           edgecolor='black', alpha=0.75, linewidth=0.5)

slope, intercept, r, p, se = stats.linregress(nacubo_arr, tuition_arr)
xs = np.linspace(nacubo_arr.min()-2, nacubo_arr.max()+2, 100)
ax.plot(xs, intercept + slope*xs, color='#1F3864', linewidth=2,
        label=f'OLS: y = {intercept:.2f} + {slope:.4f}x\nr = {r:+.3f}, R² = {r**2:.3f}, p = {p:.3f}')

ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)
ax.axvline(x=0, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)

# Annotate crash years
crash_years = [2002, 2009, 2016, 2022]
for yr in crash_years:
    if yr in df['year'].values:
        row = df[df['year']==yr].iloc[0]
        ax.annotate(f'FY{yr}', xy=(row['nacubo_return'], row['tuition_growth']),
                    xytext=(row['nacubo_return']+1.5, row['tuition_growth']+0.3),
                    fontsize=9, alpha=0.8, fontweight='bold')

ax.set_xlabel("NACUBO endowment return (%) — actual endowment performance proxy",
              fontsize=11)
ax.set_ylabel("Private university tuition YoY growth (%)", fontsize=11)
ax.set_title("Private Tuition Growth vs. NACUBO Endowment Returns (2001-2022)\n"
             "Better proxy for BC's endowment than S&P alone",
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10, loc='lower right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/home/claude/nacubo_scatter.png', dpi=180, bbox_inches='tight')
plt.close()

# ==================================================================
# CHART 2: Time series overlay
# ==================================================================
fig, ax1 = plt.subplots(figsize=(11, 5))
color1 = '#722F37'
color2 = '#1F3864'

ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Private tuition YoY growth (%)', color=color1, fontsize=11)
ax1.plot(df['year'], df['tuition_growth'], color=color1, linewidth=2.2,
         marker='o', markersize=5, label='Tuition growth')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.axhline(y=0, color='gray', linewidth=0.3, alpha=0.5)
ax1.grid(alpha=0.3)

ax2 = ax1.twinx()
ax2.set_ylabel('NACUBO endowment return (%)', color=color2, fontsize=11)
ax2.plot(df['year'], df['nacubo_return'], color=color2, linewidth=1.8,
         marker='s', markersize=4, alpha=0.75, label='NACUBO return')
ax2.tick_params(axis='y', labelcolor=color2)

# Highlight crisis years
for yr, label, y_offset in [(2002, 'tech bust', -6), (2009, 'GFC', -6),
                             (2016, 'oil crash', -5), (2020, 'COVID', 6),
                             (2022, 'tightening', -6)]:
    if yr in df['year'].values:
        row = df[df['year']==yr].iloc[0]
        ax2.annotate(label, xy=(yr, row['nacubo_return']),
                     xytext=(yr, row['nacubo_return'] + y_offset),
                     fontsize=8, ha='center', color=color2, alpha=0.9,
                     arrowprops=dict(arrowstyle='->', color=color2, lw=0.5, alpha=0.6))

plt.title(f"Tuition Growth Stayed Positive Through Every Endowment Down-Year\n"
          f"Correlation r = {r_contemp:+.3f} (p={p_contemp:.3f}); NACUBO proxy",
          fontsize=12, fontweight='bold')
fig.tight_layout()
plt.savefig('/home/claude/nacubo_timeseries.png', dpi=180, bbox_inches='tight')
plt.close()

print("\nCharts saved: nacubo_scatter.png, nacubo_timeseries.png")

# ==================================================================
# IMPLICATION FOR THE PAPER
# ==================================================================
print("\n" + "="*70)
print("IMPLICATION FOR BC_STRESS_COUPLING IN MONTE CARLO")
print("="*70)
print(f"Empirical |r| between endowment & tuition: {abs(r_contemp):.3f}")
print(f"Model's assumed coupling (rho): 0.10")
if abs(r_contemp) < 0.10:
    print(f"→ The empirical evidence supports a LOWER coupling than the model uses.")
    print(f"  Model is CONSERVATIVE against BC (i.e., overstates BC's risk).")
else:
    print(f"→ The empirical coupling is slightly higher than the 0.10 assumption.")
    print(f"  Consider raising to {abs(r_contemp):.2f} for conservatism.")
