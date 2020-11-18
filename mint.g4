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
    :   'IMPORT' WS+ ufmodulename
    ;

header
    :   'DEVICE' WS+ device_name=ID
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
    :   (orientation WS+)?  entity WS+ ufnames WS+ paramsStat ';'
    ;

bankDeclStat
    :   (orientation WS+)? 'BANK' WS+ ufnames WS+ 'of' WS+ entity WS+ paramsStat ';'
    ;

bankGenStat
    :   (orientation WS+)? 'BANK' WS+ ufname 'of' dim=INT WS+ entity WS+ paramsStat ';'
    ;

bankStat
    :   (orientation WS+)? 'BANK' WS+ ufnames WS+ 'of' WS+ dim=INT WS+ paramsStat ';'
    ;

gridGenStat
    :   (orientation WS+)? 'GRID' WS+ ufname WS+ 'of' WS+ xdim=INT WS* ',' WS* ydim=INT WS+ entity WS+ paramsStat ';'
    ;

gridDeclStat
    :   (orientation WS+)? 'GRID' WS+ ufnames WS+ 'of' WS+ xdim=INT WS* ',' WS* ydim=INT WS+ entity WS+ paramsStat ';'
    ;

gridStat
    :   orientation? 'GRID' WS+ ufnames WS+  'of' WS+ xdim=INT ',' ydim=INT WS+ paramsStat ';'
    ;

spanStat
    :   orientation? entity WS+ ufnames WS+ indim=INT WS+ 'to' WS+ outdim=INT WS+ paramsStat ';'
    ;

valveStat
    :   entity ufname 'on' ufname paramsStat ';'
    ;

nodeStat
    :   'NODE' WS+ ufnames ';'
    ;

viaStat
    :   'VIA' WS+ ufnames ';'
    ;

terminalStat
    :   'TERMINAL' WS+ ufname WS+ pin=INT ';'
    ;

channelStat
    :   (entity|'CHANNEL') WS+ ufname WS+ 'from' WS+ source=uftarget WS+ 'to' WS+ sink=uftarget WS* paramsStat ';'
    ;

netStat
    :   (entity|'NET') ufname 'from' source=uftarget 'to' sinks=uftargets paramsStat ';'
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
    :   ufname WS* (',' WS* ufname)*
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
    :   ufname WS+ 'SET' WS+ setCoordinate+ ';'
    ;

setCoordinate
    :   coordinate=('X'|'Y'|'Z') INT
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
