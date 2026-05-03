import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from sklearn.metrics import mean_squared_log_error
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb


train       = pd.read_csv("store-sales-time-series-forecasting/train.csv",            parse_dates=["date"])
test        = pd.read_csv("store-sales-time-series-forecasting/test.csv",             parse_dates=["date"])
holidays    = pd.read_csv("store-sales-time-series-forecasting/holidays_events.csv",  parse_dates=["date"])
oil         = pd.read_csv("store-sales-time-series-forecasting/oil.csv",              parse_dates=["date"])
transactions= pd.read_csv("store-sales-time-series-forecasting/transactions.csv",     parse_dates=["date"])
stores      = pd.read_csv("store-sales-time-series-forecasting/stores.csv")



oil = oil.set_index("date").resample("D").first().ffill().reset_index()
oil.rename(columns={"dcoilwtico": "oil_price"}, inplace=True)


holidays_national = holidays[
    (holidays["type"].isin(["Holiday", "Transfer"])) &
    (holidays["locale"] == "National")
][["date"]].drop_duplicates()
holidays_national["is_national_holiday"] = 1

holidays_local = holidays[
    (holidays["type"].isin(["Holiday", "Transfer"])) &
    (holidays["locale"] != "National")
][["date"]].drop_duplicates()
holidays_local["is_local_holiday"] = 1

events = holidays[holidays["type"] == "Event"][["date"]].drop_duplicates()
events["is_event"] = 1


train = train.merge(stores, on="store_nbr", how="left")
test  = test.merge(stores, on="store_nbr", how="left")


train["is_train"] = 1
test["is_train"]  = 0
test["sales"]     = np.nan

combined = pd.concat([train, test], sort=False).reset_index(drop=True)


combined = combined.merge(oil, on="date", how="left")
combined = combined.merge(transactions, on=["date","store_nbr"], how="left")
combined = combined.merge(holidays_national, on="date", how="left")
combined = combined.merge(holidays_local, on="date", how="left")
combined = combined.merge(events, on="date", how="left")

combined["is_national_holiday"] = combined["is_national_holiday"].fillna(0)
combined["is_local_holiday"]    = combined["is_local_holiday"].fillna(0)
combined["is_event"]            = combined["is_event"].fillna(0)


print("Engineering features...")

combined["year"]        = combined["date"].dt.year
combined["month"]       = combined["date"].dt.month
combined["day"]         = combined["date"].dt.day
combined["dayofweek"]   = combined["date"].dt.dayofweek
combined["weekofyear"]  = combined["date"].dt.isocalendar().week.astype(int)
combined["is_weekend"]  = (combined["dayofweek"] >= 5).astype(int)
combined["quarter"]     = combined["date"].dt.quarter

le = LabelEncoder()
for col in ["family", "city", "state", "type"]:
    combined[col] = le.fit_transform(combined[col].astype(str))


combined = combined.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)

for lag in [7, 14, 28]:
    combined[f"sales_lag_{lag}"] = (
        combined.groupby(["store_nbr", "family"])["sales"]
        .shift(lag)
    )

for window in [7, 14]:
    combined[f"sales_roll_mean_{window}"] = (
        combined.groupby(["store_nbr", "family"])["sales"]
        .shift(7)
        .rolling(window)
        .mean()
        .values
    )


train_df = combined[combined["is_train"] == 1].copy()
test_df  = combined[combined["is_train"] == 0].copy()


cutoff = train_df["date"].max() - pd.Timedelta(days=28)
val_df  = train_df[train_df["date"] > cutoff].copy()
tr_df   = train_df[train_df["date"] <= cutoff].copy()

tr_df["sales"]  = tr_df["sales"].clip(lower=0)
val_df["sales"] = val_df["sales"].clip(lower=0)

FEATURES = [
    "store_nbr", "family", "onpromotion",
    "year", "month", "day", "dayofweek", "weekofyear",
    "is_weekend", "quarter",
    "city", "state", "type", "cluster",
    "oil_price", "transactions",
    "is_national_holiday", "is_local_holiday", "is_event",
    "sales_lag_7", "sales_lag_14", "sales_lag_28",
    "sales_roll_mean_7", "sales_roll_mean_14",
]

TARGET = "sales"

X_tr  = tr_df[FEATURES]
y_tr  = tr_df[TARGET]
X_val = val_df[FEATURES]
y_val = val_df[TARGET]
X_test= test_df[FEATURES]


print("Training LightGBM model...")

params = {
    "objective"       : "regression_l1",
    "metric"          : "rmse",
    "learning_rate"   : 0.05,
    "num_leaves"      : 127,
    "min_child_samples": 20,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq"    : 5,
    "verbose"         : -1,
}

dtrain = lgb.Dataset(X_tr,  label=np.log1p(y_tr))
dval   = lgb.Dataset(X_val, label=np.log1p(y_val), reference=dtrain)

callbacks = [
    lgb.early_stopping(stopping_rounds=50, verbose=True),
    lgb.log_evaluation(period=100),
]

model = lgb.train(
    params,
    dtrain,
    num_boost_round=1000,
    valid_sets=[dtrain, dval],
    valid_names=["train", "valid"],
    callbacks=callbacks,
)

val_preds = np.expm1(model.predict(X_val))
val_preds = np.clip(val_preds, 0, None)

y_val_clipped = y_val.clip(lower=0)
rmsle = np.sqrt(mean_squared_log_error(y_val_clipped, val_preds))
print(f"\n✅ Validation RMSLE: {rmsle:.4f}")

importance = pd.DataFrame({
    "feature"   : FEATURES,
    "importance": model.feature_importance(importance_type="gain"),
}).sort_values("importance", ascending=True).tail(15)

plt.figure(figsize=(10, 6))
plt.barh(importance["feature"], importance["importance"],
         color=sns.color_palette("Blues_d", len(importance)))
plt.title("LightGBM Feature Importance (Gain) — Top 15", fontweight="bold")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("chart9_feature_importance.png")
plt.show()
print("Saved: chart9_feature_importance.png")


val_df = val_df.copy()
val_df["predicted"] = val_preds

sample = (val_df.groupby("date")[["sales","predicted"]]
          .mean()
          .reset_index()
          .sort_values("date"))

plt.figure(figsize=(14, 4))
plt.plot(sample["date"], sample["sales"],     label="Actual",    color="#3266AD", linewidth=1.8)
plt.plot(sample["date"], sample["predicted"], label="Predicted", color="#D85A30", linewidth=1.8, linestyle="--")
plt.title("Actual vs Predicted Sales — Validation Period (Last 28 Days)", fontweight="bold")
plt.xlabel("Date")
plt.ylabel("Avg Sales")
plt.legend()
plt.tight_layout()
plt.savefig("chart10_actual_vs_predicted.png")
plt.show()

test_preds = np.expm1(model.predict(X_test))
test_preds = np.clip(test_preds, 0, None)


submission = test_df[["id"]].copy()
submission["sales"] = test_preds
submission.to_csv("submission.csv", index=False)
print("✅ submission.csv saved!")
print(submission.head(10).to_string())

print("\n✅ Task 2 Complete — Model trained, validated, and predictions saved.")