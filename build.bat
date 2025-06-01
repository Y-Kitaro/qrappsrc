@echo off
setlocal

REM --- �ݒ荀�� ---
REM ���z���̃p�X
set VENV_PATH=venv
REM PyInstaller�̎��s�t�@�C���p�X
set PYINSTALLER_CMD=%VENV_PATH%\Scripts\pyinstaller.exe
REM �r���h����Python�X�N���v�g
set SCRIPT_NAME=main.py
REM �A�v���P�[�V������ (���s�t�@�C�����Əo�̓t�H���_���ɂȂ�)
set APP_NAME=QRApp
REM React�̃r���h���ʕ�������f�B���N�g��
set WEB_UI_DIR=webui\dist
REM ���̑��̃��\�[�X�t�@�C��������f�B���N�g��
set RESOURCE_DIR=resource

REM --- �r���h���� ---

echo.
echo =================================
echo  React + Pywebview �A�v���̃r���h���J�n���܂�
echo =================================
echo.

REM �O��̃r���h���ʂ��N���[���A�b�v
echo --- �O��̃r���h���ʂ��폜���Ă��܂�...
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

REM React�A�v���̃r���h
echo --- React�A�v�����r���h���Ă��܂�...
cd webui
call npm run build
cd ..
if %errorlevel% neq 0 (
    echo React�̃r���h�Ɏ��s���܂����B
    pause
    exit /b 1
)
echo.


echo --- PyInstaller��EXE���r���h���Ă��܂�...

REM PyInstaller�̎��s
%PYINSTALLER_CMD% ^
    --name %APP_NAME% ^
    --onefile ^
    --windowed ^
    --clean ^
    --add-binary "venv/Lib/site-packages/webview/lib;webview/lib" ^
    %SCRIPT_NAME%

REM �r���h�����`�F�b�N
if %errorlevel% neq 0 (
    echo.
    echo !!! PyInstaller�̃r���h�Ɏ��s���܂����B
    pause
    exit /b 1
)
echo --- �r���h������Ɋ������܂����B
echo.

echo --- �֘A�t�@�C���̃R�s�[ ---

if exist "dist\" (
    echo --- Web UI �t�@�C�����R�s�[���Ă��܂�...
    xcopy "%WEB_UI_DIR%" "dist\webui\" /E /I /Y

    echo --- ���\�[�X�t�@�C�����R�s�[���Ă��܂�...
    xcopy "%RESOURCE_DIR%" "dist\resource\" /E /I /Y

) else (
    echo �G���[: dist\ ��������܂���B
    pause
    exit /b 1
)

echo --- �o�̓t�H���_��ZIP�t�@�C���Ɉ��k���Ă��܂�...

REM dist�f�B���N�g�����̃A�v���P�[�V�����t�H���_��zip���k
powershell -Command "Compress-Archive -Path 'dist' -DestinationPath '%APP_NAME%.zip' -Force"

if %errorlevel% neq 0 (
    echo.
    echo !!! ZIP���k�Ɏ��s���܂����B
    pause
    exit /b 1
)
echo --- ZIP���k���������܂���: %APP_NAME%.zip
echo.

echo =================================
echo  ���ׂĂ̏������������܂����B
echo =================================
echo.

pause
endlocal