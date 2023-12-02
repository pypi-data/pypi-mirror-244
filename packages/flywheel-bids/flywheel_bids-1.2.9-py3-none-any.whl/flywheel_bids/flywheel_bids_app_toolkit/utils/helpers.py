import logging
from pathlib import Path
from typing import List, Union

log = logging.getLogger(__name__)


def create_analysis_output_dir(app_context):
    """
    Create analysis directory with the unique destination identifier.
    Args:
        app_context
    """
    # Create output directory
    log.info("Creating output directory %s", app_context.analysis_output_dir)
    Path(app_context.analysis_output_dir).mkdir(parents=True, exist_ok=True)


def make_dirs_and_files(files: Union[List[str], List[Path]]) -> None:
    """Create directories and touch files.

    Note: fw_gear_{BIDS_app}.utils.ry_run.py will use this method,
    but it is common enough to be part of a toolkit. One may also
    use it for testing setup.

    Args:
        files: paths to files to be created
    """
    for ff in files:
        if Path(ff).exists():
            log.debug("Exists: %s", str(ff))
        else:
            log.debug("Creating: %s", str(ff))
            dir_name = Path(ff).parents[0]
            Path(dir_name).mkdir(parents=True, exist_ok=True)
            Path(ff).touch(mode=0o777, exist_ok=True)


def split_extension(filename: str):
    """Remove flexible number of extensions.

    Imaging files and archives tend to have flexible numbers of extensions.
    This simple method deals with all extensions to return the most basic
    basename. e.g., /path/to/my/output/archive.tar.gz returns 'archive'

    Note: don't extend this method to all filenames, since 1.2.34.567.nii.gz
    or another UID-esque name would return problematically.
    :param filename (str): any filename with or without multiple extensions
    :return filename (str) Non-UID basename without any extensions
    :return ext (str) The combined suffixes from the original filename
    """
    ext = "." + ".".join(Path(filename).name.split(".")[1:])
    filename = str(Path(filename).stem.split(".")[0])
    if len(filename) < 4:
        log.warning(f"Is {filename} the correct filename without an extension?")
    return filename, ext
