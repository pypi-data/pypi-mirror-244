from dataclasses import dataclass

import numpy as np
import pandas as pd

@dataclass
class DGP_CUPED():
    """
    Data Generating Process: CUPED
    """
    mean: float = 20
    std: float = 5
    metric: str = 'y'
 
    def generate_data(
            self,
            units=100_000,
            periods=1,
            seed=2312):
        
        rng = np.random.default_rng(seed)
        dates = list(pd.date_range('2023-01-01', periods=periods, freq='D'))
        y0 = rng.normal(self.mean, self.std, units)
        y1 = y0 + rng.normal(0, 5, units)

        df = pd.DataFrame({
            'id': sorted([f'unit_{id}' for id in range(units)] * periods),
            'timeframe': dates * units,
            f'{self.metric}_pre': y0,
            f'{self.metric}': y1,
        })

        return df