"""basecomposite.py
A basic composite object which is composed of component objects.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Mapping
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class BaseComposite(BaseObject):
    """A basic composite object which is composed of component objects.

    Class Attributes:
        default_component_types: The default component classes and their keyword arguments for this object.

    Attributes:
        components: The components of this object.

    Args:
        component_kwargs: Keyword arguments for creating the components.
        component_types: Component classes and their keyword arguments to instantiate.
        components: Components to add.
        **kwargs: Keyword arguments for inheritance.
    """

    default_component_types: dict[str, tuple[type, dict[str, Any]]] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
        **kwargs: Any
    ) -> None:
        # New Attributes #
        self.components: dict[str, Any] = {}

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
                **kwargs,
            )

    # Pickling
    def __setstate__(self, state: Mapping[str, Any]) -> None:
        """Builds this object based on a dictionary of corresponding attributes.

        Args:
            state: The attributes to build this object from.
        """
        self.__dict__.update(state)
        for component in self.components.values():
            component.composite = self

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> None:
        """Constructs this object.

        Args:
            component_kwargs: Keyword arguments for creating the components.
            component_types: Component classes and their keyword arguments to instantiate.
            components: Components to add.
            **kwargs: Keyword arguments for inheritance.
        """
        self.construct_components(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
        )

        super().construct(**kwargs)

    def construct_components(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
    ) -> None:
        """Constructs or adds components.

        Args:
            component_kwargs: The keyword arguments for creating the components.
            component_types: Component class and their keyword arguments to instantiate.
            components: Components to add.
        """
        temp_types = self.default_component_types | {} if component_types is None else component_types
        new_kwargs = {} if component_kwargs is None else component_kwargs
        default_components = {n: c(composite=self, **(k | new_kwargs.get(n, {}))) for n, (c, k) in temp_types.items()}
        self.components.update(default_components | self.components | {} if components is None else components)
