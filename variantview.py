import os
import sys
import window

def main():
    # サンプルのUSDファイルを指定
    usd_file_path = os.path.abspath('C:/houdini/_test/test_56_animal/usd/animal.usd')
    # USD_FILE_PATH = str(os.path.abspath('data/shaderBall.usd'))
    # USD_FILE_PATH = str(os.path.abspath('C:/usd/Kitchen_set/Kitchen_set.usd'))
    # USD_FILE_PATH = 'C:/houdini/_test/test_56_animal/usd/animal.usd'

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
        else:
            print('The specified file is not a USD file. Opening sample USD file instead.')
    else:
        print('Opening sample USD file since no USD file was specified.')

    # メイン処理のエントリーポイント
    window.create_window(usd_file_path)

if __name__ == '__main__':
    main()