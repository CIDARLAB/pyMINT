DEVICE mirror_test1

LAYER FLOW

PORT p_in1, p_out1, p_out2, p_out3, p_out4;

TREE t1 1 to 4;

CHANNEL c_in1 from p_in1 to t1 1;

CHANNEL c_out1 from t1 2 to p_out1;

CHANNEL c_out2 from t1 3  to p_out2;

CHANNEL c_out3 from t1 4 to p_out3;

CHANNEL c_out4 from t1 5 to p_out4;

END LAYER
