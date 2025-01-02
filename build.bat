@echo off
setlocal

REM ビルドするスクリプト名
set SCRIPT_NAME=main.py
REM コピーするファイル
set RESOURCE_FILE=resource\qrcode_template.csv
REM 出力ディレクトリ名
set DIST_DIR=dist
REM 作成するzipファイル名
set ZIP_NAME=qrimg.zip

REM distディレクトリを削除（存在する場合）
if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%"
)

REM zipファイルを削除（存在する場合）
if exist "%ZIP_NAME%" (
    del "%ZIP_NAME%"
)

call venv\Scripts\activate

REM PyInstallerでビルド
pyinstaller -F -w "%SCRIPT_NAME%"

REM resourceファイルが存在するか確認
if not exist "%RESOURCE_FILE%" (
    echo エラー: %RESOURCE_FILE% が見つかりません。
    pause
    exit /b 1
)

REM distディレクトリにresourceファイルをコピー
if exist "%DIST_DIR%" (
    xcopy "%RESOURCE_FILE%" "%DIST_DIR%" /Y
) else (
    echo エラー: %DIST_DIR% が見つかりません。PyInstallerのビルドに失敗した可能性があります。
    pause
    exit /b 1
)

REM distディレクトリをzip圧縮
powershell -Command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath '%ZIP_NAME%'"

REM 完了メッセージ
echo ビルドとzip圧縮、ファイルのコピーが完了しました。
pause
endlocal