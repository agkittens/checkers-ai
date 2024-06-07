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
39 '
40 '
41 WHILE isDone = 0 
42  GoSub *pickNput
43  isDone = 1
44 WEnd
45 '
46 Mov j0
47 End
48 '
49 '
50 '
51 '
52 '
53 *pickNput
54 p1temp = p1
55 p1temp.z = p1temp.z - valueToAdd
56 p0temp = p0
57 p0temp.z = p0temp.z  - valueToAdd
58 '
59 ' ruch
60 '
61 Mvs p0
62 DLY waitTime
63 '
64 ' picking up
65 '
66 ' ##otwarcie##
67 '
68 Mvs p0temp
69 DLY waitTime
70 '
71 ' ##zamkniecie##
72 '
73 Mvs p0
74 DLY waitTime
75 '
76 Mov j0
77 '
78 Mvs p1
79 DLY waitTime
80 '
81 ' releasing
82 '
83 Mvs p1temp
84 DLY waitTime
85 '
86 ' ## otwarcie ##
87 '
88 Mvs p1
89 Return
j0=(0.000,18.350,135.430,0.000,26.380,0.000)
p0=(393.820,-431.290,318.810,180.000,-0.160,180.000)(7,0)
p1=(693.820,468.800,318.810,180.000,-0.160,180.000)(7,0)
