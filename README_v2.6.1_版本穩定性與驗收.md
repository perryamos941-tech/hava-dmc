# HAVA v2.6.1 — 穩定性及資料一致性修正版

本版本是 v2.6 的小修正，沒有改動你提供的繁體中文 DMC 正文，亦沒有改動原有英文 OCR、簡體轉換正文、單位面積、788筆電器適用資料、2950筆機電資料及圖片。

## 修改
- 網站 HTML/JS/CSS 的資源版本統一為 `2.6.1`；修正首頁曾使用 `?v=2.5.7` 的情況。
- `data/release_manifest.json` 記錄站點版本及來源；`sales.json`、`quality.json` 反映同一版本。
- `sales.js` 及 `quality.js` 由相應 JSON 重建，不再容許 JS 及 JSON 值不一致。
- Service Worker：更新 cache namespace；所有 HTML、JS、CSS、JSON 使用網絡優先策略；離線時禁止用 HTML 假扮 JS；已快取圖則仍可在離線時查閱。
- 修正資料品質頁 footer 的過時 `v2.5.7` 顯示及站點 PWA 名稱。
- `scripts/verify_v261.py` 會核實核心數據、中文來源指紋、英文公契 PDF URL、五處中英差異、所有資源修訂版本、資源存在性，以及 JSON/JS 同步。

## 資料來源及限制
- 繁體中文 DMC 取自你提供的98頁中文文件；**不是網站的 AI 譯文**。
- 簡中由繁中轉換，非獨立公契。
- 紅字標示五處目前已確認差異：8(c)、8(e)、10、13(a)、62。**其他條款未完成逐句英中核證**。
- 所有 DMC PDF 按鈕均指向 HAVA 官網英文登記公契。
- 2026年售樓說明書索引及機電資料僅供核對，不是業主單位實地驗收。
- 官方文件可公開閱覽，不等於自動授權本站轉載圖則及正文，公開前應確認使用權限。

## 測試
在網站根目錄執行：
```
python scripts/verify_release.py
python scripts/verify_v261.py
```
要修改售樓資料 JSON，完成後執行 `python scripts/sync_release_data.py`，然後重跑驗收。來源及數值未經覆核切勿任意修改。

## 更新 GitHub
將這個 ZIP 解壓後的全部檔案放入現有 `hava-dmc` Repo 根目錄，替換舊檔案，再使用 GitHub Desktop Commit → Push。GitHub Pages 的路徑和分支設定不用改。GitHub 上仍保留舊 Commit，可還原。
