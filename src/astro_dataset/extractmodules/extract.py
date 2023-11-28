import logging

import hydra
import pandas as pd
import pyrootutils
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

from astro_dataset.extractmodules.utils import get_filtered_products, get_observations, get_products
from astro_dataset.utils import dataframe_to_csv

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

log = logging.getLogger(__name__)


@hydra.main(config_path=str(root / "conf"), config_name="extraction", version_base=None)
def main(cfg: DictConfig) -> None:
    cfg = cfg.extract
    log.info(OmegaConf.to_yaml(cfg, resolve=True))
    log.info(f"Extraction of {cfg.dataset_name} Started!")
    proposal_dataframe_list = []
    for proposal_id in tqdm(cfg.proposal_id_list):
        logging.info(f"Processing Proposal ID: {proposal_id}")
        try:
            observations = get_observations(proposal_id, cfg.query)
            products = get_products(observations)
            proposal_dataframe_list.append(
                get_filtered_products(products, observations, cfg.product)
            )
        except ZeroDivisionError as error:
            logging.critical(f"Proposal ID: {proposal_id}. Error: {error}")
    df_extract = pd.concat(proposal_dataframe_list, ignore_index=True)
    dataframe_to_csv(df_extract, cfg.csv_output_path)
    log.info(f"Final Shape of JWST DataFrame {df_extract.shape}")
    log.info(f"Extraction of {cfg.dataset_name} Finished!")


if __name__ == "__main__":
    main()
