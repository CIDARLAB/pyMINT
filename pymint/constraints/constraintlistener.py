import logging
import re
from typing import List

from parchmint import Component

from pymint import MINTDevice
from pymint.antlrgen.mintListener import mintListener
from pymint.antlrgen.mintParser import mintParser
from pymint.constraints.arrayconstraint import ArrayConstraint
from pymint.constraints.mirrorconstraint import MirrorConstraint
from pymint.constraints.orientationconstraint import (
    ComponentOrientation,
    OrientationConstraint,
)
from pymint.constraints.orthogonalconstraint import OrthogonalConstraint
from pymint.constraints.positionconstraint import PositionConstraint


class ConstraintListener(mintListener):
    """Listener that is used to catch all the layout constratints
    from the MINT design

    """

    def __init__(self, device: MINTDevice):
        super().__init__()
        self.current_device = device

        # Temporary store for constrained components
        self._constrained_components = []

        # Temporary storage for mirrored components source
        self._mirror_constraint_driving_components = []

        # Temporary store for position constraints
        self._xpos: float = 0
        self._ypos: float = 0
        self._zpos: float = 0

        # Temporary store for array constraints
        self._vertical_spacing: float = 0
        self._horizontal_spacing: float = 0
        self._spacing: float = 0

        # Temporary store for relative orientatino constraints
        self._orientation = None

        # Global Relative Orientation Constraints
        self._global_relative_operations: List[OrientationConstraint] = []

        self._orthogonal_origin_candidates = []

    def enterPositionConstraintStat(
        self, ctx: mintParser.PositionConstraintStatContext
    ):
        self._xpos = 0
        self._ypos = 0
        self._zpos = 0

    def enterSetCoordinate(self, ctx: mintParser.SetCoordinateContext):
        coordinate_label = ctx.coordinate
        coordinate_value = int(ctx.INT().getText())  # type: ignore

        if coordinate_label == "X":
            self._xpos = coordinate_value
        elif coordinate_label == "Y":
            self._ypos = coordinate_value
        elif coordinate_label == "Z":
            self._zpos = coordinate_value
        else:
            raise Exception("Invalid coordinate label !")

    def exitPositionConstraintStat(self, ctx: mintParser.PositionConstraintStatContext):
        constraint = PositionConstraint(
            self._constrained_components[0], self._xpos, self._ypos, self._zpos
        )
        self.current_device.add_constraint(constraint)

    def enterHorizontalSpacingParam(
        self, ctx: mintParser.HorizontalSpacingParamContext
    ):
        self._horizontal_spacing = float(ctx.value().getText())  # type: ignore

    def enterVerticalSpacingParam(self, ctx: mintParser.VerticalSpacingParamContext):
        self._vertical_spacing = float(ctx.value().getText())  # type: ignore

    def enterSpacingParam(self, ctx: mintParser.SpacingParamContext):
        self._spacing = float(ctx.value().getText())  # type: ignore

    def exitGridStat(self, ctx: mintParser.GridStatContext):
        xdim = 1
        ydim = 1

        if ctx.xdim is not None:
            xdim = int(ctx.xdim.text)
        else:
            logging.warning(
                "No X Dimension found for GRID stat, setting dimension to 1"
            )
        if ctx.ydim is not None:
            ydim = int(ctx.ydim.text)
        else:
            logging.warning(
                "No Y Dimension found for GRID stat, setting dimension to 1"
            )
        # We need to add all the parameters here
        constraint = ArrayConstraint(
            self._constrained_components,
            xdim,
            ydim,
            self._horizontal_spacing,
            self._vertical_spacing,
        )

        self.current_device.add_constraint(constraint)

    def exitBankStat(self, ctx: mintParser.BankStatContext):
        dim = 1
        if ctx.dim is not None:  # type: ignore
            dim = int(ctx.dim.text)  # type: ignore
        else:
            logging.warning("No dimension found for BANK stat, setting dimension to 1")
        # We need to add all the parameters here
        constraint = ArrayConstraint(
            self._constrained_components, dim, horizontal_spacing=self._spacing
        )

        self.current_device.add_constraint(constraint)

    def exitBankDeclStat(self, ctx: mintParser.BankDeclStatContext):
        contraint = ArrayConstraint(
            self._constrained_components,
            len(self._constrained_components),
            horizontal_spacing=self._spacing,
        )

        self.current_device.add_constraint(contraint)

    def enterOrientation(self, ctx: mintParser.OrientationContext):
        if ctx.getText() == "H":
            self._orientation = ComponentOrientation.HORIZONTAL
        elif ctx.getText() == "V":
            self._orientation = ComponentOrientation.VERTICAL
        else:
            logging.error("Orientation that is not H or V found. Illegal Syntax")
            raise Exception("Orientation that is not H or V found. Illegal Syntax")

    def enterUfname(self, ctx: mintParser.UfnameContext):
        element_name = ctx.getText()
        component = None
        connection = None
        if self.current_device.device.component_exists(element_name):
            component = self.current_device.device.get_component(element_name)
        elif self.current_device.device.connection_exists(element_name):
            connection = self.current_device.device.get_connection(element_name)
        if component is not None:
            self._constrained_components.append(component)
        elif connection is not None:
            self._constrained_components.append(connection)
        else:
            # Check if theres a regex match against all the component names/id's
            component_names = [
                component.ID for component in self.current_device.device.components
            ]
            # Check if theres a regex match against all the connection id's in
            # component_name
            matches = map(
                lambda x: re.match(f"{element_name}_\\d+(_\\d+)?", x), component_names
            )
            for match in matches:
                if match is not None:
                    self._constrained_components.append(
                        self.current_device.device.get_component(match.group(0))
                    )
                    break
            else:
                print(
                    'Could not find component or connection with the ID "{}" in device'.format(
                        element_name
                    )
                )
                raise Exception(
                    f"Component {element_name} not found while processing constraint"
                )

    def enterLayerBlock(self, ctx: mintParser.LayerBlockContext):
        # Create a new relative orientation constraint for the whole layer
        self._global_relative_operations.append(OrientationConstraint())

    def enterFlowStat(self, ctx: mintParser.FlowStatContext):
        self._constrained_components = []
        self._orientation = None

    def exitFlowStat(self, ctx: mintParser.FlowStatContext):
        # Skip if there's no orientation set
        if self._orientation is None:
            return

        # In general check whats there and set the constraint for all the items
        # in the statement
        constraint = self._global_relative_operations[-1]
        for component in self._constrained_components:
            constraint.add_component_orientation_pair(component, self._orientation)

        self.current_device.add_constraint(constraint)

    def exitNodeStat(self, ctx: mintParser.NodeStatContext):
        # TODO: Expand on neighbours until we hit all the components on the node
        # periphery
        for component in self._constrained_components:
            if component is None:
                raise Exception(
                    "Could not apply Orthogonal Constraint, {} component not found !".format(
                        ctx.getText()
                    )
                )

            if self._check_if_component_constranied(component):
                continue

            self._orthogonal_origin_candidates.append(component)

    def exitChannelStat(self, ctx: mintParser.ChannelStatContext):
        # TODO - If length constraints exists, create them here
        pass

    def exitSpanStat(self, ctx: mintParser.SpanStatContext):
        for component in self._constrained_components:
            # Generate mirror constraints based on the in and out dimensins of span
            in_size = int(ctx.indim.text)  # type: ignore
            out_size = int(ctx.outdim.text)  # type: ignore

            if in_size > 1:
                self._mirror_constraint_driving_components.append(component)

            if out_size > 1:
                self._mirror_constraint_driving_components.append(component)

    def exitLayerBlock(self, ctx: mintParser.LayerBlockContext):
        # TODO: Fix how the mirror constraints are created
        MirrorConstraint.generate_constraints(
            self._mirror_constraint_driving_components, self.current_device
        )

    def exitNetlist(self, ctx: mintParser.NetlistContext):
        OrthogonalConstraint.generate_constraints(
            self._orthogonal_origin_candidates, self.current_device
        )

    # ------------ Helpers ----------

    def _check_if_component_constranied(self, component: Component) -> bool:
        found_flag = False
        for constraint in self.current_device.get_constraints():
            if isinstance(constraint, OrthogonalConstraint):
                found_flag = constraint.contains_component(component)

        return found_flag
