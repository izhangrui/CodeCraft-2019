# CodeCraft-2019
训练赛的时候调参有到过1000，不过初赛的时候地图旋转了，一时间没想到办法，就完全没法用。
现在改了一下随便试了个参数初赛两个地图要跑4000多。


大致思路就是建立正方形地图，遍历得到路径。遍历的时候以终点为导向，确定每次遍历的方向（上下左右）


[[164  60  10 121  61  27 133 143 131   8  33 109]
 [141 147 110 106  19  88  76  15  94  31  28  62]
 [102 153 156  98 150 160 104  81  41  58  21 144]
 [ 47 158 120  83 103 119  64  55 146 124  93  44]
 [128   6   2  56  78  51  40  86  16 129 116 145]
 [163 107  30  42  95  29 122 125 130 113 165  77]
 [139  34  36 162 126  59 136  -1  67  17  53  70]
 [ 97   4 134  22  73  18  43  25  84  75  68  23]
 [ 46   1  57 114  69  52  80 127  32 135 157 101]
 [ 79  89 161  48  -1 115 123 154 118 112  74 149]
 [ 65 100   3  50 132 152  87 148  63  26 155 159]
 [ 72  91 140  13  14  92  45  38  96  66  49  85]
 [117 138  20 105 108  24  71  37 151   9   7 111]
 [  0  99  90  54 142  12  11 137  35  39   5  82]]


代码写得比较烂....不太会面向对象，里面数据都是用列表或者numpy表示的，看起来可能有点头疼...