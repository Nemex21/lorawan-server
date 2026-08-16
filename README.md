# LoRa WAN Emergency Communication Server

Sistema de servidor central para comunicación LoRa WAN con capacidad de mensajería de emergencia, tracking GPS y mapeo en tiempo real.

## Características

- 📡 **Network Server**: Recibe y procesa paquetes LoRa
- 🗺️ **Dashboard en Tiempo Real**: Mapa interactivo con WebSockets
- 💬 **Mensajería**: Sistema de mensajería encriptada AES-256
- 📍 **Tracking GPS**: Seguimiento de ubicaciones de dispositivos
- 🔐 **Seguridad**: Cifrado end-to-end con AES-256
- 💾 **Base de Datos**: SQLite para almacenamiento persistente
- ⚡ **API RESTful**: FastAPI con documentación automática
- 🖥️ **GUI Nativa**: Interfaz gráfica PyQt6 para Windows

## Requisitos

- Python 3.9+
- pip
- SQLite3

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/Nemex21/lorawan-server.git
cd lorawan-server

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

## Uso

```bash
# Ejecutar servidor con GUI
python run_server_gui.py

# O solo servidor sin GUI
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Estructura del Proyecto

```
lorawan-server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI
│   ├── config.py               # Configuración
│   ├── models/                 # Modelos de datos
│   ├── routes/                 # Rutas API
│   ├── services/               # Servicios de negocio
│   └── websocket/              # WebSockets
├── gui/                        # Interfaz gráfica PyQt6
│   ├── main_window.py
│   ├── widgets/
│   ├── utils/
│   └── resources/
├── database/
│   ├── models.py
│   └── init_db.py
├── requirements.txt
├── .env.example
├── run_server_gui.py
└── README.md
```

## Licencia

Apache License 2.0
