@echo off
echo ===================================================
echo Verificando dependencias do IRS Automator...
echo ===================================================

if not exist ".venv" (
    echo Criando ambiente virtual Python...
    py -m venv .venv
    if errorlevel 1 (
        echo Erro ao criar o ambiente virtual. Certifique-se que o Python esta instalado.
        pause
        exit /b 1
    )
)

echo Ativando ambiente virtual e verificando pacotes...
call .venv\Scripts\activate.bat

echo Instalando dependencias (Streamlit e Pandas)...
python -m pip install --upgrade pip
pip install streamlit pandas
if errorlevel 1 (
    echo Erro ao instalar dependencias.
    pause
    exit /b 1
)

echo ===================================================
echo Iniciando a Aplicacao...
echo ===================================================
streamlit run app.py
pause
