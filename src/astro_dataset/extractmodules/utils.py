import logging

import pandas as pd
from astropy.table import Table
from astroquery.mast import Observations

from astro_dataset.utils import table_to_pandas


def get_observations(proposal_id: int, query_filter: dict) -> Table:
    observations = Observations.query_criteria(proposal_id=proposal_id, **query_filter)
    logging.info(f"Number of Observations: {len(observations)}")
    return observations


def get_products(observations: Table) -> Table:
    products = Observations.get_product_list(observations)
    logging.info(f"Number of Products: {len(products)}")
    return products


def get_filtered_products(
    products: Table, observations: Table, product_filter: dict, n_channels: int = 3
) -> pd.DataFrame:
    filtered_products = apply_product_filter(products, product_filter)
    df_product_observation = merge_product_to_observations(filtered_products, observations)
    df_product_observation_filtered = apply_property_filter(df_product_observation, n_channels)
    return df_product_observation_filtered


def apply_product_filter(products: Table, product_filter: dict) -> Table:
    filtered_products = Observations.filter_products(products, **product_filter)
    logging.info(f"Number of Filtered Products: {len(filtered_products)}")
    return filtered_products


def merge_product_to_observations(products: Table, observations: Table) -> pd.DataFrame:
    products = table_to_pandas(products)
    observations = table_to_pandas(observations)
    df = pd.merge(products, observations, on="obs_id", how="inner")
    logging.info(f"Joind Products and Observations Shape: {df.shape}")
    return df


def apply_property_filter(df: pd.DataFrame, n_channels: int = 3) -> pd.DataFrame:
    df["obs_group"] = df["obs_id"].transform(lambda x: "".join(x.split("_")[:-1]))
    df["count"] = df.groupby(["target_name", "obs_group"])["filters"].transform("nunique")
    condition = df["count"] >= n_channels
    df = df.loc[condition]
    logging.info(f"N-Channels {n_channels} applied. Shape: {df.shape}")
    return df
