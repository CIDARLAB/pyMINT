import logging
from typing import Dict, Optional

from parchmint import Layer, Target

from pymint.antlrgen.mintListener import mintListener
from pymint.antlrgen.mintParser import mintParser
from pymint.mintdevice import MINTDevice
from pymint.mintlayer import MINTLayerType


class MINTCompiler(mintListener):
    """Primary ANTLR listener class for the compiler"""

    def __init__(self):
        super().__init__()
        self.current_device: MINTDevice = MINTDevice("DEFAULT_NAME")
        self.current_block_id = 0
        self.current_layer_id = 0
        self.flow_layer_count = 0
        self.control_layer_count = 0
        self.integration_layer_count = 0
        self.current_entity: Optional[str] = None
        self.current_params: Dict = {}
        self._current_layer: Optional[Layer] = None

    def enterNetlist(self, ctx: mintParser.NetlistContext):
        self.current_device = MINTDevice("DEFAULT_NAME")

    def exitNetlist(self, ctx: mintParser.NetlistContext):
        if self.current_device is None:
            raise Exception("Could not find the device")

    def enterHeader(self, ctx: mintParser.HeaderContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        if ctx.device_name is None:
            raise Exception("Could not find Device Name")
        self.current_device.device.name = ctx.device_name.text

    def exitLayerBlock(self, ctx: mintParser.LayerBlockContext):
        # Increement teh layer block
        self.current_block_id += 1

    def enterFlowBlock(self, ctx: mintParser.FlowBlockContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )
        layer = self.current_device.create_mint_layer(
            str(self.current_layer_id),
            str(self.flow_layer_count),
            str(self.current_block_id),
            MINTLayerType.FLOW,
        )
        self._current_layer = layer
        self.flow_layer_count += 1
        self.current_layer_id += 1

    def enterControlBlock(self, ctx: mintParser.ControlBlockContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        layer = self.current_device.create_mint_layer(
            str(self.current_layer_id),
            str(self.control_layer_count),
            str(self.current_block_id),
            MINTLayerType.CONTROL,
        )
        self._current_layer = layer
        self.control_layer_count += 1
        self.current_layer_id += 1

    def enterIntegrationBlock(self, ctx: mintParser.IntegrationBlockContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        layer = self.current_device.create_mint_layer(
            str(self.current_layer_id),
            str(self.integration_layer_count),
            str(self.current_block_id),
            MINTLayerType.INTEGRATION,
        )
        self._current_layer = layer
        self.integration_layer_count += 1
        self.current_layer_id += 1

    def enterEntity(self, ctx: mintParser.EntityContext):
        self.current_entity = ctx.getText()

    def enterParamsStat(self, ctx: mintParser.ParamsStatContext):
        self.current_params = {}

    def enterIntParam(self, ctx: mintParser.IntParamContext):
        value = ctx.value().getText()  # type: ignore
        key = ctx.param_element().getText()  # type: ignore
        self.current_params[key] = int(value)

    def enterBoolParam(self, ctx: mintParser.BoolParamContext):
        if ctx.boolvalue.getText() == "YES":
            value = True
        else:
            value = False
        key = ctx.param_element.getText()
        self.current_params[key] = value

    def enterLengthParam(self, ctx: mintParser.LengthParamContext):
        value = float(ctx.value().getText())  # type: ignore
        self.current_params["length"] = value

    def enterSpacingParam(self, ctx: mintParser.SpacingParamContext):
        value = float(ctx.value().getText())  # type: ignore
        self.current_params["spacing"] = value

    def enterWidthParam(self, ctx: mintParser.WidthParamContext):
        value = ctx.value().getText()  # type: ignore
        if ctx.key is None:
            raise AssertionError
        key = ctx.key.text
        if key is None:
            raise Exception("Error in parsing the width parameter")
        if key == "w":
            key = "width"

        self.current_params[key] = int(value)

    def enterFlowStat(self, ctx: mintParser.FlowStatContext):
        self.current_entity = None
        self.current_params = {}

    def enterControlStat(self, ctx: mintParser.ControlStatContext):
        self.current_entity = None
        self.current_params = {}

    def exitPrimitiveStat(self, ctx: mintParser.PrimitiveStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the pimitive")

        # Loop for each of the components that need to be created with this param
        for ufname in ctx.ufnames().ufname():  # type: ignore
            if self._current_layer is None:
                raise Exception("Current layer is set to None")
            if not (
                self._current_layer is not None and self._current_layer.ID is not None
            ):
                raise AssertionError
            self.current_device.create_mint_component(
                ufname.getText(),
                entity,
                self.current_params,
                [self._current_layer.ID],
            )

    def exitBankDeclStat(self, ctx: mintParser.BankDeclStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the primitive")

        # Clean up the constraint specific params
        self._cleanup_bank_params()

        for ufname in ctx.ufnames().ufname():  # type: ignore
            component_name = ufname.getText()
            if self._current_layer is None:
                raise AssertionError
            self.current_device.create_mint_component(
                component_name,
                entity,
                self.current_params,
                [self._current_layer.ID],
            )

    def exitBankGenStat(self, ctx: mintParser.BankGenStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the primitive")

        self._cleanup_bank_params()

        if ctx.dim is None:
            raise AssertionError
        dim = int(ctx.dim.text)

        name = ctx.ufname().getText()  # type: ignore

        for i in range(1, dim + 1):
            component_name = name + "_" + str(i)
            if self._current_layer is None:
                raise Exception("Current Layer not Set")
            if not (
                self._current_layer is not None and self._current_layer.ID is not None
            ):
                raise AssertionError
            self.current_device.create_mint_component(
                component_name, entity, self.current_params, [self._current_layer.ID]
            )

    def exitGridDeclStat(self, ctx: mintParser.GridDeclStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the primitive")

        self._cleanup_grid_params()

        for ufname in ctx.ufnames().ufname():  # type: ignore
            component_name = ufname.getText()
            if self._current_layer is None:
                raise AssertionError
            self.current_device.create_mint_component(
                component_name,
                entity,
                self.current_params,
                [self._current_layer.ID],
            )

    def exitChannelStat(self, ctx: mintParser.ChannelStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        entity = self.current_entity
        if entity is None:
            entity = "CHANNEL"
        connection_name = ctx.ufname().getText()  # type: ignore

        source_target = ctx.uftarget()[0]  # type: ignore
        source_id = source_target.ID().getText()
        if self.current_device.device.component_exists(source_id) is False:
            raise Exception(
                "Error ! - Could not find the component '{}' in device '{}'".format(
                    source_id, self.current_device.device.name
                )
            )
        if source_target.INT():
            source_port = source_target.INT().getText()
        else:
            source_port = None

        # source_uftarget = Target(component_id=source_id, port=source_port)
        source_uftarget = Target(component_id=source_id, port=source_port)

        sink_target = ctx.uftarget()[1]  # type: ignore
        sink_id = sink_target.ID().getText()
        if self.current_device.device.component_exists(sink_id) is False:
            raise Exception(
                "Error ! - Could not find the component '{}' in device '{}'".format(
                    sink_id, self.current_device.device.name
                )
            )
        if sink_target.INT():
            sink_port = sink_target.INT().getText()
        else:
            sink_port = None

        sink_uftarget = Target(component_id=sink_id, port=sink_port)

        self._cleanup_channel_params()

        # Create a connection between the different components in the device
        if not (self._current_layer is not None and self._current_layer.ID is not None):
            raise AssertionError
        self.current_device.create_mint_connection(
            connection_name,
            entity,
            self.current_params,
            source_uftarget,
            [sink_uftarget],
            self._current_layer.ID,
        )

    def exitNetStat(self, ctx: mintParser.NetStatContext):
        entity = self.current_entity
        if entity is None:
            entity = "NET"

        connection_name = ctx.ufname().getText()  # type: ignore

        source_target = ctx.uftarget()
        source_id = source_target.ID().getText()  # type: ignore
        if source_target.INT():  # type: ignore
            source_port = source_target.INT().getText()  # type: ignore
        else:
            source_port = None

        source_uftarget = Target(component_id=source_id, port=source_port)

        sink_uftargets = []

        for sink_target in ctx.uftargets().uftarget():  # type: ignore
            sink_id = sink_target.ID().getText()
            if sink_target.INT():
                sink_port = sink_target.INT().getText()
            else:
                sink_port = None

            sink_uftargets.append(Target(component_id=sink_id, port=sink_port))
        if not (self._current_layer is not None and self._current_layer.ID is not None):
            raise AssertionError
        self.current_device.create_mint_connection(
            connection_name,
            entity,
            self.current_params,
            source_uftarget,
            sink_uftargets,
            self._current_layer.ID,
        )

    def exitSpanStat(self, ctx: mintParser.SpanStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the pimitive")

        # pipe in the in / out values to params for sizing
        if ctx.indim is not None:
            in_value = int(ctx.indim.text)
            self.current_params["in"] = in_value
        if ctx.outdim is not None:
            out_value = int(ctx.outdim.text)
            self.current_params["out"] = out_value

        # Loop for each of the components that need to be created with this param
        for ufname in ctx.ufnames().ufname():  # type: ignore
            if self._current_layer is None:
                raise AssertionError
            self.current_device.create_mint_component(
                ufname.getText(),
                entity,
                self.current_params,
                [self._current_layer.ID],
            )

    def exitNodeStat(self, ctx: mintParser.NodeStatContext):
        entity = "NODE"
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        # Loop for each of the components that need to be created with this param
        if not (self._current_layer is not None and self._current_layer.ID is not None):
            raise AssertionError
        for ufname in ctx.ufnames().ufname():  # type: ignore
            self.current_device.create_mint_component(
                ufname.getText(),
                entity,
                self.current_params,
                [self._current_layer.ID],
            )

    def exitValveStat(self, ctx: mintParser.ValveStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        entity = self.current_entity
        if entity is None:
            logging.error("Could not find entitry information for valve")
            raise Exception("Could not find entitry information for valve")
        valve_name = ctx.ufname()[0].getText()  # type: ignore
        if not (self._current_layer is not None and self._current_layer.ID is not None):
            raise AssertionError
        valve_component = self.current_device.create_mint_component(
            valve_name,
            entity,
            self.current_params,
            [self._current_layer.ID],
        )
        connection_name = ctx.ufname()[1].getText()  # type: ignore
        valve_connection = self.current_device.device.get_connection(connection_name)
        if valve_connection is None:
            raise Exception(
                "Error: Could not find connection '{}' in device '{}'".format(
                    connection_name, self.current_device.device.name
                )
            )

        self.current_device.device.map_valve(valve_component, valve_connection)

    def enterViaStat(self, ctx: mintParser.ViaStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        for ufname in ctx.ufnames().ufname():
            self.current_device.add_via(ufname.getText(), [])

    def enterTerminalStat(self, ctx: mintParser.TerminalStatContext):
        if self.current_device is None:
            raise Exception(
                "Error Initializing the device. Could not find the current device"
            )

        terminal_name = ctx.ufname().getText()
        pin_number = int(ctx.INT.getText())
        if not (self._current_layer is not None and self._current_layer.ID is not None):
            raise AssertionError
        self.current_device.add_terminal(
            terminal_name,
            pin_number,
            self._current_layer.ID,
        )

    def _cleanup_bank_params(self):
        if "spacing" in self.current_params:
            del self.current_params["spacing"]

    def _cleanup_grid_params(self):
        if "horizontalSpacing" in self.current_params:
            del self.current_params["horizontalSpacing"]
        if "verticalSpacing" in self.current_params:
            del self.current_params["verticalSpacing"]

    def _cleanup_channel_params(self):
        if "length" in self.current_params:
            del self.current_params["length"]
