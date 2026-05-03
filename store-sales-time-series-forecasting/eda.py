import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "font.size": 11})

train       = pd.read_csv("store-sales-time-series-forecasting/train.csv",            parse_dates=["date"])
holidays    = pd.read_csv("store-sales-time-series-forecasting/holidays_events.csv",  parse_dates=["date"])
oil         = pd.read_csv("store-sales-time-series-forecasting/oil.csv",              parse_dates=["date"])
transactions= pd.read_csv("store-sales-time-series-forecasting/transactions.csv",     parse_dates=["date"])
stores      = pd.read_csv("store-sales-time-series-forecasting/stores.csv")

print(f"  train       : {train.shape}")
print(f"  holidays    : {holidays.shape}")
print(f"  oil         : {oil.shape}")
print(f"  transactions: {transactions.shape}")
print(f"  stores      : {stores.shape}")


train["year"]  = train["date"].dt.year
train["month"] = train["date"].dt.month
train["dow"]   = train["date"].dt.day_name()

holiday_dates = set(holidays["date"])
train["is_holiday"] = train["date"].isin(holiday_dates)


monthly = (train.groupby(train["date"].dt.to_period("M"))["sales"]
           .mean()
           .reset_index())
monthly["date"] = monthly["date"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(monthly["date"], monthly["sales"], color="#3266AD", linewidth=1.8)
ax.fill_between(monthly["date"], monthly["sales"], alpha=0.12, color="#3266AD")
ax.set_title("Monthly Average Sales Trend (2013–2017)", fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Avg Sales")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig("chart1_monthly_trend.png")
plt.show()


hol_avg = train.groupby("is_holiday")["sales"].mean().reset_index()
hol_avg["label"] = hol_avg["is_holiday"].map({False: "Normal Day", True: "Holiday"})

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(hol_avg["label"], hol_avg["sales"],
              color=["#888780","#D85A30"], width=0.45, edgecolor="white")
for bar, val in zip(bars, hol_avg["sales"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f"{val:,.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_title("Average Sales: Normal Days vs Holidays", fontweight="bold")
ax.set_ylabel("Avg Sales")
ax.set_ylim(0, hol_avg["sales"].max() * 1.2)
plt.tight_layout()
plt.savefig("chart2_holiday_impact.png")
plt.show()



hol_merged = holidays.merge(train, on="date", how="inner")
hol_type   = (hol_merged.groupby("type")["sales"]
              .mean()
              .sort_values(ascending=True)
              .reset_index())

fig, ax = plt.subplots(figsize=(8, 4))
colors = ["#B5D4F4","#85B7EB","#378ADD","#185FA5","#0C447C","#042C53"]
ax.barh(hol_type["type"], hol_type["sales"],
        color=colors[:len(hol_type)], edgecolor="white")
for i, (val, lbl) in enumerate(zip(hol_type["sales"], hol_type["type"])):
    ax.text(val + 2, i, f"{val:,.1f}", va="center", fontsize=9)
ax.set_title("Average Sales by Holiday Type", fontweight="bold")
ax.set_xlabel("Avg Sales")
plt.tight_layout()
plt.savefig("chart3_holiday_type.png")
plt.show()




promo = train.groupby("onpromotion")["sales"].mean().reset_index()
promo_cut = promo[promo["onpromotion"] <= 20]   # cap for readability

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(promo_cut["onpromotion"], promo_cut["sales"],
       color="#1D9E75", edgecolor="white")
ax.set_title("Promotion Lift: Avg Sales by Number of Items on Promotion", fontweight="bold")
ax.set_xlabel("Items on Promotion")
ax.set_ylabel("Avg Sales")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig("chart4_promotion_lift.png")
plt.show()



daily_sales = train.groupby("date")["sales"].sum().reset_index()
oil_clean   = oil.dropna(subset=["dcoilwtico"])
merged      = daily_sales.merge(oil_clean, on="date", how="inner")
corr        = merged["sales"].corr(merged["dcoilwtico"])

fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=False)

axes[0].plot(merged["date"], merged["sales"]/1e6,
             color="#3266AD", linewidth=1.2, label="Total Sales (M)")
axes[0].set_ylabel("Total Sales (Millions)")
axes[0].set_title(f"Oil Price vs Total Daily Sales  (Pearson r = {corr:.2f})", fontweight="bold")
axes[0].legend(loc="upper left")

axes[1].plot(merged["date"], merged["dcoilwtico"],
             color="#D85A30", linewidth=1.2, label="Oil Price (WTI)")
axes[1].set_ylabel("Oil Price (USD)")
axes[1].set_xlabel("Date")
axes[1].legend(loc="upper left")

plt.tight_layout()
plt.savefig("chart5_oil_vs_sales.png")
plt.show()



dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow_sales = (train.groupby("dow")["sales"]
             .mean()
             .reindex(dow_order)
             .reset_index())

fig, ax = plt.subplots(figsize=(8, 4))
bar_colors = ["#B5D4F4"]*5 + ["#185FA5","#0C447C"]
ax.bar(dow_sales["dow"], dow_sales["sales"],
       color=bar_colors, edgecolor="white")
for bar, val in zip(ax.patches, dow_sales["sales"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f"{val:,.0f}", ha="center", va="bottom", fontsize=9)
ax.set_title("Average Sales by Day of Week", fontweight="bold")
ax.set_xlabel("Day")
ax.set_ylabel("Avg Sales")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig("chart6_day_of_week.png")
plt.show()



family_sales = (train.groupby("family")["sales"]
                .sum()
                .sort_values(ascending=True)
                .tail(10)
                .reset_index())

fig, ax = plt.subplots(figsize=(10, 5))
colors_fam = sns.color_palette("Blues_d", len(family_sales))
ax.barh(family_sales["family"], family_sales["sales"]/1e6,
        color=colors_fam, edgecolor="white")
for i, val in enumerate(family_sales["sales"]/1e6):
    ax.text(val + 0.5, i, f"{val:,.1f}M", va="center", fontsize=9)
ax.set_title("Top 10 Product Families by Total Sales", fontweight="bold")
ax.set_xlabel("Total Sales (Millions)")
plt.tight_layout()
plt.savefig("chart7_product_families.png")
plt.show()


yearly = train.groupby("year")["sales"].mean().reset_index()

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(yearly["year"], yearly["sales"], marker="o",
        color="#534AB7", linewidth=2.5, markersize=8)
for _, row in yearly.iterrows():
    ax.text(row["year"], row["sales"] + 3, f"{row['sales']:,.1f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_title("Year-over-Year Average Sales Growth", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Avg Sales")
ax.set_xticks(yearly["year"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig("chart8_yearly_growth.png")
plt.show()
