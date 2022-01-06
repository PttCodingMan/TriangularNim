# 三角棋 Triangular Nim
<img src="/demo.png" width="500">

這是三角棋[[1]]  
開始時共有 15 個圈圈，玩家可以畫一個直線，消掉一到三顆  
輪流消掉畫到最後一顆的人輸

此程式證明了有第一手有九種開局都存在必勝路徑，扣掉旋轉則為三種

This is Triangular Nim[[1]] game.  
There are 15 circles at the beginning, and the player can draw a straight line and eliminate one to three.  
Take turns to eliminate the person who draws the last one loses.  

This program proves that there is a winning path for all nine openings with the first move.  

以下是九種存在必勝路徑的第一手 
The following nine openings all has a winning path.
- 0
- 3
- 4
- 5
- 7
- 8
- 10
- 12
- 14

[1]: https://zh.wikipedia.org/wiki/%E4%B8%89%E8%A7%92%E6%A3%8B


## 用法 Usage
跟電腦玩  
Play with computer
```bash
python3 src/TriangularNim.py
```
計算必勝開局展示  
Count best move demo
```bash
python3 src/TriangularNim.py --demo
```

## Video 遊玩影片
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/YYnCp8yZIUw/0.jpg)](https://www.youtube.com/watch?v=YYnCp8yZIUw)
