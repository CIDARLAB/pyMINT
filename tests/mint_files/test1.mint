DEVICE test1

LAYER flow
PORT p1, p2, p3portRadius=100;
NODE n1;
H LONG CELL TRAP ct1numberOfChambers=10 chamberWidth=100 chamberLength=100 chamberSpacing=30 feedingChannelWidth=100;
CHANNEL c1 from p1 to n1channelWidth=100;
CHANNEL c2 from p2 to n1channelWidth=100;
CHANNEL c3 from n1 to ct1 1channelWidth=100;
CHANNEL c4 from ct1 2 to p3 channelWidth=100;
END layer

LAYER control
PORT cp1, cp2portRadius=100;
VALVE v1 on c1 width=300 length=100;
VALVE v2 on c2 width=300 length=100;
CHANNEL c5 from cp1 to v1channelWidth=50;
CHANNEL c6 from cp2 to v2channelWidth=50;
END layer