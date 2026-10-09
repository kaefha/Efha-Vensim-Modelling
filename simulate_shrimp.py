import csv
import math
import random
from PIL import Image, ImageDraw, ImageFont

def simulate_fishery(
    p_price=2000.0,
    p_cost_boat=1000000.0,
    p_ramp_slope=3.0,
    p_eff_cap=None,
    p_max_fleet=None,
    p_init_fleet=50.0,
    p_init_shrimp=30000.0,
    p_r=0.5,
    p_k=37500.0,
    p_pct_change=0.05,
    p_thresh=0.2,
    p_noise=True,
    seed=5,
    dt=0.0625,
    t_start=2000.0,
    t_end=2100.0
):
    random.seed(seed)
    t = t_start
    shrimp = p_init_shrimp
    fleet = p_init_fleet
    
    times, s_list, f_list, c_list, cap_list, eff_list, earn_list, cost_list, m_list = (
        [], [], [], [], [], [], [], [], []
    )
    
    while t <= t_end + 1e-9:
        # boat efficiency
        raw_eff = 60.0 + p_ramp_slope * max(0.0, min(100.0, t - 2000.0))
        eff = min(p_eff_cap, raw_eff) if p_eff_cap is not None else raw_eff
        
        # catch capacity
        cap = eff * fleet
        ratio = shrimp / p_k
        
        # noise (deterministic or random normal)
        if p_noise:
            # Gaussian clamped between 0.8 and 1.2
            noise = max(0.8, min(1.2, random.gauss(1.0, 0.1)))
        else:
            noise = 1.0
            
        catch = cap * ratio * noise
        catch = max(0.0, min(shrimp / dt, catch))
        
        # natural growth
        pop_inc = p_r * shrimp * (1.0 - ratio) if ratio <= 1.0 else 0.0
        
        # economics
        earn = catch * p_price
        cost = fleet * p_cost_boat
        margin = (earn - cost) / cost if cost > 0 else 0.0
        
        # fleet adjustment
        if margin > p_thresh:
            net_change = p_pct_change * margin
        else:
            net_change = -p_pct_change * abs(margin)
            
        adj = net_change * fleet
        
        # apply fleet cap if policy active
        if p_max_fleet is not None and fleet >= p_max_fleet and adj > 0:
            adj = 0.0
            
        times.append(t)
        s_list.append(shrimp)
        f_list.append(fleet)
        c_list.append(catch)
        cap_list.append(cap)
        eff_list.append(eff)
        earn_list.append(earn)
        cost_list.append(cost)
        m_list.append(margin)
        
        d_shrimp = pop_inc - catch
        d_fleet = adj
        
        shrimp = max(0.0, shrimp + d_shrimp * dt)
        fleet = max(0.0, fleet + d_fleet * dt)
        t += dt
        
    return {
        "time": times,
        "shrimp": s_list,
        "fleet": f_list,
        "catch": c_list,
        "catch_capacity": cap_list,
        "boat_efficiency": eff_list,
        "earnings": earn_list,
        "costs": cost_list,
        "margin": m_list,
    }

# 1. Baseline Run
base = simulate_fishery()

with open("The Shrimp Fishery System/shrimp_baseline_sim.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Shrimp Population", "Fleet", "Catch", "Catch Capacity", "Boat Efficiency", "Earnings", "Costs", "Margin"])
    step = int(round(1.0 / 0.0625)) # save annual points
    for i in range(0, len(base["time"]), step):
        writer.writerow([
            f"{base['time'][i]:.2f}",
            f"{base['shrimp'][i]:.1f}",
            f"{base['fleet'][i]:.2f}",
            f"{base['catch'][i]:.1f}",
            f"{base['catch_capacity'][i]:.1f}",
            f"{base['boat_efficiency'][i]:.1f}",
            f"{base['earnings'][i]:.1f}",
            f"{base['costs'][i]:.1f}",
            f"{base['margin'][i]:.4f}"
        ])

# 2. Scenarios
# S1: Baseline
# S2: Subsidy / High Price Boom (Depletion Risk: Cost=$200k/boat, Price=$3500/ton)
boom = simulate_fishery(p_cost_boat=200000.0, p_price=3500.0)
# S3: Tech Leap (Ramp slope = 6.0)
tech = simulate_fishery(p_ramp_slope=6.0, p_cost_boat=350000.0)
# S4: Robust Intervention (Fleet cap = 30, Efficiency cap = 150 tons/boat, cost=$200k, price=$3500)
policy = simulate_fishery(p_cost_boat=200000.0, p_price=3500.0, p_max_fleet=30.0, p_eff_cap=150.0)

