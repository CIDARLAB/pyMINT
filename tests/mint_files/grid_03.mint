DEVICE grid_3_device

LAYER FLOW
PORT p1, p2 portRadius=100;
SQUARE CELL TRAP ct1 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct2 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct3 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct4 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct5 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct6 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct7 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct8 chamberWidth=100 chamberLength=100 channelWidth=100 ;
SQUARE CELL TRAP ct9 chamberWidth=100 chamberLength=100 channelWidth=100 ;
H TREE m1 spacing=1200 flowChannelWidth=100 in=1 out=3 ;
H TREE m2 spacing=1200 flowChannelWidth=100 in=3 out=1 ;
CONNECTION c1 from p1  to m1 1 w=100  ;
CONNECTION c2 from m1 2 to ct1 4 w=100  ;
CONNECTION c3 from m1 3 to ct2 4 w=100  ;
CONNECTION c4 from m1 4 to ct3 4 w=100  ;
CONNECTION c5 from ct1 3 to ct2 1 w=100  ;
CONNECTION c6 from ct2 3 to ct3 1 w=100  ;
CONNECTION c7 from ct1 2 to ct4 4 w=100  ;
CONNECTION c8 from ct2 2 to ct5 4 w=100  ;
CONNECTION c9 from ct3 2 to ct6 4 w=100  ;
CONNECTION c10 from ct4 3 to ct5 1 w=100  ;
CONNECTION c11 from ct5 3 to ct6 1 w=100  ;
CONNECTION c12 from ct4 2 to ct7 4 w=100  ;
CONNECTION c13 from ct5 2 to ct8 4 w=100  ;
CONNECTION c14 from ct6 2 to ct9 4 w=100  ;
CONNECTION c15 from ct7 3 to ct8 1 w=100  ;
CONNECTION c16 from ct8 3 to ct9 1 w=100  ;
CONNECTION c17 from ct7 2 to m2 1 w=100  ;
CONNECTION c18 from ct8 2 to m2 2 w=100  ;
CONNECTION c19 from ct9 2 to m2 3 w=100  ;
CONNECTION c20 from m2 4 to p2  w=100  ;
END LAYER

LAYER CONTROL
PORT vcp1;
PORT hcp1;
PORT vcp2;
PORT hcp2;
PORT vcp3;
VALVE v1 on c5 w=300 l=100 ;
VALVE v2 on c6 w=300 l=100 ;
VALVE v3 on c7 w=300 l=100 ;
VALVE v4 on c8 w=300 l=100 ;
VALVE v5 on c9 w=300 l=100 ;
VALVE v6 on c10 w=300 l=100 ;
VALVE v7 on c11 w=300 l=100 ;
VALVE v8 on c12 w=300 l=100 ;
VALVE v9 on c13 w=300 l=100 ;
VALVE v10 on c14 w=300 l=100 ;
VALVE v11 on c15 w=300 l=100 ;
VALVE v12 on c16 w=300 l=100 ;
CONNECTION n1 from vcp1  to v1 , v2  w=100  ;
CONNECTION cc1 from v3  to v4  w=100  ;
CONNECTION cc2 from v4  to v5  w=100  ;
CONNECTION cc3 from v5  to hcp1  w=100  ;
CONNECTION n2 from vcp2  to v6 , v7  w=100  ;
CONNECTION cc4 from v8  to v9  w=100  ;
CONNECTION cc5 from v9  to v10  w=100  ;
CONNECTION cc6 from v10  to hcp2  w=100  ;
CONNECTION n3 from vcp3  to v11 , v12  w=100  ;
END LAYER