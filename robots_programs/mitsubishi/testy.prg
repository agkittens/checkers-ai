1 ' program testowy
2 '
3 '
4 Base  (+0.00,+0.00,+0.00,+0.00,+0.00,+0.00)
5 Tool (+0.00,+0.00,+0.00,+0.00,+0.00,+0.00)
6 '
7 ' speed
8 Spd 300
9 '
10 ' joints override
11 JOvrd 50
12 '
13 ' override
14 Ovrd 50
15 '
16 ' acceleration and decelaretion
17 Accel 50, 50
18 '
19 ' continuous movement control
20 Cnt 1, 100, 100
21 '
22 '
23 Servo On
24 Wait M_Svo(1)=1
25 '
26 ' composition off
27 Cmp Off
28 '
29 '
30 ' home position move
31 Mov j0
32 '
33 '
34 ' variables
35 isPlayerDone = 1
36 isDone = 0
37 valueToAdd = 200
38 waitTime = 3
39 a = 0
40 b = 0
41 '
42 '
43 WHILE isDone = 0
44  GoSub *pickNput
45  isDone = 1
46 WEnd
47 '
48 Mov j0
49 End
50 '
51 '
52 '
53 ' ---------------------------------- transformacja pozycji ---------------------------------------------
54 *transform 
55 DIM v0(2), v1(2)  
56 DIM offset(2)      
57 v0(0) = b1 - b0
58 v0(1) = b2 - b0
59 v1(0) = b2 - b0
60 v1(1) = b2 - b0
61 offset(0) = offset(0) + a * v0(0) / 8 + b * v1(0) / 8
62 offset(1) = offset(1) + a * v0(1) / 8 + b * v1(1) / 8
63 offset(2) = offset(2) + a * v0(2) / 8 + b * v1(2) / 8
64 '
65 'setting up p0
66 '
67 p0.x = b0.x + offset(0)
68 p0.y = b0.y + offset(1)
69 p0.z = b0.z + offset(2)
70 '
71 'setting up p1
72 '
73 p1.x = b0.x + offset(0)
74 p1.y = b0.y + offset(1)
75 p1.z = b0.z + offset(2)
76 Return
77 '
78 '
79 '
80 '
81 '
82 '
83 ' ---------------------------------- przenoszenie ---------------------------------------------
84 '
85 '
86 *pickNput
87 p1temp = p1
88 p1temp.z = p1temp.z - valueToAdd
89 p0temp = p0
90 p0temp.z = p0temp.z  - valueToAdd
91 '
92 ' ruch
93 '
94 Mvs p0
95 DLY waitTime
96 '
97 ' picking up
98 '
99 ' ##otwarcie##
100 '
101 Mvs p0temp
102 DLY waitTime
103 '
104 ' ##zamkniecie##
105 '
106 Mvs p0
107 DLY waitTime
108 '
109 Mov j0
110 '
111 Mvs p1
112 DLY waitTime
113 '
114 ' releasing
115 '
116 Mvs p1temp
117 DLY waitTime
118 '
119 ' ## otwarcie ##
120 '
121 Mvs p1
122 Return
j0=(0.000,18.350,135.430,0.000,26.380,0.000)
p0=(393.820,-431.290,318.810,180.000,-0.160,180.000)(7,0)
p1=(693.820,468.800,318.810,180.000,-0.160,180.000)(7,0)
b0=(1.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000)(0,0)
b1=(0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000)(0,0)
b2=(0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000)(0,0)
