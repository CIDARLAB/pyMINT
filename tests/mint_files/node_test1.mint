DEVICE node_test1

LAYER FLOW

NODE n1, n2, n3;

PORT p1, p2, p3;

CHANNEL c1 from p1 to n1;

CHANNEL c2 from n1 to n2;

CHANNEL c3 from n2 to n3;

CHANNEL c4 from n3 to p3;

CHANNEL c5 from n2 to p2;


END LAYER