with open("The Shrimp Fishery System/shrimp_scenarios_sim.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Shrimp_Base", "Fleet_Base", "Shrimp_Boom", "Fleet_Boom", "Shrimp_Tech", "Fleet_Tech", "Shrimp_Policy", "Fleet_Policy"])
    step = int(round(1.0 / 0.0625))
    for i in range(0, len(base["time"]), step):
        writer.writerow([
            f"{base['time'][i]:.2f}",
            f"{base['shrimp'][i]:.1f}",
            f"{base['fleet'][i]:.2f}",
            f"{boom['shrimp'][i]:.1f}",
            f"{boom['fleet'][i]:.2f}",
            f"{tech['shrimp'][i]:.1f}",
            f"{tech['fleet'][i]:.2f}",
            f"{policy['shrimp'][i]:.1f}",
            f"{policy['fleet'][i]:.2f}"
        ])

print("Saved CSV simulation outputs successfully!")

# 3. Plotting Helper
def draw_panel(draw, font, font_bold, x, y, w, h, x_lim, y_lim, y_ticks, x_ticks, curves, labels, title, x_title="Year"):
    draw.rectangle([x, y, x + w, y + h], fill="white", outline="#333333", width=2)
    # Title
    t_box = font_bold.getbbox(title)
    draw.text((x + w//2 - (t_box[2]-t_box[0])//2, y - 24), title, fill="#111111", font=font_bold)
    
    # Grid Y
    for yt in y_ticks:
        if y_lim[0] <= yt <= y_lim[1]:
            py = y + h - (yt - y_lim[0]) / (y_lim[1] - y_lim[0]) * h
            draw.line([(x, py), (x + w, py)], fill="#DCDCDC", width=1)
            lbl = f"{int(yt):,}" if yt >= 10 or yt <= -10 or yt == 0 else f"{yt:.2f}"
            b = font.getbbox(lbl)
            draw.text((x - (b[2]-b[0]) - 8, py - (b[3]-b[1])//2), lbl, fill="#333333", font=font)
            
    # Grid X
    for xt in x_ticks:
        if x_lim[0] <= xt <= x_lim[1]:
            px = x + (xt - x_lim[0]) / (x_lim[1] - x_lim[0]) * w
            draw.line([(px, y), (px, y + h)], fill="#DCDCDC", width=1)
            lbl = f"{int(xt)}"
            b = font.getbbox(lbl)
            draw.text((px - (b[2]-b[0])//2, y + h + 6), lbl, fill="#333333", font=font)
            
    # X title
    b = font.getbbox(x_title)
    draw.text((x + w//2 - (b[2]-b[0])//2, y + h + 24), x_title, fill="#333333", font=font)
    
    # Curves
    for (xs, ys, color, width, dash) in curves:
        pts = []
        for xi, yi in zip(xs, ys):
            px = x + (xi - x_lim[0]) / (x_lim[0] - x_lim[0] + x_lim[1] - x_lim[0]) * w
            py = y + h - (yi - y_lim[0]) / (y_lim[1] - y_lim[0]) * h
            pts.append((px, py))
        if len(pts) > 1:
            draw.line(pts, fill=color, width=width)
            
    # Labels
    for text, (lx, ly), color in labels:
        px = x + (lx - x_lim[0]) / (x_lim[1] - x_lim[0]) * w
        py = y + h - (ly - y_lim[0]) / (y_lim[1] - y_lim[0]) * h
        draw.text((px, py), text, fill=color, font=font_bold)

try:
    font = ImageFont.truetype("arial.ttf", 15)
    font_bold = ImageFont.truetype("arialbd.ttf", 15)
except Exception:
    font = ImageFont.load_default()
    font_bold = font

# Generate Baseline BOT PNG (4 panels)
img_base = Image.new("RGB", (1000, 920), "white")
d_base = ImageDraw.Draw(img_base)

# Panel 1: Shrimp Biomass
c_shrimp = [(base["time"], base["shrimp"], "#0055aa", 3, False),
            (base["time"], [37500]*len(base["time"]), "#888888", 2, True)]
l_shrimp = [("Shrimp Population", (2015, 33000), "#0055aa"),
            ("Highest Population (37,500)", (2035, 38000), "#666666")]
draw_panel(d_base, font, font_bold, 80, 50, 400, 340, (2000, 2100), (25000, 40000),
           [25000, 30000, 35000, 40000], [2000, 2025, 2050, 2075, 2100],
           c_shrimp, l_shrimp, "Shrimp Population (tons)")

# Panel 2: Fleet Dynamics
c_fleet = [(base["time"], base["fleet"], "#cc3300", 3, False)]
l_fleet = [("Fleet (boats)", (2020, 25), "#cc3300")]
draw_panel(d_base, font, font_bold, 560, 50, 400, 340, (2000, 2100), (0, 60),
           [0, 10, 20, 30, 40, 50, 60], [2000, 2025, 2050, 2075, 2100],
           c_fleet, l_fleet, "Active Fleet Size (boats)")

# Panel 3: Catch & Capacity
c_catch = [(base["time"], base["catch"], "#2e7d32", 2, False),
           (base["time"], base["catch_capacity"], "#ff8f00", 2, False)]
l_catch = [("Catch (tons/yr)", (2035, 1200), "#2e7d32"),
           ("Catch Capacity", (2005, 3200), "#ff8f00")]
draw_panel(d_base, font, font_bold, 80, 500, 400, 340, (2000, 2100), (0, 4000),
           [0, 1000, 2000, 3000, 4000], [2000, 2025, 2050, 2075, 2100],
           c_catch, l_catch, "Catch & Harvesting Capacity (tons/year)")

# Panel 4: Economic Margin
c_margin = [(base["time"], base["margin"], "#6a1b9a", 3, False),
            (base["time"], [0.2]*len(base["time"]), "#888888", 2, True)]
l_margin = [("Margin", (2025, -0.65), "#6a1b9a"),
            ("Threshold Margin (0.2)", (2030, 0.25), "#666666")]
draw_panel(d_base, font, font_bold, 560, 500, 400, 340, (2000, 2100), (-1.0, 0.5),
           [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5], [2000, 2025, 2050, 2075, 2100],
           c_margin, l_margin, "Economic Profit Margin (Dmnl)")

img_base.save("The Shrimp Fishery System/shrimp_baseline_bots.png", "PNG")
print("Saved shrimp_baseline_bots.png!")

# Generate Scenarios Comparison PNG
img_scen = Image.new("RGB", (1000, 920), "white")
d_scen = ImageDraw.Draw(img_scen)

# Panel 1: Shrimp Population Comparison across Scenarios
c_s_comp = [
    (base["time"], base["shrimp"], "#2e7d32", 3, False),
    (boom["time"], boom["shrimp"], "#d32f2f", 3, False),
    (tech["time"], tech["shrimp"], "#f57c00", 2, False),
    (policy["time"], policy["shrimp"], "#1976d2", 3, False),
]
l_s_comp = [
    ("1. Baseline", (2055, 36000), "#2e7d32"),
    ("2. Subsidized Boom (Collapse!)", (2045, 5500), "#d32f2f"),
    ("3. Rapid Tech Creep", (2035, 12000), "#f57c00"),
    ("4. Robust Policy Intervention", (2045, 28000), "#1976d2"),
]
draw_panel(d_scen, font, font_bold, 80, 50, 880, 360, (2000, 2100), (0, 40000),
           [0, 10000, 20000, 30000, 40000], [2000, 2020, 2040, 2060, 2080, 2100],
           c_s_comp, l_s_comp, "Shrimp Biomass: Scenarios & Policy Interventions (tons)")

# Panel 2: Fleet Comparison across Scenarios
c_f_comp = [
    (base["time"], base["fleet"], "#2e7d32", 3, False),
    (boom["time"], boom["fleet"], "#d32f2f", 3, False),
    (tech["time"], tech["fleet"], "#f57c00", 2, False),
    (policy["time"], policy["fleet"], "#1976d2", 3, False),
]
l_f_comp = [
    ("1. Baseline", (2040, 10), "#2e7d32"),
    ("2. Boom & Bust Fleet Overcapacity", (2025, 75), "#d32f2f"),
    ("3. Tech Creep", (2050, 45), "#f57c00"),
    ("4. Robust Intervention (Cap 30)", (2065, 33), "#1976d2"),
]
draw_panel(d_scen, font, font_bold, 80, 490, 880, 360, (2000, 2100), (0, 100),
           [0, 20, 40, 60, 80, 100], [2000, 2020, 2040, 2060, 2080, 2100],
           c_f_comp, l_f_comp, "Fishing Fleet Size: Scenarios & Policy Interventions (boats)")

img_scen.save("The Shrimp Fishery System/shrimp_scenarios_comparison.png", "PNG")
print("Saved shrimp_scenarios_comparison.png!")
