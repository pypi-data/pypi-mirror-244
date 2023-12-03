# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 02.12.2023

  Purpose: Sets of classes for various date/time operations.
"""

from time import time

from jsktoolbox.attribtool import NoNewAttributes


class Timestamp(NoNewAttributes):
    """Timestamp class for geting current timestamp."""

    @classmethod
    @property
    def now(cls) -> int:
        """Return timestamp int."""
        return int(time())


# #[EOF]#######################################################################
