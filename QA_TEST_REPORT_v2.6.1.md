# HAVA v2.6.1 驗收紀錄（2026-10-28）

## 目的與改動

本次為穩定性及資料一致性小修正，**不是重新翻譯或更改公契**。繁體中文 DMC 來自使用者提供的98頁中文文件，英語正式核對來源仍是 HAVA 官網英文登記公契。簡體中文仍是繁中轉換版。網站已知五處中英差異（8(c)、8(e)、10、13(a)、62）原樣保留；不能視作其他條款已完成逐句核證。

主要修正：
1. 所有五頁載入的本地 JS/CSS 查詢版本 `?v=2.6.1`；修正首頁先前使用 `2.5.7` 的情況。
2. Service Worker 新快取命名空間，HTML/JS/CSS/JSON 網絡優先，不再於 JavaScript 資源載入失敗時返回 HTML。
3. 售樓資料 `sales.json` / `sales.js` 及品質資料 `quality.json` / `quality.js` 保持值完全相同，並新增 `scripts/sync_release_data.py` 及發布自動檢查。
4. 修正品質頁 footer、站點版本、PWA 名稱。

## 實際檢查結果

- PASS：`scripts/verify_release.py`。單位594組／設備788筆／機電2,950筆；5個機電版本修訂格、11筆抽樣設備核對記錄符合現有資料核對規則。
- PASS：`scripts/verify_v261.py`。5頁程式載入版本一致； JSON 與 JS 包裝器完全一致；來源URL、欄位及圖片存在性； DMC 85個單元、五處紅字提示；不公開中文PDF連結。
- PASS：Node.js 語法檢查（app.js、assets/units.js、service-worker.js、data/content.js、data/sales.js、data/quality.js）。
- PASS：Chromium 模擬320、390、430、768、1366px × 5頁，共25組，無執行階段 JavaScript 錯誤或水平溢出；「管理費」搜尋有結果、單位頁顯示、中文全文紅字提示正常。
- PASS：舊版更新包對照：`data/content.js`、中文來源 manifest、五處差異資料、單位程式 `assets/units.js` **位元組完全相同**。舊版162個 `brochure/` 和 `plans/` 圖片檔案逐一雜湊相同； `sales.json` 的594組單位資料、788筆設備及2,950筆機電列表與 v2.6 完全相同。
- PASS：ZIP完整性及所有檔案清單。

## 未能確認／仍有的限制

- **Service Worker 實際離線使用切換**：瀏覽器測試環境禁止存取本機 HTTP 伺服器，無法完成真實 SW 端到端離線測試。已完成 JavaScript 語法、程式分支及快取規則靜態核查，不能冒稱離線行為全面驗收。
- **GitHub Pages 部署**：未直接推送，網站真實 URL 與實機 Samsung/iPhone 測試尚未驗收。
- **法律語義**：繁中與英文公契已確認部分差異，全文仍未完成獨立逐句法律核證，須以正式登記英文公契為準。
- **圖則重刊**：須確認在公開站重新託管的使用權限。
