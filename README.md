# HAVA 公契查閱網站 v1.7 — Drawing Titles 三語圖則頁

## 這次更新

- 從左側目錄按「圖則及圖例」時，**直接顯示11張圖則的圖片畫廊**，不再打開 OCR 空白頁。
- 每張圖則卡片以**圖則上 Drawing Title 的英文原文**及**非官方繁體中文翻譯**為標題，不再用「圖則01」作標題。簡體模式顯示簡體、英文及繁體對照。
- 原 PDF 頁碼保留為小字，並保留放大、縮放、拖曳、手機雙指縮放、PDF 連結及原尺寸圖片。
- 從條款搜尋中點擊 PDF 77–87 頁，或使用舊連結 `?s=plans` / `?p=83`，會自動進入圖則頁／對應圖則。
- 圖則圖片沿用 v1.6：沒有 AI 重繪、沒有改動底圖位元組。

## 在 GitHub Desktop 更新

1. 解壓 ZIP。把 ZIP 內的 `index.html`、`app.js`、`style.css`、`service-worker.js`、`README.md`，連同 `plans/`、`data/` 等所有資料夾複製到本機 `hava-dmc` repository 根目錄，覆蓋同名檔案。
2. GitHub Desktop → Commit to main → Push origin。
3. 網站：`https://perryamos941-tech.github.io/hava-dmc/`。

## 準確性與法律提醒

英文 Drawing Title 由所附公契 PDF 第77–87頁圖則右側題名欄逐張抄錄；繁簡中文是非官方便利用語。原文圖則、界線與圖例均以正式登記公契為準。條文的 OCR 和中文初譯未完成法律校對。原始公契在發展商網站公開可讀，不等於容許把圖則重新複製及公開散播。正式部署前請確認有相應的複製與重刊權利。
