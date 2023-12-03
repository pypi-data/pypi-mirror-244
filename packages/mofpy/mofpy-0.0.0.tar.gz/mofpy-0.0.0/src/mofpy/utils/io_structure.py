"""
`mofpy.utils.io_structure` submodule provides tools for reading MOF structures with/
without adsorbates.

TODO:

- Add support for reading structures in different formats (CIF, lammps.dump etc)
- Add support for writing MOF structures with/ without adsorbates in different formats.
"""

from typing import Union, Optional, List
from ase.io import read
from ase import Atoms


def read_structure(
    filename: str,
    file_format: Optional[str] = None,
    index: Union[int, str, slice] = ":",
) -> Atoms | List[Atoms]:
    """
    Read MOF structure from file.

    Parameters
    ----------
    filename : str
        Path to file containing MOF structure with/ without adsorbates.
    file_format : str | None
        Format of the file containing MOF structure with/ without adsorbates. Default: None
    index : int | str | slice
        Index of the structure to read from file. Default: ":"

    Returns
    -------
    Atoms | List[Atoms]
        MOF structure.
    """

    if not file_format:
        file_format = find_format(filename=filename)

    return read(filename=filename, index=index, format=file_format)


def find_format(filename: str) -> str:
    """
    Find format of the file containing MOF structure with/ without adsorbates.

    Parameters
    ----------
    filename : str
        Path to file containing MOF structure with/ without adsorbates.

    Returns
    -------
    file_format : str
        Format of the file containing MOF structure with/ without adsorbates.

    Raises
    ------
    ValueError
        Unsupported file format.
    """

    if filename.endswith(".traj"):
        file_format = "traj"
    elif filename.endswith(".xyz"):
        file_format = "xyz"
    elif filename.endswith(".xml"):
        file_format = "xml"
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    return file_format
