@echo off
echo =============================================
echo  🌍 INSTALADOR UNIVERSAL – DJANGO + SQLITE
echo =============================================

REM 1. Verificar Python
echo Verificando Python...
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python no está instalado.
    pause
    exit /b
)

REM 2. Crear entorno virtual
echo ¿Deseas crear el entorno virtual (venv)? (s/n)
set /p crear_venv=
IF /I "%crear_venv%"=="s" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM 3. Activar entorno virtual (Windows)
if exist venv\Scripts\activate (
    call venv\Scripts\activate
)

REM 4. Activar entorno virtual (Mac/Linux)
if exist venv/bin/activate (
    call venv/bin/activate
)

REM 5. Instalar dependencias
echo Instalando dependencias desde requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

REM 6. Aplicar migraciones (SQLite)
echo Ejecutando migraciones en SQLite...
python manage.py migrate

echo =============================================
echo  ✔ Instalación completa con éxito.
echo  ✔ Base de datos SQLite lista.
echo =============================================

echo ¿Deseas iniciar el servidor Django ahora? (s/n)
set /p runserver=
IF /I "%runserver%"=="s" (
    python manage.py runserver
)

pause
