"""Module to test commands.py"""
from unittest.mock import Mock

import pytest

from flywheel_bids.flywheel_bids_app_toolkit import BIDSAppContext, commands


class MockZipFile:
    def __init__(self):
        self.files = []

    def __enter__(self):
        return Mock()

    def __exit__(self, *args, **kwargs):
        return Mock()

    def __iter__(self):
        return iter(self.files)

    def write(self, fname):
        self.files.append(fname)


# - when there are and when there aren't bids_app_args
@pytest.mark.parametrize("bids_app_command", [None, "arg1 arg2 --my_arg", "--work-dir"])
def test_generate_command(bids_app_command, extended_gear_context):
    """Unit tests for generate_command"""
    extended_gear_context.config.get.side_effect_dict[
        "bids_app_command"
    ] = bids_app_command
    extended_gear_context.config.get.side_effect = (
        lambda key: extended_gear_context.config.get.side_effect_dict.get(key)
    )
    mock_app_context = BIDSAppContext(extended_gear_context)
    cmd = commands.generate_bids_command(mock_app_context)

    # Check that the returned cmd:
    # - is a list of strings:
    assert isinstance(cmd, list)
    assert all(isinstance(c, str) for c in cmd)
    # starts with the mandatory arguments:
    assert cmd[0:4] == [
        str(mock_app_context.bids_app_binary),
        str(mock_app_context.bids_dir),
        str(mock_app_context.analysis_output_dir),
        str(mock_app_context.analysis_level),
    ]

    # check that the bids_app_args are in the command:
    if bids_app_command:
        assert [arg in cmd for arg in bids_app_command.split()]


def test_clean_generated_command():
    cmd = ["--verbose=v", "--work-dir /path/to/work/dir", "--foo=bar fam"]
    cmd = commands.clean_generated_bids_command(cmd)
    assert cmd == ["-v", "--work-dir /path/to/work/dir", "--foo bar fam"]
