# CP3 SVG 圖示

`260827 - CP3/web/img` 底下視訊（video）、音訊（audio）、燈光（light）圖示的 SVG 重繪版。
每個 SVG 與原本的 PNG 同資料夾、同檔名，只有副檔名不同，例如
`video/in/21_hdmi.png` 對應 `video/in/21_hdmi.svg`。

打開 `preview.html` 可以並排比對新舊圖示（大圖是新 SVG，右下小圖是原 PNG）。

## 規格

| 項目 | 設定 |
| --- | --- |
| 繪圖網格 | 64 × 64，`viewBox="-8 -8 80 80"`（四周留 8 單位，視覺大小與原 PNG 相同） |
| 預設尺寸 | `width="160" height="160"`（與原 PNG 相同） |
| 線條 | `stroke-width="3.5"`、圓角端點與轉角 |
| 顏色 | `color="#fff"` + `currentColor`，預設白色 |

`light/color_stage.svg` 是唯一的彩色圖示（色環）。

## 使用方式

**直接替換 `<img>`**：把 `.png` 改成 `.svg` 就好，預設是白色，跟原圖一樣。

```html
<img src="img/video/in/21_hdmi.svg">
```

**內嵌 SVG 並用 CSS 改顏色**：內嵌時 CSS 的 `color` 會覆蓋預設白色。

```css
.btn svg { color: #39f; }
.btn.active svg { color: #fff; }
```

**當作遮罩上色**（用 `<img>` 也能隨狀態換色）：

```css
.icon {
  width: 64px; height: 64px;
  background-color: currentColor;
  -webkit-mask: url(img/audio/in/21_xlr.svg) center / contain no-repeat;
          mask: url(img/audio/in/21_xlr.svg) center / contain no-repeat;
}
```

## 重新產生

所有圖示都由 `tools/build_icons.py` 產生，共用的圖形（HDMI、投影機、錄影機…）只定義一次。
要整體調整線寬、留白或顏色時，改腳本後執行：

```sh
python3 tools/build_icons.py
```

會覆寫全部 SVG 和 `preview.html`。直接手動修改 SVG 檔也可以，但下次執行腳本時會被蓋掉。

## 跟原圖意思不同的地方

大部分圖示都照原本的意思重繪，下列幾個有調整，請確認：

- `video/in/33_appletv`、`audio/in/43_appletv`：拿掉 Apple 商標，改成標「TV」的串流盒。
- `video/in/34_google_cast`：原圖是 Chrome 標誌，改成通用的投放（Cast）圖示。
- `video/in/54_multiview`：四宮格改成分割成四格的螢幕。
- `video/in/61_livestream`、`video/out/23_livestream`：「Live」字樣上方加了廣播訊號。
- `audio/out/13_subwoofer`：原圖是兩路喇叭，改成單一大單體的重低音音箱。
- `audio/out/22_echo`：原圖像 Wi‑Fi 符號，改成逐漸變淡的聲波。
- `audio/out/81_recorder_audio`：音符旁加了錄音圓點，跟 `41_music` 區分。
- `light/basic_dim`：原圖是星星，改成半亮的太陽，跟全開、全關同一組。
- `light/stage_spotlight`：兩盞交叉的聚光燈改成一盞照向地面的聚光燈。
- `light/0_default.svg`：原本是黑色實心方塊，改成同風格的白色線條方塊。
