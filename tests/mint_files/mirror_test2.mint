DEVICE mirror_test2

LAYER FLOW

PORT p_in1, p_out1, p_out2, p_out3, p_out4;

TREE t1 1 to 4;

LONG CELL TRAP lct1, lct2, lct3, lct4;

CHANNEL c_in1 from p_in1 to t1 1;

CHANNEL c_lct1 from t1 2 to lct1;

CHANNEL c_lct2 from t1 3 to lct2;

CHANNEL c_lct3 from t1 4 to lct3;

CHANNEL c_lct4 from t1 5 to lct4;

CHANNEL c_out1 from lct1 to p_out1;

CHANNEL c_out2 from lct2 to p_out2;

CHANNEL c_out3 from lct3 to p_out3;

CHANNEL c_out4 from lct4 to p_out4;


END LAYER
