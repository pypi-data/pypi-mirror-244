SELECT
  timeframe,
  restaurant_city as id,
  orders,
  avg_food_price,
  revenue,
  revenue_per_order
FROM
  `just-data-warehouse.experimentation.causal_jet_metrics_city_je_uk`
WHERE
  frequency = "daily"
  AND timeframe BETWEEN "2023-01-01" AND "2023-06-30"