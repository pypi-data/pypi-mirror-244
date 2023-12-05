SELECT
  id,
  timeframe,
  menu_2_basket_cvr,
  avg_food_price
FROM
  `just-data-warehouse.experimentation.causal_jet_metrics_resto_je_uk`
WHERE
  frequency = "daily"
  AND timeframe between "2023-01-01" AND "2023-06-30"
