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
    :   WS* 'IMPORT' WS+ ufmodulename
    ;

header
    :   WS* 'DEVICE' WS+ device_name=ID
    ;

ufmoduleBlock
    :   globalStats+
    ;

globalStats
    :   ufmoduleStat
    |   viaStat
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
    :   WS*'LAYER FLOW'
        (WS* flowStat)*
        WS*'END LAYER'
    ;

controlBlock
    :   WS*'LAYER CONTROL'
        (WS* controlStat)*
        WS*'END LAYER'
    ;

integrationBlock
    :   'LAYER INTEGRATION'
        (integrationStat)*
        'END LAYER'
    ;

flowStat
    :   primitiveStat
    |   nodeStat
    |   channelStat
    |   netStat
    |   bankDeclStat
    |   gridStat
    |   spanStat
    |   positionConstraintStat
    |   gridStat
    |   gridGenStat
    |   gridDeclStat
    |   bankStat
    |   bankGenStat
    |   bankDeclStat
    |   terminalStat
    ;

controlStat
    :   valveStat
    |   channelStat
    |   netStat
    |   bankDeclStat
    |   bankStat
    |   bankGenStat
    |   gridStat
    |   gridGenStat
    |   primitiveStat
    |   nodeStat
    |   viaStat
    |   positionConstraintStat
    |   terminalStat
    ;

integrationStat
    :   primitiveStat
    |   positionConstraintStat
    ;

//Flow and Control Statements

primitiveStat
    :   (orientation WS+)?  entity WS+ ufnames (WS+ paramsStat)? statTerminaion
    ;

bankDeclStat
    :   (orientation WS+)? 'BANK' WS+ ufnames WS+ 'of' WS+ entity (WS+ paramsStat)? statTerminaion
    ;

bankGenStat
    :   (orientation WS+)? 'BANK' WS+ ufname  WS+ 'of'  WS+ dim=INT WS+ entity (WS+ paramsStat)? statTerminaion
    ;

bankStat
    :   (orientation WS+)? 'BANK' WS+ ufnames (WS+ paramsStat)? statTerminaion
    ;

gridGenStat
    :   (orientation WS+)? 'GRID' WS+ ufname WS+ 'of' WS+ xdim=INT WS* ',' WS* ydim=INT WS+ entity (WS+ paramsStat)? statTerminaion
    ;

gridDeclStat
    :   (orientation WS+)? 'GRID' WS+ ufnames WS+ 'of' WS+ xdim=INT WS* ',' WS* ydim=INT WS+ entity (WS+ paramsStat)? statTerminaion
    ;

gridStat
    :   (orientation WS+)? 'GRID' WS+ ufnames WS+  'of' WS+ xdim=INT WS* ',' WS* ydim=INT (WS+ paramsStat)? statTerminaion
    ;

spanStat
    :   (orientation WS+)? entity WS+ ufnames WS+ indim=INT WS+ 'to' WS+ outdim=INT (WS+ paramsStat)? statTerminaion
    ;

valveStat
    :   entity WS+ ufname WS+ 'on' WS+ ufname (WS+ paramsStat)? statTerminaion
    ;

nodeStat
    :   'NODE' WS+ ufnames statTerminaion
    ;

viaStat
    :   'VIA' WS+ ufnames statTerminaion
    ;

terminalStat
    :   'TERMINAL' WS+ ufname WS+ pin=INT statTerminaion
    ;

channelStat
    :   (entity|'CHANNEL') WS+ ufname WS+ 'from' WS+ source=uftarget WS+ 'to' WS+ sink=uftarget WS* (WS+ paramsStat)? statTerminaion
    ;

netStat
    :   (entity|'NET') WS+ ufname WS+ 'from' WS+ source=uftarget WS+ 'to' WS+ sinks=uftargets (WS+ paramsStat)? statTerminaion
    ;

//Common Parser Rules

entity
    :   entity_element (WS entity_element)*
    ;

entity_element
    :   ID_BIG
    ;

paramsStat
    :   (paramStat WS*)*
    ;

statTerminaion : WS* ';' WS* ;
//connectionParamStat
//    :   lengthParam
//    |   paramsStat
//    ;

connectionParamStat
    :   paramsStat
    ;

paramStat
    :   intParam
    |   boolParam
    |   widthParam
    |   constraintParams
    |   lengthParam
    |   spacingParam
    ;

constraintParams
    :   rotationParam
    |   directionParam
    |   spacingParam
    |   lengthParam
    |   verticalSpacingParam
    |   horizontalSpacingParam
    ;

spacingParam: 'spacing'WS*'=' WS* value;

directionParam: 'direction''=' direction=('UP'|'DOWN'|'LEFT'|'RIGHT');

param_element
    :   ID
    ;

intParam
    :   param_element '=' WS* value
    ;

boolParam
    :   param_element '=' boolvalue
    ;

widthParam
    :   key='width'WS*'=' WS* value
    |   key='w'WS*'=' WS* value
    ;

verticalSpacingParam
    :   'horizontalSpacing'WS*'=' WS* value
    ;

horizontalSpacingParam
    :   'horizontalSpacing'WS*'=' WS* value
    ;

rotationParam
    :   'rotation'WS*'=' WS* rotation=value
    ;

lengthParam
    :   'length'WS*'=' WS* length=value
    ;

ufmodulename
    :   ID_BIG
    ;

ufterminal
    :   INT
    ;

uftargets
    :    uftarget WS* (',' WS* uftarget)+
    ;

uftarget
    :   target_name=ID (WS+ target_terminal=INT)?
    ;

ufname
    :   ID
    ;

ufnames
    :   ufname WS* (',' WS* ufname)* WS*
    ;

value
    :   INT
    |   Real_number
    ;

boolvalue
    :   'YES'
    |   'NO'
    ;

//Constraints
positionConstraintStat
    :   ufname WS+ 'SET' setCoordinate+ ';'
    ;

setCoordinate
    :   WS+ coordinate=('X'|'Y'|'Z') WS+ INT
    ;

orientation : ('V'|'H') ;

//Common Lexical Rules

ID : ('a'..'z'|'_')('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;

ID_BIG  :  ('A'..'Z'|'_') ('A'..'Z'|'_'|'0'..'9')*  ;

INT :   [0-9]+ ; // Define token INT as one or more digits

WS  :   [ \t]+ ;

NL : [\r\n]+ -> skip ; // Define whitespace rule, toss it out

COMMENT :    '#' ~[\r\n]* -> skip ;

Real_number
   : Unsigned_number '.' Unsigned_number | Unsigned_number ('.' Unsigned_number)? [eE] ([+-])? Unsigned_number
   ;

fragment Unsigned_number
   : Decimal_digit ('_' | Decimal_digit)*
   ;

fragment Decimal_digit
   : [0-9]
   ;
