"""Tools to help zip, unzip, and process HTML, result, or archived files."""
import datetime
import fnmatch
import logging
import os
from pathlib import Path
from typing import List, Union
from zipfile import ZIP_DEFLATED, ZipFile

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils.zip_tools import zip_output

from .utils.helpers import split_extension

log = logging.getLogger(__name__)


def walk_tree_to_exclude(root_dir: Path, inclusion_list: List):
    """
    Walks a tree and excludes files or directories not specified in the inclusion list.
    Returns a list of excluded files and folders.

    GTK requires an exclusionary list for `zip_output`. Thus, this method
    combs the tree and reports which files to pass to `zip_output` for exclusion.

    Args:
        root_dir (Path): directory to walk to locate files to exclude
        inclusion_list (List): Files to keep for zipping. If a file is
        encountered during the walk and not in this list, it will be returned
        as one of the files to exclude, when GTK zips the contents of the root_dir.
    """
    excluded_items = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter and process the filenames
        for filename in filenames:
            if not any(
                fnmatch.fnmatch(filename, pattern) for pattern in inclusion_list
            ):
                file_path = os.path.join(dirpath, filename)
                excluded_items.append(file_path)

    return excluded_items


def prepend_index_filename(orig_filename: Union[Path, str]):
    """
    Add the analysis date and time to the beginning of the filename.

    Sometimes, there is an index.html file in the analysis' output.
     This file will be need to be identified, temporarily renamed,
     and then restored to the original location. (Other htmls are
     temporarily named "index.html" prior to being zipped, so this
     method helps avoid files being overwritten.)
    :param orig_filename: full path to the file that needs to be
            temporarily renamed.
    :return
        updated_filename: new location/name of the file, so that the file
        can be returned to its original location after the other results are
        marked and zipped.
    """
    now = datetime.datetime.now()
    updated_filename = Path(
        Path(orig_filename).parents[0],
        now.strftime("%Y-%m-%d_%H") + "_" + Path(orig_filename).name,
    )
    os.rename(orig_filename, updated_filename)
    return updated_filename


def unzip_archive_files(gear_context: GearToolkitContext, archive_key: str):
    """Unzip archived files (e.g., FreeSurfer) from previous runs.

    This method is called when the BIDSAppContext object is instantiated.

    Args:
        gear_context (GearToolkitContext): Details about the gear run
        archive_key (str): Key to retrieve/set from app_options
    Returns:
        unzipped_dir (Path): newly unzipped directory
    """
    zipped_dir = gear_context.get_input_path(archive_key)
    # Remove the extension, so the location as an unzipped dir can be passed to the BIDSAppContext
    unzipped_dir = Path(zipped_dir).with_suffix("")
    # Extract the dir
    with ZipFile(zipped_dir, "r") as zip_ref:
        zip_ref.extractall(unzipped_dir)
    return unzipped_dir


def zip_derivatives(app_context, alt_derivatives: List[str] = None):
    """
    Zip any and all derivative folders created by the BIDS App.

    Args:
        app_context (BIDSAppContext): Details about the gear setup and BIDS options
        alt_derivatives (List): Any other directories to look through for
            compression. e.g., qsirecon in addition to qsiprep
    """
    derivatives = [app_context.bids_app_binary]
    derivatives.extend(alt_derivatives)
    for derivative in derivatives:
        derivative_dir = Path(app_context.analysis_output_dir) / derivative

        if derivative_dir.exists():
            zip_file_name = (
                app_context.output_dir
                / f"{app_context.bids_app_binary}_{app_context.destination_id}_{derivative}.zip"
            )
            zip_output(
                str(app_context.analysis_output_dir),
                derivative,
                str(zip_file_name),
                dry_run=False,
                exclude_files=None,
            )
            zip_htmls(
                app_context.output_dir, app_context.destination_id, derivative_dir
            )


def zip_htmls(
    output_dir: Union[Path, str], destination_id: str, html_path: Union[Path, str]
):
    """Zip all .html files at the given path, so they can be displayed
    on the Flywheel platform.

    Each html file must be converted into an archive individually:
      rename each to be "index.html", then create a zip archive from it.
      # BMS - is "index.html" a requirement of the platform to be viewable?
    Args:
        output_dir (Path): Location for the zip to end up.
        destination_id (str): Flywheel ID
        html_path (Path): Location to search for htmls to zip.
    """
    log.info("Creating viewable archives for all html files")

    if Path(html_path).exists():
        html_files = list(Path(html_path).rglob("*.html"))
        if html_files:
            log.info(f"Zipping files at {str(html_path)}")
            for f in html_files:
                zip_it_zip_it_good(output_dir, destination_id, f)
        else:
            log.warning("No *.html files at " + str(html_path))
    else:
        log.error("Path NOT found: " + str(html_path))


def zip_it_zip_it_good(
    output_dir: Union[Path, str], destination_id: str, unzipped_file: Union[Path, str]
):
    """Compress html file into an appropriately named archive file *.html.zip
    files are automatically shown in another tab in the browser. These are
    saved at the top level of the output folder.
    Args:
        output_dir (os.PathLike): default is /flywheel/v0
        destination_id (str): container identifier
        unzipped_file (os.PathLike): expects full path; does not assume directory
        location. Probably ends in "index.html"
    """

    basename, ext = split_extension(str(unzipped_file))

    dest_zip = os.path.join(output_dir, basename + "_" + destination_id + ext + ".zip")

    log.info('Creating viewable archive "' + dest_zip + '"')

    with ZipFile(dest_zip, "w", ZIP_DEFLATED) as outzip:
        outzip.write(unzipped_file)
