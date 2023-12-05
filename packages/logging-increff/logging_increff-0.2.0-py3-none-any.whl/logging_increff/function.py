import os
import logging


def create_folder(path):
    if not os.path.exists(str(path)):
        os.makedirs(str(path))


def setup_logger(env="NA", job_id="NA"):
    create_folder(f"/tmp/caas_{job_id}")
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s %(levelname)s %(pathname)s:%(lineno)s [env="
        + env
        + "][job_id="
        + job_id
        + "] [%(message)s]",
        datefmt="%d-%b-%y %H:%M:%S",
        force=True,
        handlers=[
            logging.FileHandler(f"/tmp/caas_{job_id}/runner.log"),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger("azure").setLevel(logging.WARNING)
