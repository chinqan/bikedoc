# 小鐵人 5/24 台3線車訓 — 活動文件專案

> 桃園小鐵人探險隊 2026 年 5/24（日）台3線車訓活動的文件庫，包含主辦單位與參加人員雙版本行前資料、路線檔案與一個簡單的入口網頁。

---

## 🌐 線上瀏覽

開啟 `index.html` 為入口頁，提供兩個進入點：

- 📋 **主辦單位行前注意事項** — `organizer.html`
- 🚴 **參加人員行前手冊** — `participant.html`

部署到 GitHub Pages 或任意靜態伺服器即可線上瀏覽。

---

## 📁 專案結構

```
bikedoc/
├── index.html                      # 入口頁（兩張卡片連到主辦／參加版）
├── organizer.html                  # 主辦版網頁（由 md 產生）
├── participant.html                # 參加者版網頁（由 md 產生）
│
├── 行前注意事項-主辦單位.md         # 主辦版內容源（編輯這份）
├── 小鐵人－台3線騎車活動.md         # 參加者版內容源（編輯這份）
├── 小鐵人－台3線騎車活動.pdf        # 參加者版 PDF 輸出
│
├── 小鐵人台三線騎行會前會-會議記錄.md   # 會前會原始記錄（5 張附件圖出處）
├── 小鐵人台三線騎行會前會-會議記錄.pdf
├── 小鐵人台三線騎行會前會-會議記錄.txt
│
├── 五月浪漫台三線車訓報名表.xlsx    # Google Form 報名彙整（含便當訂單）
├── 路線圖.xlsx                     # 路線初版規劃
│
├── 台3線車訓路線.gpx               # ★ GPX 軌跡檔（OpenRouteService 生成）
├── 台3線車訓路線-MyMaps匯入.csv    # ★ 9 點 WKT/lat-lng（My Maps 匯入用）
│
├── 飛騎.png                        # ★ 飛騎 Velodash 路線 QR Code
├── 圖1.jpg ～ 圖5.jpg               # ★ 5 張關鍵路口／施工／折返照片
├── dm1.png, dm2.png                # 活動 DM 設計檔
├── image.png, top_left_style_crop.png
│
├── md2pdf.py                       # Markdown → PDF 工具（中文友善）
└── README.md                       # 本文件
```

`★` 標示者為網頁會引用的靜態資源，部署時須一併上傳。

---

## 🎯 活動概要

| 項目 | 內容 |
|---|---|
| 活動名稱 | 小鐵人－台3線車訓 |
| 日期 | 2026/5/24（日） |
| 集合 | 07:00 龍潭大池．貴族世家右側停車場 |
| 出發／返抵 | 07:30 出發、預計 11:30 返抵、12:00 慶生 |
| 總里程 | 約 41 km（OpenRouteService 實測 42 km、爬升 178 m） |
| 路線 | 龍潭大池 → 7-11 騰達門市（折返）→ 龍潭大池 |
| 報名人數 | 41 人（14 個家庭，5 組 + 機動 + 補給車 2 台） |

### 路線節點

| 編號 | 類型 | 名稱 | 里程 |
|:---:|---|---|---:|
| 1 | 起點 | 龍潭大池 | 0 km |
| 2 | 迴轉 | 號誌燈迴轉點 | 0.3 km |
| 3 | 🚦 交管 | 大北坑 | 1 km |
| 4 | 🚦 交管 | 內環山 | 8.3 km |
| 5 | 🥤 補給 1 | 國道三號路橋下 | 9 km |
| 6 | 🔄 折返 | 7-11 騰達門市 | 20 km |
| 7 | 🥤 補給 2 | 濟世宮 | 28.5 km |
| 8 | 🥤 補給 3 | 中油正新站 | 35 km |
| 9 | 終點 | 龍潭大池 | 41 km |

---

## 🛠️ 開發 / 維護流程

### 編輯文件

1. **內容只改 `.md`**：
   - 主辦版改 `行前注意事項-主辦單位.md`
   - 參加版改 `小鐵人－台3線騎車活動.md`
2. **不要直接編輯 `.html`** — 會在下次重建時被覆蓋。

### 重新產生 HTML

使用以下 Python script（依賴 `markdown` 套件）：

```bash
pip install markdown   # 一次性安裝
python3 build.py       # 若已封裝；否則用對話中的 inline script
```

實際的建置邏輯在歷次對話中以 inline Python 執行，包含：

