import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "font.size": 11})


print("Loading data...")
train        = pd.read_csv("store-sales-time-series-forecasting/train.csv",            parse_dates=["date"])
holidays     = pd.read_csv("store-sales-time-series-forecasting/holidays_events.csv",  parse_dates=["date"])
oil          = pd.read_csv("store-sales-time-series-forecasting/oil.csv",              parse_dates=["date"])
transactions = pd.read_csv("store-sales-time-series-forecasting/transactions.csv",     parse_dates=["date"])
stores       = pd.read_csv("store-sales-time-series-forecasting/stores.csv")
submission   = pd.read_csv("store-sales-time-series-forecasting/submission.csv")
test         = pd.read_csv("store-sales-time-series-forecasting/test.csv",             parse_dates=["date"])

train = train.merge(stores, on="store_nbr", how="left")
oil   = oil.set_index("date").resample("D").first().ffill().reset_index()
oil.rename(columns={"dcoilwtico": "oil_price"}, inplace=True)

print("="*65)
print("  TASK 4 — SAD REPORT INSIGHTS")
print("="*65)


print("\n── INSIGHT 1: Demand Drivers ──")


holiday_dates = set(holidays["date"])
train["is_holiday"] = train["date"].isin(holiday_dates)
hol = train.groupby("is_holiday")["sales"].mean()
lift = ((hol[True] - hol[False]) / hol[False]) * 100
print(f"  Holiday Sales Lift     : +{lift:.1f}% vs normal days")

promo = train.groupby(train["onpromotion"] > 0)["sales"].mean()
promo_lift = ((promo[True] - promo[False]) / promo[False]) * 100
print(f"  Promotion Sales Lift   : +{promo_lift:.1f}% when items on promotion")


daily_sales = train.groupby("date")["sales"].sum().reset_index()
merged_oil  = daily_sales.merge(oil, on="date", how="inner").dropna()
corr        = merged_oil["sales"].corr(merged_oil["oil_price"])
print(f"  Oil Price Correlation  : {corr:.4f} (negative = sales drop when oil drops)")


fig, axes = plt.subplots(1, 3, figsize=(15, 5))


axes[0].bar(["Normal Day", "Holiday"],
            [hol[False], hol[True]],
            color=["#888780", "#D85A30"], edgecolor="white", width=0.45)
axes[0].set_title("Holiday Impact on Sales", fontweight="bold")
axes[0].set_ylabel("Avg Sales")
for bar, val in zip(axes[0].patches, [hol[False], hol[True]]):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                 f"{val:,.1f}", ha="center", fontsize=10, fontweight="bold")

# Promotion
axes[1].bar(["No Promo", "On Promotion"],
            [promo[False], promo[True]],
            color=["#888780", "#1D9E75"], edgecolor="white", width=0.45)
axes[1].set_title("Promotion Impact on Sales", fontweight="bold")
axes[1].set_ylabel("Avg Sales")
for bar, val in zip(axes[1].patches, [promo[False], promo[True]]):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                 f"{val:,.1f}", ha="center", fontsize=10, fontweight="bold")

# Oil scatter
axes[2].scatter(merged_oil["oil_price"], merged_oil["sales"]/1e6,
                alpha=0.3, color="#3266AD", s=10)
axes[2].set_title(f"Oil Price vs Sales (r={corr:.2f})", fontweight="bold")
axes[2].set_xlabel("Oil Price (USD)")
axes[2].set_ylabel("Total Sales (Millions)")

plt.suptitle("INSIGHT 1 — Key Demand Drivers", fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("insight1_demand_drivers.png", bbox_inches="tight")
plt.show()
print("  Saved: insight1_demand_drivers.png")


print("\n── INSIGHT 2: Replenishment Decisions ──")


test_pred = test.merge(submission, on="id", how="left")
store_reorder = test_pred.groupby("store_nbr")["sales"].sum().sort_values(ascending=False).reset_index()
store_reorder.columns = ["store_nbr", "predicted_demand"]

top5  = store_reorder.head(5)
bot5  = store_reorder.tail(5)
print("  Top 5 stores needing most stock replenishment:")
print(top5.to_string(index=False))
print("\n  Bottom 5 stores (lower demand, less urgent):")
print(bot5.to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 5))
colors = ["#D85A30" if i < 5 else "#3266AD" if i >= len(store_reorder)-5 else "#AECCE4"
          for i in range(len(store_reorder))]
ax.bar(store_reorder["store_nbr"].astype(str), store_reorder["predicted_demand"]/1e3,
       color=colors, edgecolor="white")
ax.set_title("Predicted Demand per Store — Aug 2017\n(Red = High Priority Replenishment | Blue = Low Priority)",
             fontweight="bold")
