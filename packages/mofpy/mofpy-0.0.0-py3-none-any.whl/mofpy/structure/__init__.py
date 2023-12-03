"""
`mofpy.structure` module has two submodules:

- `analysis`

- `construct`
"""

from typing import Union, Optional, List
from ase import Atoms
from mofpy.utils.io_structure import read_structure


class BaseStructure:
    """
    Base class for all MOF structures with/ without adsorbates. This class contains the
    following attributes:

    - `self.ase_traj` : list[Atoms] | [ ]
    """

    def __init__(
        self,
        ase_atoms: Union[str, Atoms, List[Atoms]] = Atoms(),
        file_format: Optional[str] = None,
        index: Union[int, str, slice] = ":",
    ) -> None:
        """
        Initialize an instance of `class BaseStructure`.

        Parameters
        ----------
        ase_atoms : str | Atoms | List[Atoms]
            ASE structure / traj or path to file containing ASE structure / traj. Default: Atoms()

        file_format : str | None
            Format of the file containing MOF structure with/ without adsorbates. Default: None

        index : str | int | slice
            Index of the structure to read from file. Default: ":"

        Raises
        ------
        TypeError
            `ase_atoms` must be of type `str` or `Atoms` or `list[Atoms]`
        """
        if isinstance(ase_atoms, str):
            ase_atoms = read_structure(
                filename=ase_atoms, file_format=file_format, index=index
            )

        if isinstance(ase_atoms, Atoms):
            self.ase_traj = [ase_atoms] if ase_atoms else []
        elif isinstance(ase_atoms, list) and all(
            isinstance(x, Atoms) for x in ase_atoms
        ):
            self.ase_traj = ase_atoms
        else:
            raise TypeError(
                f"ase_atoms must be of type `str` or `Atoms` or `list[Atoms]`, \
                    not {type(ase_atoms)}"
            )