- 使用 `markdown` 套件解析 `.md` → HTML
- 啟用 extensions: `tables`, `fenced_code`, `attr_list`, `md_in_html`, `sane_lists`
- 注入共用 CSS（主辦版藍色主題、參加版綠色主題）
- 套用響應式設計、checklist 互動樣式、details 摺疊圖片樣式

### 產生 PDF

```bash
python3 md2pdf.py 行前注意事項-主辦單位.md
# 或
python3 md2pdf.py 小鐵人－台3線騎車活動.md
```

底層使用 `npx md-to-pdf` + chromium 渲染，支援中文（Noto Sans TC）、表格、圖片嵌入。

### 重新產生路線檔

#### GPX（OpenRouteService 自行車路徑）

需要 `ORS_API_KEY` 環境變數（已在 `~/.zshrc` 中設置）。

對 9 個座標點呼叫 `cycling-regular` profile，輸出 GPX。詳見對話歷史中的 inline script。

#### CSV（My Maps 匯入用）

手動編輯 `台3線車訓路線-MyMaps匯入.csv` 或從會議紀錄複製座標即可。

---

## 📝 內容架構

### 主辦版（organizer.html）

1. 活動時間與集合
2. 停車場位置提醒
3. 分組名單（押隊紅字標示）
4. 各組負責事項（領隊任務 + 工作分配表）
5. 路線地圖與導航（飛騎 + My Maps）
6. 雨天備案
7. **前一晚 LINE 群組要發送的訊息**（4 則可複製訊息範本）
8. 工作人員行前確認清單（5/23 晚 Check）
9. 附件：便當訂單明細（14 家庭 / 38 份）

### 參加者版（participant.html）

1. 活動基本資訊
2. 集合與出發時間
3. 騎乘路線總覽（含五大原則卡片）
4. 分組名單
5. 路線地圖與導航（飛騎主要 / My Maps 備援並排）
6. 沿途補給時間
7. 重要路線節點說明（含可摺疊圖片）
8. 補給車說明
9. 安全與團騎規則（含可摺疊施工路段照片）
10. 雨天備案
11. 途中棄賽或身體不適處理
12. 參加者自備物品（互動 checklist）
13. 單車檢查建議（互動 checklist）
14. 出發前最後檢查（互動 checklist）

---

## 🎨 設計約定

- **主辦版**：藍色主題（`#2980b9` / `#1a5276`）
- **參加版**：綠色主題（`#27ae60` / `#186a3b`）
- **押隊標示**：紅色 badge（`#c0392b` / `#fdecea`）
- **字型**：Noto Sans TC（Google Fonts CDN）
- **響應式**：桌面 max-width 1080px，700px 以下自動切換手機版（地圖、map-row、checklist 重新排版）
- **可互動元件**：
  - `<details>` 折疊式圖片
  - `<input type="checkbox">` checklist（hover、勾選反饋）
  - Google My Maps `<iframe>` 嵌入預覽

---

## 🔗 外部資源

| 資源 | URL／路徑 |
|---|---|
| 飛騎路線 Deep Link | <https://velodash.page.link/4ZZQ> |
| iOS App | <https://apps.apple.com/us/app/velodash-cycle-together/id1329905651> |
| Android App | <https://play.google.com/store/apps/details?id=co.velodash.app> |
| Google My Maps | <https://www.google.com/maps/d/u/0/edit?mid=1WwdglPGRHG5MGx53j-zqjOfqWtP8Exc> |

---

## 👥 工作分配

| 角色 | 負責人 |
|---|---|
| 總教練（帶操） | — |
| 領隊 | （見分組名單之領騎欄） |
| 補給車 | 羊來了、金錢豹 |
| 特殊關照（黑豆） | 紅豆（同組） |
| 便當／餐廳 | 高鐵 |
| 慶生蛋糕 | 荔枝 |
| 報名表／拍照 | 金錢豹（小掌櫃：開心果） |
| 補給品採買 | 鱸鰻 |
| 行前說明 | 翼龍 |
| 分組規劃 | 熊鷹／瑪麗貓 |
| 設計活動貼紙 | 紅豆 |

---

## 📜 版本記錄

主要更新請見 `git log`。最近幾次重大調整：

- 主辦版章節重組、新增 LINE 訊息範本節
- 兩份文件嵌入會議紀錄 5 張附件圖（路口／施工／折返）
- 參加者版改用表格與互動 checklist 精簡內容
- 加入 GPX、My Maps CSV、入口頁 `index.html`

---

🚴 **安全第一、互相照應、順利完騎！**