ax.set_xlabel("Store Number")
ax.set_ylabel("Predicted Sales (Thousands)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}K"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("insight2_replenishment.png")
plt.show()
print("  Saved: insight2_replenishment.png")

print("\n── INSIGHT 3: Perishable Risk Analysis ──")

PERISHABLES = ["PRODUCE", "MEATS", "DAIRY", "DELI", "SEAFOOD", "BREAD/BAKERY", "FROZEN FOODS"]

family_pred = test.merge(submission, on="id", how="left")
family_demand = family_pred.groupby("family")["sales"].sum().reset_index()
family_demand.columns = ["family", "predicted_demand"]
family_demand["is_perishable"] = family_demand["family"].isin(PERISHABLES)
family_demand = family_demand.sort_values("predicted_demand", ascending=True)

perishable_total = family_demand[family_demand["is_perishable"]]["predicted_demand"].sum()
total_demand     = family_demand["predicted_demand"].sum()
pct              = (perishable_total / total_demand) * 100
print(f"  Perishable share of total predicted demand: {pct:.1f}%")
print("  High-risk perishable families:")
print(family_demand[family_demand["is_perishable"]].sort_values("predicted_demand", ascending=False).to_string(index=False))

fig, ax = plt.subplots(figsize=(11, 7))
colors_p = ["#D85A30" if p else "#AECCE4" for p in family_demand["is_perishable"]]
ax.barh(family_demand["family"], family_demand["predicted_demand"]/1e3,
        color=colors_p, edgecolor="white")
ax.set_title("Predicted Demand by Product Family — Aug 2017\n(Red = Perishable / High Shrinkage Risk)",
             fontweight="bold")
ax.set_xlabel("Predicted Sales (Thousands)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}K"))
plt.tight_layout()
plt.savefig("insight3_perishable_risk.png")
plt.show()
print("  Saved: insight3_perishable_risk.png")


print("\n── INSIGHT 4: Store-Level Supply Strategy ──")

store_pred = test_pred.merge(stores, on="store_nbr", how="left")
cluster_demand = store_pred.groupby(["cluster", "type"])["sales"].sum().reset_index()
cluster_demand.columns = ["cluster", "store_type", "predicted_demand"]

cluster_summary = cluster_demand.groupby("cluster")["predicted_demand"].sum().sort_values(ascending=False).reset_index()
print("  Predicted demand by store cluster:")
print(cluster_summary.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))


axes[0].bar(cluster_summary["cluster"].astype(str),
            cluster_summary["predicted_demand"]/1e3,
            color=sns.color_palette("Blues_d", len(cluster_summary)),
            edgecolor="white")
axes[0].set_title("Predicted Demand by Store Cluster", fontweight="bold")
axes[0].set_xlabel("Cluster")
axes[0].set_ylabel("Predicted Sales (Thousands)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}K"))


type_demand = store_pred.groupby("type")["sales"].sum().sort_values(ascending=False).reset_index()
axes[1].bar(type_demand["type"], type_demand["sales"]/1e3,
            color=sns.color_palette("Oranges_d", len(type_demand)),
            edgecolor="white")
axes[1].set_title("Predicted Demand by Store Type", fontweight="bold")
axes[1].set_xlabel("Store Type")
axes[1].set_ylabel("Predicted Sales (Thousands)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}K"))

plt.suptitle("INSIGHT 4 — Store Cluster & Type Supply Strategy", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("insight4_store_strategy.png")
plt.show()
print("  Saved: insight4_store_strategy.png")


recommendations = {
    "POS → Warehouse Data Flow"         : "Real-time sales data from all 54 stores must feed into central warehouse daily",
    "Holiday-Aware Replenishment"       : f"Pre-stock {lift:.0f}% extra inventory before national holidays",
    "Promotion Planning"                : f"Allocate {promo_lift:.0f}% more stock for items flagged for promotion",
    "Perishable Alert System"           : f"Automated low-stock alerts for {len(PERISHABLES)} perishable categories",
    "Oil Price Monitoring"              : "Integrate macroeconomic feed — oil drop signals demand slowdown",
    "Cluster-Based Allocation"          : "High-demand clusters get priority warehouse dispatch",
    "Weekend Stock Buffer"              : "Saturday/Sunday demand peaks — pre-position stock by Friday",
}

print("\n  SAD System Design Recommendations:")
print("  " + "-"*60)
for key, val in recommendations.items():
    print(f"  ▸ {key}")
    print(f"    → {val}")
print("  " + "-"*60)


fig, ax = plt.subplots(figsize=(13, 6))
ax.axis("off")
rows = [[k, v] for k, v in recommendations.items()]
table = ax.table(
    cellText=rows,
    colLabels=["System Component", "Recommendation"],
    cellLoc="left",
    loc="center",
    colWidths=[0.32, 0.68],
)
table.auto_set_font_size(False)
table.set_fontsize(9.5)
table.scale(1, 2.2)
for (r, c), cell in table.get_celld().items():
    if r == 0:
        cell.set_facecolor("#3266AD")
        cell.set_text_props(color="white", fontweight="bold")
    elif r % 2 == 0:
        cell.set_facecolor("#EEF4FB")
    else:
        cell.set_facecolor("#FFFFFF")
    cell.set_edgecolor("#CCCCCC")
ax.set_title("INSIGHT 5 — ERP System Design Recommendations for SAD Report",
             fontweight="bold", fontsize=12, pad=20)
plt.tight_layout()
plt.savefig("insight5_system_recommendations.png", bbox_inches="tight")
plt.show()
