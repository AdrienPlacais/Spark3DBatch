#!/usr/bin/env python3
"""Define the class holding a SPARK3D configuration.

.. todo::
    Easily allow corona, videos.

"""
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from helper import fmt_array, printc


class SparkXML:
    """A class to handle the ``XML`` files from SPARK3D."""

    #: Links ``d_conf`` keys with :class:`.ElementTree` names
    _convert = {
        "Project": "project",
        "Model": "model",
        "Configurations": "confs",
        "EMConfigGroup": "em_conf",
        "MultipactorConfig": "discharge_conf",
    }

    def __init__(self, file: Path, keys: Sequence[str] | None = None) -> None:
        """Init object.

        Parameters
        ----------
        file :
            Path to the ``XML`` file.
        keys :
            Sequence of strings to indicate where the configuration should be
            in the ``XML`` file.

        """
        self.file = file
        self._tree = ET.parse(file)
        self._spark = self._tree.getroot()

        # Add a VideoMultipactorConfig key if needed, or change Multipactor to
        # corona
        self._keys = (
            tuple(keys)
            if keys is not None
            else (
                "Project",
                "Model",
                "Configurations",
                "EMConfigGroup",
                "MultipactorConfig",
            )
        )

    def get_config(self, **kwargs: int) -> ET.Element:
        """Return the configuration corresponding to the inputs.

        Parameters
        ----------
        *kwargs :
            Links configuration entries from ``self._keys`` to their value.

        Raises
        ------
        IOError
            ``*args`` matched no existing configuration. If it matched several,
            either the ``XML`` is wrong, either this code is wrong!

        Returns
        -------
        ET.Element
            Configuration in the form of an :class:`.ElementTree.Element`.

        """
        keys_xml = (self._convert[key] for key in self._keys)
        values_xml = (kwargs[key] for key in keys_xml)

        path = (f"{key}[{val}]" for key, val in zip(self._keys, values_xml))
        configuration = self._spark.findall("/".join(path))
        if len(configuration) != 1:
            raise OSError("More than one or no configuration was found.")
        return configuration[0]

    def edit(
        self,
        conf: ET.Element,
        save: bool = False,
        info: bool = True,
        **kwargs,
    ) -> None:
        """Modify the ``XML``.

        Parameters
        ----------
        conf :
            Configuration to be modified.
        save :
            To save the updated ``XML`` file. Previous file will be
            overwritten.
        info :
            To output some information on what was changed.
        **kwargs :
            Dict of values to change. Keys must be in ``<MultipactorConfig>``,
            eg ``'initialNumberElectrons'``. To modify inner keys, you must use
            the full path, eg ``'sweepPoints'`` will not work but
            ``'PowerSweep/sweepPoints'`` will. You must ensure that the type of
            the values matches what SPARK3D expects.

        """
        if info:
            printc(
                "xml_parser.edit info:",
                f"Modifying {conf.find('name').text}...",
            )
        for key, new_value in kwargs.items():
            s_old_value = conf.find(key).text

            s_new_val = str(new_value)
            conf.find(key).text = s_new_val
            if info:
                printc(
                    "xml_parser.edit info:",
                    f"Changed {key}: {s_old_value} to {s_new_val}",
                )

        if save:
            self._tree.write(self.file)
            printc("xml_parser.edit info:", f"xml saved in {self.file}")


if __name__ == "__main__":
    from importlib import resources

    file = (
        resources.files("spark3dbatch.data")
        / "Coax_filter_CST(M, C, Eigenmode).xml"
    )
    xml = SparkXML(file)

    # As already defined
    config = {
        "project": 1,
        "model": 1,
        "confs": 1,
        "em_conf": 1,
        "discharge_conf": 1,
        "video": -1,
    }
    xml_conf = xml.get_config(**config)

    power = fmt_array(np.linspace(1e-2, 1e2, 10))

    alter_conf = {
        "initialNumberElectrons": int(2e4),
        "pathRelativePrecision": 0.1,
        "PowerSweep/sweepPoints": power,
    }
    # Warning, save=True will overwrite previous ``XML``.
    xml.edit(xml_conf, save=False, **alter_conf)
