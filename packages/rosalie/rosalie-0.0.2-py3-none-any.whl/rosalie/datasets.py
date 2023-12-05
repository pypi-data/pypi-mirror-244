from dataclasses import dataclass


@dataclass
class DatasetInfo:
    name: str
    id_col: str
    metric: str
    pre_period: tuple = None
    post_period: tuple = None
    format: str = "cross_section"


customer_data = DatasetInfo(
    name="customer",
    id_col="id",
    metric="order_price",
    pre_period=("1 Jan 2023", "31 May 2023"),
    post_period=("1 Jun 2023", "31 Aug 2023"),
    format="cross_section",
)


datasets = []
