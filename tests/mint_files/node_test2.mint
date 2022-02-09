DEVICE node_test2

LAYER FLOW

NODE n1, n2, n3;

PORT p1, p2, p3, p4;

CHANNEL c1 from p1 to n1;

CHANNEL c2 from n1 to n2;

CHANNEL c3 from n2 to n3;

CHANNEL c4 from n3 to p2;

LONG CELL TRAP lct1, lct2;

CHANNEL c5 from n2 to lct1;

CHANNEL c6 from lct1 to lct2;

NODE n4, n5, n6;

CHANNEL c7 from p3 to n4;

CHANNEL c8 from n4 to n5;

CHANNEL c9 from n5 to n6;

CHANNEL c10 from n6 to p4;

CHANNEL c11 from lct2 to n5;

END LAYER