# HAVA 公契查閱網站 v1.6（非官方）

## GitHub Pages 上載方法

1. 將本 ZIP 內的 **所有檔案及資料夾**（包含 `plans/` 和 `data/`）放在 GitHub repository `hava-dmc` 的根目錄。
2. 使用 GitHub Desktop Commit，再按 Push origin。
3. GitHub → Settings → Pages → Deploy from a branch → `main` → `/(root)`。
4. 開啟 `https://perryamos941-tech.github.io/hava-dmc/`，點「圖則查閱」。

## v1.6 新增

- 新增專用的圖則查閱頁：11張，對應 PDF 第77至87頁；第75–76頁屬簽署／蓋章，不屬圖則。
- 縮圖使用 WebP，原尺寸使用從公契 PDF 無重新壓縮抽取的 **JPEG 內嵌影像**（2478×1752 像素）。用 JPEG 是因為原公契內嵌影像本來就是 JPEG；不作 PNG 轉換可保留相同原始影像位元組，不會引入新的影像重壓縮。
- 放大、縮小、移動、手機雙指縮放、上一張／下一張、開新分頁及 PDF 來源連結。
- 保留 v1.5 的公契搜尋／三語初譯功能，不包含先前刪除的全文機器翻譯工作台。
- 原公契 PDF 不儲存在此 repository；使用者提供的來源為 `https://www.thehava.hk/upload/dmc/HAVA_DMC_dd_20251125_Reg20251209.pdf`。

## 使用及版權提醒

網站並非官方翻譯。英文 OCR 及中文條款內容仍屬未經逐條核對的初稿；請依正式公契判斷權利義務。

**公契可以在官網公開閱讀，不等於圖則可以自由複製及重新發布。** 此 ZIP 已包含11張從原 PDF 抽取的圖則圖片，正式公開上傳之前請先確認是否具有適當的複製及再發布權限。

圖片沒有經 AI 改圖、補線或重繪；只添加非官方頁碼索引，圖面本身仍需以正式登記公契核對。

## 檔案位置

- `index.html` 網站首頁
- `app.js` 搜尋與圖則瀏覽互動
- `style.css` 桌面／手機樣式
- `plans/plan-77.jpg` ... `plans/plan-87.jpg` 原圖
- `plans/thumb-77.webp` ... `plans/thumb-87.webp` 縮圖
- `data/content.js` 現有公契搜尋資料

## 備註

檔案測試只涵蓋指定生成版本，不保證 HAVA 外部 PDF 服務會接受所有來源的連結或在手機 PDF 閱讀器中正確定位頁碼。
