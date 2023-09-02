# Sistemas Distribuidos | gRPC

El plazo de entrega del TP es hasta el 05/09, puede puede ser extendido una semana mas. Las consignas estan en este [PDF](https://drive.google.com/file/d/1bnzmNa9q-rOXIRGmKE1DZOYYAykm50jU/view?usp=sharing)

## Instalacion

- [Instalar Python](https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe)
- `python -m pip install --upgrade pip` (puede ser que en vez de python sea py o python3)
- `git clone https://github.com/MauroLucas/Server-RPC.git` (Es posible que tengas que pedir acceso a Mauro)
- `cd .\Server-RPC\`
- `pip3 install virtualenv` (El server se corre antes que el cliente)
- `virtualenv venv`
- `Set-ExecutionPolicy -Scope LocalMachine unrestricted` (Usando powershell)
- `./venv/scripts/activate` (solo en linux)
- `pip install -r requirements.txt`
- `cd database`
- `python database.py` (Recordar no tener el cliente de postgresql ejecutando porque produce error, **es posible que tengas que cambiar la contrase;a**)
- `cd..`
- `cd server`
- `python server.py`
