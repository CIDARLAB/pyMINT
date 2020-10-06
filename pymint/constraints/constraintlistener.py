from typing import List
import logging
from pymint.mintcomponent import MINTComponent
from pymint.constraints.orthogonalconstraint import OrthogonalConstraint
from pymint.constraints.arrayconstraint import ArrayConstraint
from pymint.constraints.positionconstraint import PositionConstraint
from pymint.constraints.constraint import LayoutConstraint
from pymint.antlr.mintListener import mintListener
from pymint.mintdevice import MINTDevice
from pymint.antlr.mintParser import mintParser
from pymint.constraints.orientationconstraint import ComponentOrientation, OrientationConstraint


class ConstraintListener(mintListener):

    def __init__(self, device: MINTDevice):
        super().__init__()
        self.current_device = device
        self.__current_constraints = []

        #Temporary store for constrained components
        self._constrained_components = []

        #Temporary store for position constraints
        self._xpos = None
        self._ypos = None
        self._zpos = None

        #Temporary store for array constraints
        self._vertical_spacing = None
        self._horizontal_spacing = None
        self._spacing = None

        #Temporary store for relative orientatino constraints
        self._orientation = None

        #Global Relative Orientation Constraints
        self._global_relative_operations = []
    
    def enterSetCoordinate(self, ctx: mintParser.SetCoordinateContext):
        coordinate_label = ctx.coordinate
        coordinate_value = float(ctx.INT().getText())
        
        if coordinate_label == 'X':
            self._xpos = coordinate_value
        elif coordinate_label == 'Y':
            self._ypos = coordinate_value
        else:
            self._zpos = coordinate_value

    def exitPositionConstraintStat(self, ctx: mintParser.PositionConstraintStatContext):
        constraint = PositionConstraint(self._constrained_components[0], self._xpos, self._ypos, self._zpos )
        self.current_device.addConstraint(constraint)

    def enterHorizontalSpacingParam(self, ctx: mintParser.HorizontalSpacingParamContext):
        self._horizontal_spacing = float(ctx.value().getText())

    def enterVerticalSpacingParam(self, ctx: mintParser.VerticalSpacingParamContext):
        self._vertical_spacing = float(ctx.value().getText())

    def enterSpacingParam(self, ctx: mintParser.SpacingParamContext):
        self._spacing = float(ctx.value().getText())

    def exitGridStat(self, ctx: mintParser.GridStatContext):
        xdim = 1
        ydim = 1

        if ctx.xdim is not None:
            xdim = int(ctx.xdim.text)
        else:
            logging.warning("No X Dimension found for GRID stat, setting dimension to 1")
        if ctx.ydim is not None:
            ydim = int(ctx.ydim.text)
        else:
            logging.warning("No Y Dimension found for GRID stat, setting dimension to 1")
        #We need to add all the parameters here
        constraint = ArrayConstraint(self._constrained_components, xdim, ydim, self._horizontal_spacing, self._vertical_spacing)

        self.current_device.addConstraint(constraint)

    def exitBankStat(self, ctx: mintParser.BankStatContext):
        dim = 1
        if ctx.xdim is not None:
            dim = int(ctx.dim.text)
        else:
            logging.warning("No dimension found for BANK stat, setting dimension to 1")
        #We need to add all the parameters here
        constraint = ArrayConstraint(self._constrained_components, dim, horizontal_spacing=self._spacing)

        self.current_device.addConstraint(constraint)

    def enterOrientation(self, ctx: mintParser.OrientationContext):
        if ctx.getText() == 'H':
            self._orientation = ComponentOrientation.HORIZONTAL
        elif ctx.getText() == 'V':
            self._orientation = ComponentOrientation.VERTICAL
        else:
            logging.error("Orientation that is not H or V found. Illegal Syntax")
            raise Exception("Orientation that is not H or V found. Illegal Syntax")


    def enterUfname(self, ctx: mintParser.UfnameContext):
        component_name = ctx.getText()
        component = self.current_device.getComponent(component_name)
        if component is not None:
            # raise Exception("Could not find component in device : {}".format(component_name))
            self._constrained_components.append(component)

    
    def enterLayerBlock(self, ctx: mintParser.LayerBlockContext):
        #Create a new relative orientation constraint for the whole layer
        self._global_relative_operations.append(OrientationConstraint())

    def enterFlowStat(self, ctx: mintParser.FlowStatContext):
        self._constrained_components = []
        self._orientation = None
   
    def exitFlowStat(self, ctx: mintParser.FlowStatContext):
        #Skip if there's no orientation set
        if self._orientation is None:
            return
        
        #In general check whats there and set the constraint for all the items in the statement
        constraint = self._global_relative_operations[-1]
        for component in self._constrained_components:
            constraint.add_component(component, self._orientation)

        self.current_device.addConstraint(constraint)


    def exitNodeStat(self, ctx: mintParser.NodeStatContext):
        #TODO: Expand on neighbours until we hit all the components on the node periphery
        for component in self._constrained_components:
            if component is None:
                raise Exception("Could not apply Orthogonal Constraint, {} component not found !".format(name.getText()))
            
            if self._checkIfComponentConstranied(component):
                continue

            #TODO check if component exists in any of the of existing constraints
            components = OrthogonalConstraint.traverse_node_component_neighbours(component, self.current_device)
            constraint = OrthogonalConstraint(components)
            self.current_device.addConstraint(constraint)

        
        #TODO: Add all the components onto the list and create the constraint
    

    ##############Helpers############
    def _checkIfComponentConstranied(self, component:MINTComponent)->bool:
        found_flag = False
        for constraint in self.current_device.getConstraints():
            if isinstance(constraint, OrthogonalConstraint):
                found_flag = constraint.contains_component(component)
        
        return found_flag