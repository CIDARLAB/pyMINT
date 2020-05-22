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
    |   nodeStat
    |   channelStat
    |   netStat
    |   bankDeclStat
    |   gridStat
    |   spanStat
    |   viaStat
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
    :   orientation? entity ufnames paramsStat ';'
    ;

bankDeclStat
    :   orientation? 'BANK' ufnames 'of' dim=INT entity paramsStat ';'
    ;

bankGenStat
    :   orientation? 'BANK' ufname 'of' dim=INT entity paramsStat ';'
    ;

bankStat
    :   orientation? 'BANK' ufnames 'of' dim=INT paramsStat ';'
    ;

gridGenStat
    :   orientation? 'GRID' ufname 'of' xdim=INT ',' ydim=INT entity paramsStat ';'
    ;

gridDeclStat
    :   orientation? 'GRID' ufnames 'of' xdim=INT ',' ydim=INT paramsStat ';'
    ;

gridStat
    :   orientation? 'GRID' ufnames 'of' xdim=INT ',' ydim=INT paramsStat ';'
    ;

spanStat
    :   orientation? entity ufnames  indim=INT 'to' outdim=INT paramsStat ';'
    ;

valveStat
    :   entity ufname 'on' ufname paramsStat ';'
    ;

nodeStat
    :   'NODE' ufnames ';'
    ;

viaStat
    :   'VIA' ufnames ';'
    ;

terminalStat
    :   'TERMINAL' ufname pin=INT ';'
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

spacingParam: 'spacing' '=' value;

directionParam: 'direction''=' direction=('UP'|'DOWN'|'LEFT'|'RIGHT');

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
    ;

verticalSpacingParam
    :   'horizontalSpacing''=' value
    ;

horizontalSpacingParam
    :   'horizontalSpacing''=' value
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
    |   Real_number
    ;

boolvalue
    :   'YES'
    |   'NO'
    ;

//Constraints
positionConstraintStat
    :   ufname 'SET' setCoordinate+ ';'
    ;

setCoordinate
    :   coordinate=('X'|'Y'|'Z') INT
    ;

orientation : ('V'|'H') ;

//Common Lexical Rules

ID : ('a'..'z'|'_')('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;

ID_BIG  :  ('A'..'Z'|'_') ('A'..'Z'|'_'|'0'..'9')*  ;

INT :   [0-9]+ ; // Define token INT as one or more digits

WS  :   [ \t\r\n]+ -> skip ; // Define whitespace rule, toss it out

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
