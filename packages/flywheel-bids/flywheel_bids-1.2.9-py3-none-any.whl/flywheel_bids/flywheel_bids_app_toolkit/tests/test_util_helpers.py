from pathlib import Path

import pytest

from flywheel_bids.flywheel_bids_app_toolkit.utils.helpers import (
    create_analysis_output_dir,
    make_dirs_and_files,
    split_extension,
)


def test_create_analysis_output_dir(tmp_path, extended_gear_context):
    test_path = Path(tmp_path) / "output"
    extended_gear_context.analysis_output_dir = test_path

    create_analysis_output_dir(extended_gear_context)

    assert test_path.exists()


@pytest.mark.parametrize(
    "filename, expected_name, expected_ext",
    [
        ("a.nii", "a", ".nii"),
        ("/try/path/b.nii.gz", "b", ".nii.gz"),
        ("c.dicom.zip.extra.suffixes", "c", ".dicom.zip.extra.suffixes"),
    ],
)
def test_split_extension(filename, expected_name, expected_ext):
    result_name, result_ext = split_extension(filename)
    assert result_name == expected_name
    assert result_ext == expected_ext


def test_make_dirs_and_files(tmp_path):
    files = ["path/to/file1.txt", "path/to/file2.txt", "path/to/dir/file3.txt"]
    paths = [tmp_path / file for file in files]

    make_dirs_and_files(paths)

    for path in paths:
        assert path.exists()


def test_make_dirs_and_files_with_path_objects(tmp_path):
    files = [
        Path("../../tests/path/to/file1.txt"),
        Path("../../tests/path/to/file2.txt"),
        Path("../../tests/path/to/dir/file3.txt"),
    ]

    make_dirs_and_files(files)

    for file in files:
        assert file.exists()
