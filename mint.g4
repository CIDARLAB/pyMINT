/*
 * krishna
 */

grammar mint;

netlist
    :   importBlock?
        header
        ufmoduleBlock?
        layerBlocks
        EOF
    ;

importBlock
    :   importStat+
    ;

importStat
    :   'IMPORT' ufmodulename
    ;

header
    :   'DEVICE' device_name=ID
    ;

ufmoduleBlock
    :   ufmoduleStat+
    ;

ufmoduleStat
    :   ufmodulename ufnames ';'
    ;

layerBlocks
    :   layerBlock+
    ;

layerBlock
    :   flowBlock
        controlBlock?
        integrationBlock?
    ;


flowBlock
    :   'LAYER FLOW'
        (flowStat)*
        'END LAYER'
    ;

controlBlock
    :   'LAYER CONTROL'
        (controlStat)*
        'END LAYER'
    ;

integrationBlock
    :   'LAYER INTEGRATION'
        (integrationStat)*
        'END LAYER'
    ;

flowStat
    :   primitiveStat
    |   primitiveWithOrientationConstraintStat
    |   nodeStat
    |   channelStat
    |   netStat
    |   bankStat
    |   gridStat
    |   spanStat
    ;

controlStat
    :   valveStat
    |   channelStat
    |   netStat
    |   bankStat
    |   primitiveStat
    ;

integrationStat
    :   primitiveStat
    ;

//Flow and Control Statements

primitiveStat
    :   entity ufnames paramsStat ';'
    ;

bankStat
    :   'BANK' ufnames 'of' dim=INT entity paramsStat ';'
    ;

gridStat
    :   'GRID' ufnames 'of' xdim=INT ',' ydim=INT paramsStat ';'
    ;

spanStat
    :   entity ufnames  indim=INT 'to' outdim=INT paramsStat ';'
    ;

primitiveWithOrientationConstraintStat
    :   orientation ( bankStat | spanStat | primitiveStat )
    ;

valveStat
    :   valve_entity=('VALVE'|'3DVALVE') ufname 'on' ufname paramsStat ';'
    ;

nodeStat
    :   'NODE' ufnames ';'
    ;

channelStat
    :   (entity|'CHANNEL') ufname 'from' source=uftarget 'to' sink=uftarget paramsStat ';'
    ;

netStat
    :   (entity|'NET') ufname 'from' source=uftarget 'to' sinks=uftargets paramsStat ';'
    ;

//Common Parser Rules

entity
    :   entity_element+
    ;

entity_element
    :   ID_BIG
    ;

paramsStat
    :   paramStat*
    ;

connectionParamStat
    :   lengthParam
    |   paramsStat
    ;

paramStat
    :   intParam
    |   boolParam
    |   verticalDirectionParam
    |   horizontalDirectionParam
    |   widthParam
    ;

param_element
    :   ID
    ;

intParam
    :   param_element '=' value
    ;

boolParam
    :   param_element '=' boolvalue
    ;

widthParam
    :   key='width' '=' value
    |   key='w' '=' value
    |   key='channelWidth' '=' value
    ;

verticalDirectionParam
    :   'dir''='direction=('RIGHT'|'LEFT')
    ;

horizontalDirectionParam
    :   'dir''='direction=('UP'|'DOWN')
    ;

rotationParam
    :   'rotation' '=' rotation=value
    ;

lengthParam
    :   'length' '=' length=value
    ;

ufmodulename
    :   ID_BIG
    ;

ufterminal
    :   INT
    ;

uftargets
    :    uftarget (',' uftarget)+
    ;

uftarget
    :   target_name=ID (target_terminal=INT)?
    ;

ufname
    :   ID
    ;

ufnames
    :   ufname (',' ufname)*
    ;

value
    :   INT
    ;

boolvalue
    :   'YES'
    |   'NO'
    ;

orientation : ('V'|'H') ;

//Common Lexical Rules

ID : ('a'..'z'|'_')('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;

ID_BIG  :  ('A'..'Z'|'_') ('A'..'Z'|'_'|'0'..'9')*  ;

INT :   [0-9]+ ; // Define token INT as one or more digits

WS  :   [ \t\r\n]+ -> skip ; // Define whitespace rule, toss it out

COMMENT :    '#' ~[\r\n]* -> skip ;