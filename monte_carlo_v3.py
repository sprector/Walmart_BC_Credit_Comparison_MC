"""
Correlated Monte Carlo: BC vs Walmart 30-year bond
=====================================================
UPDATED INPUTS: Uses Moody's published Aa 10-year CDRs directly
- BC: 0.03% (Aa muni)
- Walmart: 0.96% (Aa corporate)
Same systematic stress factor mechanism for default-recovery correlation.
"""
import numpy as np
from scipy.stats import beta as beta_dist
import matplotlib.pyplot as plt

np.random.seed(42)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# =================================================================
# SIMULATION PARAMETERS
# =================================================================
N_PATHS = 10_000
HORIZON = 30
NOTIONAL = 200_000_000

# =================================================================
# INPUTS
# =================================================================
# BC: Moody's Aa muni 10-yr CDR = 0.03%
# Source: Moody's "US Municipal Bond Defaults and Recoveries, 1970-2022"
BC_10YR_CDR = 0.0003
BC_BASE_PD = 1 - (1 - BC_10YR_CDR)**(1/10)  # ≈ 0.00300%/yr
BC_RECOVERY_MEAN = 0.57
BC_RECOVERY_STD = 0.20
BC_STRESS_COUPLING = 0.10

# Walmart: Moody's Aa corporate 10-yr CDR = 0.96%
# Source: Moody's Annual Default Study (1983-2022 sample)
WMT_10YR_CDR = 0.0096
WMT_BASE_PD = 1 - (1 - WMT_10YR_CDR)**(1/10)  # ≈ 0.0964%/yr
WMT_RECOVERY_MEAN = 0.35
WMT_RECOVERY_STD = 0.22
WMT_STRESS_COUPLING = 0.60

print("Updated inputs:")
print(f"  BC annual hazard:  {BC_BASE_PD*100:.5f}% → 30-yr cum: {(1-(1-BC_BASE_PD)**30)*100:.3f}%")
print(f"  WMT annual hazard: {WMT_BASE_PD*100:.5f}% → 30-yr cum: {(1-(1-WMT_BASE_PD)**30)*100:.3f}%")
print(f"  Ratio (WMT / BC):  {WMT_BASE_PD/BC_BASE_PD:.1f}x annual, {((1-(1-WMT_BASE_PD)**30)/(1-(1-BC_BASE_PD)**30)):.1f}x cumulative")

# =================================================================
# BETA HELPER
# =================================================================
def beta_params(mean, std):
    var = std**2
    common = mean*(1-mean)/var - 1
    return mean*common, (1-mean)*common

# =================================================================
# SIMULATION ENGINE (Systematic Stress Factor)
# =================================================================
def simulate(base_pd, rec_mean, rec_std, coupling, label):
    losses = np.zeros(N_PATHS)
    default_years = np.full(N_PATHS, np.nan)
    recoveries_at_default = []
    
    for i in range(N_PATHS):
        for t in range(1, HORIZON+1):
            S_t = np.random.standard_normal()
            adjusted_pd = base_pd * np.exp(coupling * S_t)
            adjusted_pd = min(adjusted_pd, 0.5)
            
            if np.random.random() < adjusted_pd:
                shifted_mean = rec_mean - coupling * 0.15 * S_t
                shifted_mean = np.clip(shifted_mean, 0.05, 0.95)
                alpha, b = beta_params(shifted_mean, rec_std)
                if alpha > 0 and b > 0:
                    recovery = np.random.beta(alpha, b)
                else:
                    recovery = shifted_mean
                losses[i] = NOTIONAL * (1 - recovery)
                default_years[i] = t
                recoveries_at_default.append(recovery)
                break
    
    n_def = int(np.sum(~np.isnan(default_years)))
    avg_rec = np.mean(recoveries_at_default) if recoveries_at_default else float('nan')
    
    print(f"\n{'='*70}")
    print(f"{label} (base_pd={base_pd*100:.4f}%/yr, coupling={coupling})")
    print(f"{'='*70}")
    print(f"Defaults: {n_def}/{N_PATHS} ({n_def/N_PATHS*100:.2f}%)")
    print(f"Mean recovery | default:    {avg_rec*100:.1f}%")
    print(f"Base recovery (no stress):  {rec_mean*100:.1f}%")
    print(f"Mean loss (all paths):      ${losses.mean():>14,.0f}")
    print(f"Median loss:                ${np.median(losses):>14,.0f}")
    print(f"95th percentile loss:       ${np.percentile(losses, 95):>14,.0f}")
    print(f"99th percentile loss:       ${np.percentile(losses, 99):>14,.0f}")
    print(f"99.5th percentile loss:     ${np.percentile(losses, 99.5):>14,.0f}")
    print(f"Worst-case loss:            ${losses.max():>14,.0f}")
    
    return losses, default_years, recoveries_at_default

