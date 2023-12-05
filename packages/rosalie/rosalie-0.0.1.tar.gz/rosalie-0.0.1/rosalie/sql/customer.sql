-- Using Ireland data for customer data because it's familiar
-- from IE OneWeb rollout

SELECT
  v.visit_key,
  v.user.consolidated_user_id AS user_id,
  v.visit_date AS timeframe,
  v.app AS platform,
  o.order_price,
FROM
  `just-data-warehouse.analytics.visits_ie_*` AS v
LEFT JOIN
  UNNEST(orders) AS o
WHERE
  visit_date BETWEEN "2023-01-01" AND "2023-08-31"
  AND totals.pageviews > 0
  AND totals.pageviews IS NOT NULL