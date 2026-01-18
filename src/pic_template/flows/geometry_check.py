"""Python-based geometry verification for photonic components.

This module provides programmatic checks for component geometry that complement
the KLayout DRC. These checks can be run as part of the test suite.
"""

from __future__ import annotations
from typing import Any
import gdsfactory as gf


class GeometryChecker:
    """Verify component geometry constraints programmatically."""
    
    def __init__(self, component: gf.Component):
        """Initialize checker with a component.
        
        Parameters
        ----------
        component : gf.Component
            Component to verify
        """
        self.component = component
        self.violations = []
    
    def check_min_feature_size(self, min_width: float = 0.45) -> bool:
        """Check minimum feature size in the component.
        
        Parameters
        ----------
        min_width : float
            Minimum allowed width in micrometers
        
        Returns
        -------
        bool
            True if all features are above minimum width
        """
        # This is a simplified check - full implementation would analyze
        # the actual polygon geometry
        bbox = self.component.bbox()
        if bbox.width() < min_width or bbox.height() < min_width:
            self.violations.append(
                f"Component has dimension < {min_width} µm"
            )
            return False
        return True
    
    def check_port_count(self, expected_count: int | None = None, 
                        allow_zero: bool = False) -> bool:
        """Check that component has expected number of ports.
        
        Parameters
        ----------
        expected_count : int | None
            Expected port count, or None to just check > 0
        allow_zero : bool
            If True, allow components with zero ports (e.g., top-level chips)
        
        Returns
        -------
        bool
            True if port count matches expectation
        """
        actual_count = len(self.component.ports)
        
        if expected_count is not None:
            if actual_count != expected_count:
                self.violations.append(
                    f"Expected {expected_count} ports, got {actual_count}"
                )
                return False
        elif actual_count == 0 and not allow_zero:
            self.violations.append("Component has no ports")
            return False
        
        return True
    
    def check_port_widths(self, min_width: float = 0.4, max_width: float = 2.0) -> bool:
        """Check that all ports have reasonable widths.
        
        Parameters
        ----------
        min_width : float
            Minimum port width in micrometers
        max_width : float
            Maximum port width in micrometers
        
        Returns
        -------
        bool
            True if all port widths are within range
        """
        all_valid = True
        
        for port in self.component.ports:
            if port.width < min_width:
                self.violations.append(
                    f"Port {port.name} width {port.width:.3f} < {min_width} µm"
                )
                all_valid = False
            elif port.width > max_width:
                self.violations.append(
                    f"Port {port.name} width {port.width:.3f} > {max_width} µm"
                )
                all_valid = False
        
        return all_valid
    
    def check_bounding_box(self, max_width: float | None = None, 
                          max_height: float | None = None) -> bool:
        """Check component bounding box constraints.
        
        Parameters
        ----------
        max_width : float | None
            Maximum allowed width in micrometers
        max_height : float | None
            Maximum allowed height in micrometers
        
        Returns
        -------
        bool
            True if bounding box is within constraints
        """
        bbox = self.component.bbox()
        width = bbox.width()
        height = bbox.height()
        all_valid = True
        
        if max_width is not None and width > max_width:
            self.violations.append(
                f"Component width {width:.2f} > max {max_width} µm"
            )
            all_valid = False
        
        if max_height is not None and height > max_height:
            self.violations.append(
                f"Component height {height:.2f} > max {max_height} µm"
            )
            all_valid = False
        
        return all_valid
    
    def check_port_orientations(self, allowed_angles: list[float] | None = None) -> bool:
        """Check that port orientations are valid.
        
        Parameters
        ----------
        allowed_angles : list[float] | None
            Allowed port angles, defaults to [0, 90, 180, 270]
        
        Returns
        -------
        bool
            True if all port orientations are valid
        """
        if allowed_angles is None:
            allowed_angles = [0, 90, 180, 270]
        
        all_valid = True
        
        for port in self.component.ports:
            if port.orientation not in allowed_angles:
                self.violations.append(
                    f"Port {port.name} has invalid orientation {port.orientation}°"
                )
                all_valid = False
        
        return all_valid
    
    def run_all_checks(self, is_top_level: bool = False) -> dict[str, Any]:
        """Run all geometry checks.
        
        Parameters
        ----------
        is_top_level : bool
            If True, relax checks for top-level components (e.g., allow no ports)
        
        Returns
        -------
        dict
            Dictionary with check results and violations
        """
        self.violations = []
        
        results = {
            "component_name": self.component.name,
            "checks": {
                "min_feature_size": self.check_min_feature_size(),
                "port_count": self.check_port_count(allow_zero=is_top_level),
                "port_widths": self.check_port_widths(),
                "port_orientations": self.check_port_orientations(),
            },
            "violations": self.violations,
            "passed": len(self.violations) == 0
        }
        
        return results


def verify_component(component: gf.Component) -> dict[str, Any]:
    """Convenience function to verify a component.
    
    Parameters
    ----------
    component : gf.Component
        Component to verify
    
    Returns
    -------
    dict
        Verification results
    """
    checker = GeometryChecker(component)
    return checker.run_all_checks()
