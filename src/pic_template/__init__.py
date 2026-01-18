"""PIC Template - Photonic Integrated Circuit design scaffold using gdsfactory."""

from __future__ import annotations
import gdsfactory as gf

# Activate the generic PDK on module import
# This is required before creating any gdsfactory components
gf.gpdk.PDK.activate()

__all__ = []
