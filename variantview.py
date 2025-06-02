import os
import sys
import window

def main():
    # サンプルのUSDファイルを指定(ファイルを指定されなかった場合に開く)
    usd_file_path = os.path.abspath('data/testCube.usdz')

    # 引数で指定されたUSDファイルに変更
    if len(sys.argv) > 1:
        # 引数を取得
        file_path = os.path.abspath(sys.argv[1])
        # 絶対パスに変換し, 拡張子を取得
        _, extension = os.path.splitext(file_path)
        # 拡張子のピリオド以外を小文字にする
        extension = extension[1:].lower()
        usd_extensions = ['usd', 'usda', 'usdc', 'usdc', 'usdz']
        # USDファイルの拡張子と一致するか確認
        if extension in usd_extensions:
            usd_file_path = file_path

    window.set_usd_file_path(usd_file_path)
    window.create_window()

if __name__ == '__main__':
    main()