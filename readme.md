# 54600-Series wave viewer

HP 54600-Series plotter emulator(Data receive and translation HP-GL to SVG)

HP 54600シリーズのハードコピーをSVG画像に変換するソフトウェアです。
python3.8環境で動作します。

動作確認済みハードウェア構成
- HP54645D MSO
- 54652B RS-232-C and parallel Interface

恐らくHP54600シリーズのMSOとRS-232-C Interface(54651A，54656A，54658A，54659B)でも動くと思われます。

## 本体設定
- RS-232C
- baudrate:19200
- plotter
- Factor:ON
- pen:2

# 取得例

![54600シリーズから取得したハードコピー](./svg_test.svg)