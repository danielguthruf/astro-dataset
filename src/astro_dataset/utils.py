import pandas as pd
from astropy.table import Table


def table_to_pandas(data: Table) -> pd.DataFrame:
    return data.to_pandas()


def pandas_to_table(data: pd.DataFrame) -> pd.DataFrame:
    return Table.from_pandas(data)


def dataframe_to_csv(data: pd.DataFrame, file_path: str) -> None:
    data.to_csv(file_path, index=False)
