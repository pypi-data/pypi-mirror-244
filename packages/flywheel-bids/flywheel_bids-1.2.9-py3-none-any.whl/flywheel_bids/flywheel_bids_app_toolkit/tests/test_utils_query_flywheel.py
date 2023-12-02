import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from importlib_resources import files

from flywheel_bids.flywheel_bids_app_toolkit.utils.query_flywheel import (
    copy_bidsignore_file,
    fix_dataset_description,
    get_fw_details,
)

BIDS_PATH = files("tests.assets").joinpath("dataset")


@pytest.mark.parametrize(
    "bidsignore_condition, copied_file",
    [("use", ".bidsignore"), ("skip", "found.bidsignore")],
)
def test_copy_bidsignore_file(bidsignore_condition, copied_file, tmp_path):
    # Set up dummy file
    input_dir = Path(tmp_path) / "input"
    input_dir.mkdir(parents=True)
    bidsignore = None
    if bidsignore_condition == "use":
        bidsignore = input_dir / copied_file
        bidsignore.touch()
    else:
        tmp_file = input_dir / copied_file
        tmp_file.touch()

    copy_bidsignore_file(BIDS_PATH, bidsignore, input_dir)
    expected_result = Path(BIDS_PATH) / ".bidsignore"

    assert expected_result.exists()

    # Clean-up
    os.remove(expected_result)


@pytest.mark.parametrize(
    "funding_entry, expected_funding, expected_info_log_calls",
    [
        ("str", ["str"], 1),
        (None, [None], 1),
        (["Grant 1", "Grant 2"], ["Grant 1", "Grant 2"], 0),
    ],
)
def test_fix_dataset_description(
    funding_entry, expected_funding, expected_info_log_calls, tmp_path, caplog
):
    caplog.set_level("INFO")
    mock_dd = tmp_path / "dataset_description.json"
    # Create a temporary dataset_description.json file with incorrect "Funding" field
    dataset_description = {
        "Name": "My Dataset",
    }
    if funding_entry:
        dataset_description["Funding"] = funding_entry

    mock_dd.write_text(json.dumps(dataset_description))

    # Call the function to fix the dataset_description.json file
    fix_dataset_description(tmp_path)

    # Verify that the file has been updated correctly
    updated_data = json.loads(mock_dd.read_text())
    assert isinstance(updated_data["Funding"], list)
    assert updated_data["Funding"] == expected_funding
    assert expected_info_log_calls == len(
        [rec for rec in caplog.records if rec.levelname == "INFO"]
    )


def test_get_fw_details(extended_gear_context):
    extended_gear_context.manifest.get.side_effect = lambda key: {
        "custom": {"gear-builder": {"image": "flywheel/bids-qsiprep:0.0.1_0.15.1"}}
    }.get(key)
    extended_gear_context.client.get.side_effect = MagicMock()
    destination, gear_builder_info, container = get_fw_details(extended_gear_context)
    assert isinstance(destination, MagicMock)
    assert isinstance(gear_builder_info, dict)
    assert isinstance(container, str)
