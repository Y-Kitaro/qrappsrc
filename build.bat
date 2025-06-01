@echo off
setlocal

REM --- 設定項目 ---
REM 仮想環境のパス
set VENV_PATH=venv
REM PyInstallerの実行ファイルパス
set PYINSTALLER_CMD=%VENV_PATH%\Scripts\pyinstaller.exe
REM ビルドするPythonスクリプト
set SCRIPT_NAME=main.py
REM アプリケーション名 (実行ファイル名と出力フォルダ名になる)
set APP_NAME=QRApp
REM Reactのビルド成果物があるディレクトリ
set WEB_UI_DIR=webui\dist
REM その他のリソースファイルがあるディレクトリ
set RESOURCE_DIR=resource

REM --- ビルド処理 ---

echo.
echo =================================
echo  React + Pywebview アプリのビルドを開始します
echo =================================
echo.

REM 前回のビルド結果をクリーンアップ
echo --- 前回のビルド結果を削除しています...
if exist "dist\" (
    rmdir /s /q "dist\"
)
if exist "build" (
    rmdir /s /q "build"
)
if exist "%APP_NAME%.zip" (
    del "%APP_NAME%.zip"
)
echo.

REM Reactアプリのビルド
echo --- Reactアプリをビルドしています...
cd webui
call npm run build
cd ..
if %errorlevel% neq 0 (
    echo Reactのビルドに失敗しました。
    pause
    exit /b 1
)
echo.


echo --- PyInstallerでEXEをビルドしています...

REM PyInstallerの実行
%PYINSTALLER_CMD% ^
    --name %APP_NAME% ^
    --onefile ^
    --windowed ^
    --clean ^
    --add-binary "venv/Lib/site-packages/webview/lib;webview/lib" ^
    %SCRIPT_NAME%

REM ビルド成功チェック
if %errorlevel% neq 0 (
    echo.
    echo !!! PyInstallerのビルドに失敗しました。
    pause
    exit /b 1
)
echo --- ビルドが正常に完了しました。
echo.

echo --- 関連ファイルのコピー ---

if exist "dist\" (
    echo --- Web UI ファイルをコピーしています...
    xcopy "%WEB_UI_DIR%" "dist\webui\" /E /I /Y

    echo --- リソースファイルをコピーしています...
    xcopy "%RESOURCE_DIR%" "dist\resource\" /E /I /Y

) else (
    echo エラー: dist\ が見つかりません。
    pause
    exit /b 1
)

echo --- 出力フォルダをZIPファイルに圧縮しています...

REM distディレクトリ内のアプリケーションフォルダをzip圧縮
powershell -Command "Compress-Archive -Path 'dist' -DestinationPath '%APP_NAME%.zip' -Force"

if %errorlevel% neq 0 (
    echo.
    echo !!! ZIP圧縮に失敗しました。
    pause
    exit /b 1
)
echo --- ZIP圧縮が完了しました: %APP_NAME%.zip
echo.

echo =================================
echo  すべての処理が完了しました。
echo =================================
echo.

pause
endlocal