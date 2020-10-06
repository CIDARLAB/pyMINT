import logging
from pymint.minttarget import MINTTarget
from pymint.mintcomponent import MINTComponent
from parchmint.component import Component
from pymint.mintdevice import MINTDevice
from pymint.antlr.mintListener import mintListener
from pymint.antlr.mintParser import mintParser
from pymint.mintlayer import MINTLayer, MINTLayerType
from typing import Optional

class MINTCompiler(mintListener):

    def __init__(self):
        super().__init__()
        self.current_device: Optional[MINTDevice] = None
        self.current_block_id = 0
        self.current_layer_id = 0
        self.current_entity: Optional[str]
        self.current_params = dict()

    def enterNetlist(self, ctx: mintParser.NetlistContext):
        self.current_device = MINTDevice("DEFAULT_NAME")

    
    def enterHeader(self, ctx: mintParser.HeaderContext):
        if ctx.device_name is None:
            raise Exception("Could not find Device Name")
        self.current_device.name = ctx.device_name.text

    def exitLayerBlock(self, ctx: mintParser.LayerBlockContext):
        #Increement teh layer block
        self.current_block_id += 1

    def enterFlowBlock(self, ctx: mintParser.FlowBlockContext):
        self.current_device.addLayer(str(self.current_layer_id), str(self.current_block_id), MINTLayerType.FLOW)

    def exitLayerBlock(self, ctx: mintParser.FlowBlockContext):
        self.current_layer_id += 1
    
    def enterControlBlock(self, ctx: mintParser.ControlBlockContext):
        self.current_device.addLayer(str(self.current_layer_id), str(self.current_block_id), MINTLayerType.FLOW)

    def enterIntegrationBlock(self, ctx: mintParser.IntegrationBlockContext):
        self.current_device.addLayer(str(self.current_layer_id), str(self.current_block_id), MINTLayerType.INTEGRATION)

    def enterEntity(self, ctx: mintParser.EntityContext):
        self.current_entity = ctx.getText()
    
    def enterParamsStat(self, ctx: mintParser.ParamsStatContext):
        self.current_params = dict()

    def enterIntParam(self, ctx: mintParser.IntParamContext):
        value = ctx.value().getText()
        key = ctx.param_element().getText()
        self.current_params[key] = int(value)

    def enterBoolParam(self, ctx: mintParser.BoolParamContext):
        if ctx.boolvalue.getText() == 'YES' : 
            value = True
        else:
            value = False
        key = ctx.param_element.getText()
        self.current_params[key] = value

    def enterLengthParam(self, ctx: mintParser.LengthParamContext):
        value = float(ctx.value().getText())
        self.current_params['length'] = value
    
    def enterSpacingParam(self, ctx: mintParser.SpacingParamContext):
        value = float(ctx.value().getText())
        self.current_params['spacing'] = value
    
    def enterWidthParam(self, ctx: mintParser.WidthParamContext):
        value = ctx.value().getText()
        key = ctx.key.text
        if key is None:
            raise Exception("Error in parsing the width parameter")
        if key =='w' :
            key = 'width'
        
        self.current_params[key] = int(value)

    def enterFlowStat(self, ctx: mintParser.FlowStatContext):
        self.current_entity = None
        self.current_params = dict()

    def exitPrimitiveStat(self, ctx: mintParser.PrimitiveStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the pimitive")
        
        #Loop for each of the components that need to be created with this param
        for ufname in ctx.ufnames().ufname():
            self.current_device.addComponent(ufname.getText(), entity, self.current_params, str(self.current_layer_id))
    

    def exitBankDeclStat(self, ctx: mintParser.BankDeclStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the primitive")

        for ufname in ctx.ufnames().ufname():
            component_name = ufname.getText()
            self.current_device.addComponent(component_name, entity, self.current_params, str(self.current_layer_id))

    def exitBankGenStat(self, ctx:mintParser.BankGenStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the primitive")

        dim = int(ctx.dim.text)

        name = ctx.ufname().getText()

        for i in range(1, dim+1):
            component_name = name + "_" + str(i)
            self.current_device.addComponent(component_name, entity, self.current_params, str(self.current_layer_id))

    def exitGridDeclStat(self, ctx: mintParser.GridDeclStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the primitive")

        for ufname in ctx.ufnames().ufname():
            component_name = ufname.getText()
            self.current_device.addComponent(component_name, entity, self.current_params, str(self.current_layer_id))

    def exitChannelStat(self, ctx: mintParser.ChannelStatContext):
        entity = self.current_entity
        if entity is None:
            entity = 'CHANNEL'
        connection_name = ctx.ufname().getText()

        source_target = ctx.uftarget()[0]
        source_id = source_target.ID().getText()
        if self.current_device.component_exists(source_id) is False:
            raise Exception("Error ! - Could not find the component '{}' in device '{}'".format(source_id, self.current_device.name))
        if source_target.INT():
            source_port = source_target.INT().getText()
        else:
            source_port = None

        source_uftarget = MINTTarget(source_id, source_port)

        sink_target = ctx.uftarget()[1]
        sink_id = sink_target.ID().getText()
        if self.current_device.component_exists(sink_id) is False:
            raise Exception("Error ! - Could not find the component '{}' in device '{}'".format(sink_id, self.current_device.name))
        if sink_target.INT():
            sink_port = sink_target.INT().getText()
        else:
            sink_port = None

        sink_uftarget = MINTTarget(sink_id, sink_port)
        
        #Create a connection between the different components in the device
        self.current_device.addConnection(connection_name, entity, self.current_params, source_uftarget, [sink_uftarget], str(self.current_layer_id))

    def exitNetStat(self, ctx: mintParser.NetStatContext):
        entity = self.current_entity
        if entity is None:
            entity = 'NET'
        
        connection_name = ctx.ufname().getText()
        
        source_target = ctx.uftarget()
        source_id = source_target.ID().getText()
        if source_target.INT():
            source_port = source_target.INT().getText()
        else:
            source_port = None

        source_uftarget = MINTTarget(source_id, source_port)

        sink_uftargets = []

        for sink_target in ctx.uftargets().uftarget():
            sink_id = sink_target.ID().getText()
            if sink_target.INT():
                sink_port = sink_target.INT().getText()
            else:
                sink_port = None

            sink_uftargets.append(MINTTarget(sink_id, sink_port))

        self.current_device.addConnection(connection_name, entity, self.current_params, source_uftarget, sink_uftargets, str(self.current_layer_id))

    def exitSpanStat(self, ctx: mintParser.SpanStatContext):
        entity = self.current_entity
        if entity is None:
            raise Exception("Could not find the technology for the pimitive")
        
        #Loop for each of the components that need to be created with this param
        for ufname in ctx.ufnames().ufname():
            self.current_device.addComponent(ufname.getText(), entity, self.current_params, str(self.current_layer_id))

        #TODO: Figure out how to pipe in the in / out format


    def exitNodeStat(self, ctx: mintParser.NodeStatContext):
        entity = 'NODE'
        
        #Loop for each of the components that need to be created with this param
        for ufname in ctx.ufnames().ufname():
            self.current_device.addComponent(ufname.getText(), entity, self.current_params, str(self.current_layer_id))

    def exitValveStat(self, ctx: mintParser.ValveStatContext):
        entity =  self.current_entity
        if entity is None:
            logging.error("Could not find entitry information for valve")
            raise Exception("Could not find entitry information for valve")
        valve_name = ctx.ufname()[0].getText()
        valve_component = self.current_device.addComponent(valve_name, entity, self.current_params, str(self.current_layer_id))
        connection_name = ctx.ufname()[1].getText()
        valve_connection = self.current_device.getConnection(connection_name)
        if valve_connection is None:
            raise Exception("Error: Could not find connection '{}' in device '{}'".format(connection_name, self.current_device.name))
        
        self.current_device.mapValve(valve_component, valve_connection)

    def enterViaStat(self, ctx:mintParser.ViaStatContext):
        for ufname in ctx.ufnames().ufname():
            self.current_device.addVia(ufname.getText(),)

    def enterTerminalStat(self, ctx:mintParser.TerminalStatContext):
        terminal_name = ctx.ufname().getText()
        pin_number = int(ctx.INT.getText())
        self.current_device.addTerminal(terminal_name, pin_number, str(self.current_layer_id))
        
    def exitNetlist(self, ctx: mintParser.NetlistContext):
        self.current_device.generate_network()



        

    


    

        


    



