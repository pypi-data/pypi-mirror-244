from pathlib import Path
from unittest.mock import patch

import pytest

from flywheel_bids.flywheel_bids_app_toolkit import BIDSAppContext


@pytest.mark.parametrize(
    "archived_files, expected_bids_dir, expected_count",
    [
        (None, Path("/path/to/work_dir/bids"), 0),
        ("/a/tar.zip", Path("/a/tar"), 1),
        ("/another/archive", Path("/another/archive"), 0),
    ],
)
def test_BIDSAppContext(
    archived_files, expected_bids_dir, expected_count, extended_gear_context
):
    extended_gear_context.get_input_path.return_value = archived_files
    extended_gear_context.config.get.side_effect = (
        lambda key: extended_gear_context.config.get.side_effect_dict.get(key)
    )
    with patch(
        "flywheel_bids.flywheel_bids_app_toolkit.context.unzip_archive_files",
        return_value=expected_bids_dir,
    ) as unzip:
        # Create an instance of the BIDSAppContext class
        bids_app_context = BIDSAppContext(extended_gear_context)

    # Test the initialization of the BIDSAppContext object
    assert bids_app_context.destination_id == "output_destination_id"
    assert bids_app_context.analysis_level == "participant"
    assert bids_app_context.bids_app_binary == "something_bids_related"
    assert bids_app_context.bids_app_modalities == ["modality1", "modality2"]
    assert bids_app_context.bids_app_dry_run is True
    assert bids_app_context.bids_app_options.get("--extra_option")

    # Test the parsing of directory settings
    assert bids_app_context.output_dir == Path("/path/to/output_dir")
    assert bids_app_context.work_dir == Path("/path/to/work_dir")
    assert bids_app_context.bids_dir == expected_bids_dir

    # Test the parsing of run settings
    assert bids_app_context.save_intermediate_output is True
    assert bids_app_context.gear_dry_run is False
    assert bids_app_context.keep_output is False

    # Test the log file output location
    assert bids_app_context.output_log_file == bids_app_context.output_dir / Path(
        str(bids_app_context.bids_app_binary) + "_log.txt"
    )

    # Test the analysis output dir
    assert bids_app_context.analysis_output_dir == Path(
        bids_app_context.output_dir
    ) / Path(bids_app_context.destination_id)

    assert unzip.call_count == expected_count
