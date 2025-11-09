## Crear el virtualenv (.venv)

1) Crear y activar un virtualenv:
   python3 -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows PowerShell

2) Actualizar herramientas de empaquetado:
   pip install --upgrade pip setuptools wheel

3) Instalar dependencias:
   pip install -r requirements.txt


## Eliminar el virtualenv (.venv)

- Si el entorno está activo, primero desactívalo:
  - macOS / Linux / Windows (venv): deactivate
  - conda: conda deactivate

- Eliminar el directorio del entorno (macOS / Linux):
  rm -rf .venv

- Eliminar el directorio del entorno (Windows PowerShell):
  Remove-Item -Recurse -Force .venv

- Comprobación rápida:
  - Verifica existencia: [ -d .venv ] && echo ".venv existe" || echo ".venv no existe"


