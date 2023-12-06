import sys
from pathlib import Path
from typing import Optional

import click
from colorama import Fore

from tecton import version
from tecton.cli import printer
from tecton.cli import repo_utils
from tecton.cli.command import TectonGroup
from tecton.framework import repo_config as repo_config_module


# Templated starter repo config string. Simpler than bundling as a data asset.
_STARTER_REPO_CONFIG = """# This is the Tecton Repo Config. It's used to configure how Tecton collects and builds your
# feature definitions during `tecton plan/apply/test`.
#
# By default, the tecton CLI will use the repo configuration specified at TECTON_REPO_ROOT/repo.yaml, but you
# can use other files by using `tecton plan --config my_config.yaml`.

# Specify tecton object defaults. These defaults can be overridden on a per-object basis in your repo.
defaults:
  batch_feature_view:
    tecton_materialization_runtime: {current_version}
  stream_feature_view:
    tecton_materialization_runtime: {current_version}
  feature_table:
    tecton_materialization_runtime: {current_version}


# Example defaults with more fields set.
# defaults:
#   batch_feature_view:
#     tecton_materialization_runtime: {current_version}
#     online_store:
#       kind: DynamoConfig
#     offline_store:
#       kind: OfflineStoreConfig
#       staging_table_format:
#         kind: ParquetConfig
#     batch_compute:
#       kind: DatabricksClusterConfig
#       instance_type: m5.xlarge
#       instance_availability: on_demand
#       number_of_workers: 2
#       extra_pip_dependencies:
#         - "haversine==2.8.0"
#   stream_feature_view:
#     tecton_materialization_runtime: {current_version}
#     # TODO(you): batch_compute:
#     # TODO(you): stream_compute:
#     online_store:
#       kind: DynamoConfig
#     offline_store:
#       kind: OfflineStoreConfig
#       staging_table_format:
#         kind: ParquetConfig
#   feature_table:
#     tecton_materialization_runtime: {current_version}
#     # TODO(you): batch_compute:
#     online_store:
#       kind: DynamoConfig
#     offline_store:
#       kind: OfflineStoreConfig
#       staging_table_format:
#         kind: DeltaConfig
#   feature_service:
#     on_demand_environment: tecton-python-extended:0.2
"""


@click.command("repo-config", cls=TectonGroup)
def repo_config_group():
    """Create, inspect, or debug the repo configuration."""


@repo_config_group.command("show")
@click.argument(
    "config", required=False, default=None, type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True)
)
def show(config: Optional[Path]):
    """Print out the parsed repo config at CONFIG path. Defaults to the repo.yaml at the repo root."""
    if config is None:
        config = repo_utils.get_default_repo_config_path()

    printer.safe_print(f"Loading and printing repo config at path: {config}")
    repo_utils.load_repo_config(config)
    loaded_config = repo_config_module.get_repo_config()

    # TODO(jake): This prints out formatted JSON, which is decent. Using a library like "rich" or a custom function
    # to print out the model would be better.
    printer.safe_print(loaded_config.model_dump_json(exclude_unset=True, indent=4))


@repo_config_group.command("init")
@click.argument("config", required=False, default=None, type=click.Path(exists=False, path_type=Path, readable=True))
def init(config: Optional[Path]):
    """Write out a starter repo config to the provided CONFIG path. Default path is REPO_ROOT/repo.yaml."""
    if config is None:
        config = repo_utils.get_default_repo_config_path()

    if config.exists():
        printer.safe_print(Fore.RED + f"A file already exists at {config}. Aborting." + Fore.RESET)
        sys.exit(1)

    create_starter_repo_config(config_path=config)
    printer.safe_print(Fore.GREEN + f"Starter repo config written to {config}." + Fore.RESET)


def create_starter_repo_config(config_path: Path):
    """Create a starter repo config to config_path."""
    sdk_version = version.get_semantic_version() or "99.99.99"

    formatted_start_repo_config = _STARTER_REPO_CONFIG.format(current_version=sdk_version)

    with open(config_path, "w") as file:
        file.write(formatted_start_repo_config)