print(f"\nMonte Carlo: {N_PATHS:,} paths × {HORIZON} years × $200mm notional")

bc_losses, bc_def, bc_recs = simulate(
    BC_BASE_PD, BC_RECOVERY_MEAN, BC_RECOVERY_STD,
    BC_STRESS_COUPLING, "BOSTON COLLEGE (Aa muni CDR 0.03%)")
wmt_losses, wmt_def, wmt_recs = simulate(
    WMT_BASE_PD, WMT_RECOVERY_MEAN, WMT_RECOVERY_STD,
    WMT_STRESS_COUPLING, "WALMART (Aa corporate CDR 0.96%)")

# =================================================================
# COMPARISON
# =================================================================
print(f"\n{'='*70}")
print("WALMART vs. BC")
print(f"{'='*70}")
mean_ratio = wmt_losses.mean() / max(bc_losses.mean(), 1)
p99_bc = max(np.percentile(bc_losses, 99), 1)
p99_wmt = np.percentile(wmt_losses, 99)
print(f"Mean loss:            BC ${bc_losses.mean()/1e6:.2f}mm  vs.  WMT ${wmt_losses.mean()/1e6:.2f}mm  ({mean_ratio:.1f}x)")
print(f"99th percentile loss: BC ${np.percentile(bc_losses,99)/1e6:.1f}mm vs.  WMT ${p99_wmt/1e6:.1f}mm  ({p99_wmt/p99_bc:.1f}x)")

# =================================================================
# CHARTS
# =================================================================

# Chart 1: Conditional loss distributions
fig, ax = plt.subplots(figsize=(10, 5))
bins = np.linspace(0, 200, 50)
bc_def_loss = bc_losses[bc_losses > 0] / 1e6
wmt_def_loss = wmt_losses[wmt_losses > 0] / 1e6
if len(bc_def_loss) > 0:
    ax.hist(bc_def_loss, bins=bins, color='#722F37', alpha=0.65,
            label=f'BC (n={len(bc_def_loss)} defaults)',
            edgecolor='black', linewidth=0.3)
ax.hist(wmt_def_loss, bins=bins, color='#FFC220', alpha=0.65,
        label=f'Walmart (n={len(wmt_def_loss)} defaults)',
        edgecolor='black', linewidth=0.3)
ax.set_xlabel("Realized loss ($mm) — paths with default only", fontsize=11)
ax.set_ylabel("Number of paths", fontsize=11)
ax.set_title("Conditional Loss Distributions (Default Paths Only)\nAa muni 0.03% vs Aa corp 0.96% base CDR; BC ρ=0.10, WMT ρ=0.60",
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/home/claude/mc_v3_conditional.png', dpi=180, bbox_inches='tight')
plt.close()

# Chart 2: Tail loss comparison across full distribution
fig, ax = plt.subplots(figsize=(10, 5))
percentiles = [50, 75, 90, 95, 99, 99.5, 99.9]
bc_pcts = [np.percentile(bc_losses, p)/1e6 for p in percentiles]
wmt_pcts = [np.percentile(wmt_losses, p)/1e6 for p in percentiles]
x = np.arange(len(percentiles))
w = 0.38
ax.bar(x - w/2, bc_pcts, w, color='#722F37', label='Boston College',
       edgecolor='black', linewidth=0.5)
ax.bar(x + w/2, wmt_pcts, w, color='#FFC220', label='Walmart',
       edgecolor='black', linewidth=0.5)
for i, (b, wv) in enumerate(zip(bc_pcts, wmt_pcts)):
    ax.text(i - w/2, b + 3, f'${b:.0f}' if b > 1 else '$0', ha='center', fontsize=8)
    ax.text(i + w/2, wv + 3, f'${wv:.0f}' if wv > 1 else '$0', ha='center', fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels([f'{p}th' for p in percentiles])
ax.set_xlabel("Percentile of loss distribution", fontsize=11)
ax.set_ylabel("Loss at percentile ($mm)", fontsize=11)
ax.set_title("Tail Loss Comparison Across Full Distribution\nMoody's published Aa CDRs + systematic stress coupling",
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3, axis='y')
ax.set_ylim(0, max(wmt_pcts)*1.15 if max(wmt_pcts) > 0 else 100)
plt.tight_layout()
plt.savefig('/home/claude/mc_v3_tail.png', dpi=180, bbox_inches='tight')
plt.close()

print("\nCharts saved: mc_v3_conditional.png, mc_v3_tail.png")
