# 三角棋 (Triangular Nim)

<p align="center">
  <img src="/demo.png" width="500">
</p>

這是一個經典的組合遊戲「三角棋」的 Python 實作，內建一個會使用演算法尋找最佳解的 AI。遊戲的目標是避免拿走最後一個棋子。

This project is a Python implementation of the classic combinatorial game "Triangular Nim", featuring an AI opponent that uses algorithms to find the optimal move.

---

## 遊戲規則 (Game Rules)

1.  **棋盤**：遊戲在一個由 15 個點組成的三角形棋盤上進行。
2.  **走法**：玩家輪流在棋盤上畫一條直線，這條直線可以消除掉 1 到 3 個**連續相鄰**的點。
3.  **勝負**：這是一個「**輸棋賽局 (Misère Game)**」。根據規則，**拿走棋盤上最後一個棋子的玩家為輸家**。

## 功能特色 (Features)

*   **電腦 AI**：程式內建一個強大的 AI，它會透過遞迴演算法計算所有可能的遊戲狀態，找出最佳的走法。
*   **必勝策略**：此程式證明了在先手情況下，存在 9 種開局棋步可以保證 100% 獲勝 (對稱變化計為不同)。
*   **快取機制 (Cache)**：AI 在計算過程中會記錄下每個局面的勝負結果。透過 `--demo` 模式，可以將這些計算結果儲存成 `cache.json` 檔案，讓 AI 在之後的遊戲中能瞬間做出最佳決策，無需重複計算。

## 如何使用 (Usage)

### 1. 一般遊戲模式 (Play against the Computer)

直接執行程式，即可開始一場與電腦的對戰。輪到您時，請根據提示輸入 1 到 3 個棋子的編號。

```bash
python3 src/TriangularNim.py
```

*   **電腦先手**：在遊戲開始時，直接按下 `Enter` 鍵。
*   **玩家先手**：在遊戲開始時，輸入您想下的第一個棋步。

### 2. 產生 AI 快取 (Demo Mode)

使用 `--demo` 或 `-D` 旗標來執行。此模式會完整分析所有第一步的可能性，並將計算結果儲存到 `src/cache.json`。這是一個耗時的操作，但一旦完成，AI 在之後的遊戲中將能秒速回應。

```bash
python3 src/TriangularNim.py --demo
```

### 3. 分析第一手勝率 (Probability Mode)

使用 `--probability` 或 `-P` 旗標。此模式會計算並顯示所有合法第一步的獲勝機率，但**不會**儲存快取檔案。這有助於分析和理解遊戲的開局策略。

```bash
python3 src/TriangularNim.py --probability
```

---

## 必勝開局 (Winning Openings)

此程式證明了，先手情況下，以下 9 種開局棋步均存在必勝路徑：

- `0`
- `3`
- `4`
- `5`
- `7`
- `8`
- `10`
- `12`
- `14`


## 參考資料 (Reference)

*   [維基百科：三角棋](https://zh.wikipedia.org/wiki/%E4%B8%89%E8%A7%92%E6%A3%8B)

## 遊玩影片 (Gameplay Video)

[![Gameplay Video](https://img.youtube.com/vi/v9D_MbOy1Y4/0.jpg)](https://www.youtube.com/watch?v=v9D_MbOy1Y4)