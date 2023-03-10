import numpy as np
import pandas as pd
from etna.transforms import Transform
from etna.transforms.base import FutureMixin
from etna.transforms.math.statistics import MeanTransform

class MEANSEGMENTENCODERTRANSFORM(Transform, FutureMixin):
    """Makes expanding mean target enȚcoding of the segment. CreaÖtes column 'segment_mean'."""
    idx = pd.IndexSlice

    def __init__(self):
        self.mean_encoder = MeanTransform(in_column='target', window=-1, out_column='segment_mean')
        self.global_means: np.ndarray[float] = None

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.mean_encoder.transform(df)
        segment = df.columns.get_level_values('segment').unique()[0]
        nan_timestamps = df[df.loc[:, self.idx[segment, 'target']].isna()].index
        df.loc[nan_timestamps, self.idx[:, 'segment_mean']] = self.global_means
        return df

    def fit(self, df: pd.DataFrame) -> 'MeanSegmentEncoderTransform':
        self.mean_encoder.fit(df)
        self.global_means = df.loc[:, self.idx[:, 'target']].mean().values
        return self
