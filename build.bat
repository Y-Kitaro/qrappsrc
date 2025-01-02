@echo off
setlocal

REM �r���h����X�N���v�g��
set SCRIPT_NAME=main.py
REM �R�s�[����t�@�C��
set RESOURCE_FILE=resource\qrcode_template.csv
REM �o�̓f�B���N�g����
set DIST_DIR=dist
REM �쐬����zip�t�@�C����
set ZIP_NAME=qrimg.zip

REM dist�f�B���N�g�����폜�i���݂���ꍇ�j
if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%"
)

REM zip�t�@�C�����폜�i���݂���ꍇ�j
if exist "%ZIP_NAME%" (
    del "%ZIP_NAME%"
)

call venv\Scripts\activate

REM PyInstaller�Ńr���h
pyinstaller -F -w "%SCRIPT_NAME%"

REM resource�t�@�C�������݂��邩�m�F
if not exist "%RESOURCE_FILE%" (
    echo �G���[: %RESOURCE_FILE% ��������܂���B
    pause
    exit /b 1
)

REM dist�f�B���N�g����resource�t�@�C�����R�s�[
if exist "%DIST_DIR%" (
    xcopy "%RESOURCE_FILE%" "%DIST_DIR%" /Y
) else (
    echo �G���[: %DIST_DIR% ��������܂���BPyInstaller�̃r���h�Ɏ��s�����\��������܂��B
    pause
    exit /b 1
)

REM dist�f�B���N�g����zip���k
powershell -Command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath '%ZIP_NAME%'"

REM �������b�Z�[�W
echo �r���h��zip���k�A�t�@�C���̃R�s�[���������܂����B
pause
endlocal