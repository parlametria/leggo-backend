from glob import glob
import pandas as pd

prop_data_files = '../../agora-digital/data/*/*prop*.csv'


def get_props(nonans=True):
    df = pd.concat([pd.read_csv(f) for f in glob(prop_data_files)], sort=False)
    if nonans:
        df = df.where((pd.notnull(df)), None)
    return df
