# Variant View
USDファイルのVariantを素早く確認できるOpenUSDを使用したツールです。
## 使用方法
OpenUSDがインストールされた環境で`variantview.py`を実行することで使用できます。  
引数として, USDファイルのパスを渡すことでそのファイルを開きます。  
※パスを指定しなかった場合は, サンプルデータを開きます。  
## 画面構成
左半分がVariant関連のリスト, 右側が3Dビューになっています。  
### Variant リスト
リストは2つ存在し, 左側にPrim, 右側に現在選択されているPrimのVariantが表示されます。  
PrimはVariant Setを持つもののみリスト化され, それ以外は無視されます。  
Variantのリストにはドロップダウンメニューが存在し, ここからVariantを変更することができます。  
※USDファイルにVariantの変更が保存されることはありません。あくまでプレビューを目的としており, 編集する目的では使用できません。
### 3Dビュー
usdviewとほぼ同一のものです。  
画面上部のメニューバーの`Render Mode`, `Background Color`, `Other View Settings`から各種ビューの設定を行うことができます。

## OpenUSDの動作確認環境
Windows 11 Pro 24H2, OpenUSD Version 25.05で動作を確認しています。  
OpenUSDのビルド時, 及び本ツールの作成にはPySide6を使用しています。  
また, OpenUSDのビルドの際に指定されるディレクトリパスが`PYTHONPATH`に追加されている必要があります。

## ライセンス情報
本ツールでは以下のApache License 2.0のソフトウェア/リソースを使用しています：
- OpenUSD（一部のコンポーネント）
  - Copyright © Pixar Animation Studios.
  - Apache License 2.0の下で使用
  - https://github.com/PixarAnimationStudios/OpenUSD
- Google Fonts（アイコン）
  - Copyright © Google LLC
  - Apache License 2.0の下で使用
  - [https://fonts.google.com/](https://fonts.google.com/)  

Apache License 2.0の全文は[こちら](https://www.apache.org/licenses/LICENSE-2.0)でご覧いただけます。

本ツールでは以下のLGPLv3のライブラリを使用しています：
- PySide6
  - Copyright © The Qt Company Ltd.
  - LGPLv3ライセンスの下で使用
  - [https://doc.qt.io/qtforpython-6/](https://doc.qt.io/qtforpython-6/)

LGPLv3ライセンスの全文は[こちら](https://www.gnu.org/licenses/lgpl-3.0.html)でご覧いただけます。