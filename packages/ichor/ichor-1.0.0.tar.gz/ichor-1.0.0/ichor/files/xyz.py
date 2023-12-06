from pathlib import Path
from typing import Union

class XYZ:
    """A class which wraps around a .xyz file .

    :param path: The path to an .xyz file
    """

    def __init__(self, path: Union[Path, str]):
        self.path = path

    def _read_file(self):
        """Read a .xyz file and constructs the `self.atoms` attribute which is an instance of `Atoms`"""
        with open(self.path, "r") as f:
            natoms = int(next(f))
            _ = next(f)  # blank line
            read_atoms = []
            for _ in range(natoms):
                record = next(f).split()
                read_atoms.add(
                        record[0],
                        float(record[1]),
                        float(record[2]),
                        float(record[3]),
                    )
        self.atoms = self.atoms or read_atoms

    def _write_file(self, path: Path):
        """Write a .xyz to a given path. If no path is given,
        it will write it to the path given when the XYZ instance was constructed.

        :param path: An optional path to which to write the .xyz file
        """
        fmtstr = "12.8f"
        with open(path, "w") as f:
            f.write(f"{len(self.atoms)}\n")
            f.write("\n")
            for atom in self.atoms:
                f.write(
                    f"{atom.type} {atom.x:{fmtstr}} {atom.y:{fmtstr}} {atom.z:{fmtstr}}\n"
                )
