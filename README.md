# HAVA 公契非官方三語查閱網站 — GitHub Pages v1.5

本專案是一個可部署到 GitHub Pages 的靜態查閱網站（繁體中文 / 简体中文 / English）。

## 內容

- 章節目錄、關鍵字搜尋、條文索引與頁碼定位。
- 既有第1至80條及其他部分附表的 AI 中文**初譯**，不代表已完成逐句、全頁翻譯。
- 英文 OCR 未經逐字校對；份數表、圖則、簽署頁不可依靠 OCR。
- 連結到 HAVA 官網 PDF，不在儲存庫放置原 PDF。
- 已移除 V2 全文機器初譯工作台。

**原始公契 PDF（使用者提供的外部網址）：**
https://www.thehava.hk/upload/dmc/HAVA_DMC_dd_20251125_Reg20251209.pdf

**重要：** 透過自動工具嘗試讀取上述來源時得到 403，因此未獨立核實其可用性及是否與此前上傳的87頁 PDF 完全一致。網站只作連結，並不代理或下載該來源。部分手機 PDF 檢視器可能無法直接跳到 `#page=...` 指定頁，遇到此情況請按畫面提示手動轉到所標示的 PDF 頁碼。

## 法律及品質提醒

- 本網站並非官方翻譯或法律意見，亦非發展商、管理處、土地註冊處的官方服務。
- **公開能看見 PDF 不代表取得再發布、OCR 轉錄、翻譯或索引資料的授權。** 在公開推廣或再發布之前，請核實權利及條款；免責聲明不能取代授權。
- 所有中文初譯未經法律專業審核，內容可能有缺漏及概括翻譯；應以適用正式登記英文公契及有效修訂文件為準。
- 此試用版採用 `noindex`，減少未核實譯文出現在搜尋引擎，但**並不是存取控制**；凡部署在 GitHub Pages 的內容均屬公開可存取。

## GitHub Desktop 上傳（免指令）

1. 將本 ZIP 解壓，確保 `index.html` 位於資料夾根目錄。
2. 在 GitHub Desktop 選 File → Add local repository；如果不是 Git repository，選 Create a Repository，儲存位置選這個資料夾。
3. 建立後，在 Changes 輸入 commit 訊息，按 Commit to main。
4. 選 Publish repository（或 Push origin，視乎狀態），建立對應 GitHub repository。
5. 在 GitHub 網站開啟 repository → Settings → Pages。
6. Build and deployment → Source 選 Deploy from a branch；Branch 選 `main`；Folder 選 `/(root)`；Save。
7. Pages 區域會出現正式網址。常見形式是 `https://<username>.github.io/<repo>/`。

注意：不要把 ZIP 本身作為網站唯一檔案上傳 GitHub。要把解壓後的檔案和資料夾放在 repository 根目錄。

## 檔案

- `index.html` — 首頁
- `app.js`, `style.css`, `data/content.js` — 網站程式及索引資料
- `assets/icon.svg`, `manifest.webmanifest` — 圖示及網頁設定
- `service-worker.js` — 頁面快取；新版本使用新的 cache key
- `.nojekyll` — 防止 GitHub Pages 特別處理靜態檔案
- **沒有** `original/source.pdf`

## 手動測試

1. 搜尋「管理費」，應該有非零結果；可搜尋 `Clause 47`、`業主委員會`。
2. 按「閱讀／查看」，確認標題和繁簡切換正常。
3. 按「PDF ↗」或首頁「開啟原始公契 PDF」，確認跳轉到上面的 HAVA 官網 URL。
4. 以 iPhone / Android 瀏覽器開啟部署網址，確認可以搜尋及切換語言。
