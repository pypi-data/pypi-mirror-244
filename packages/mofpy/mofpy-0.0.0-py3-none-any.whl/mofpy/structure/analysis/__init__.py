"""
`mofpy.structure.analysis` submodule provides tools for analyzing MOF structures
with / without adsorbates.

Possible analyses include:

- Rings/ Windows distribution with corresponding ASE indices

- Pore size distribution using zeopp-lsmo (to be implemented)

- Adsorbate structure analysis if present (to be implemented)

- Metal center & Linker structure analysis in MOF (to be implemented)

- Topology analysis (to be implemented)

- Automatic identification of metal centers and linkers (to be implemented)
"""


class StructureGraph:
    """
    Graph representation of MOF structure with/ without adsorbates using the NetworkX package.
    An instance of class `StructureGraph` contains the following,

    Attributes
    ----------

    - TODO

    Methods
    -------

    - find rings

    - TODO
    """

    def __init__(self, ase_traj) -> None:
        pass


class StructureAnalyser:
    """
    Analyse MOF structure with/ without adsorbates.

    IDEA:
    This class will check for adosrbates in the structure and probably perform some heuristics
    using some MOF rules to check if the (sub-)structure is a valid MOF.
    """

    def __init__(self, ase_atoms) -> None:
        pass
