DEVICE valve_test1

LAYER FLOW

PORT p1, p2;

CHANNEL c1 from p1 to p2;

END LAYER


LAYER CONTROL

VALVE v1 on c1;

PORT cp1;

CHANNEL cc1 from v1 to cp1;

END LAYER