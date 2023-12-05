"""Contains constants used throughout ADMET-AI."""
from importlib import resources


# Paths to data and models
with resources.path("admet_ai", "resources") as resources_dir:
    DEFAULT_ADMET_PATH = resources_dir / "data" / "admet.csv"
    # TODO: update DrugBank path once it's added to the repo
    # DEFAULT_DRUGBANK_PATH = None
    DEFAULT_DRUGBANK_PATH = resources_dir / "data" / "drugbank_approved.csv"
    DEFAULT_MODELS_DIR = resources_dir / "models"
