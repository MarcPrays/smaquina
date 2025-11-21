# 🏭 Sistema de Monitoreo y Diagnóstico Predictivo de Maquinaria - Backend

Sistema de monitoreo en tiempo real con análisis predictivo para maquinaria industrial utilizando FastAPI, SQLAlchemy y WebSockets.

## 📋 Características

- ✅ **API RESTful** con FastAPI
- ✅ **Base de datos MySQL** con SQLAlchemy ORM
- ✅ **WebSockets** para monitoreo en tiempo real
- ✅ **Simulador de datos** sintéticos
- ✅ **Análisis predictivo** con detección de anomalías
- ✅ **Gestión de alertas** (críticas, advertencias, estable)
- ✅ **CRUD completo** para máquinas y datos

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para bases de datos
- **MySQL** - Sistema de gestión de bases de datos
- **PyMySQL** - Conector MySQL para Python
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.10 o superior**
   - Descargar desde: https://www.python.org/downloads/

2. **MySQL Server 8.0+**
   - Descargar desde: https://dev.mysql.com/downloads/mysql/

3. **Git** (opcional)
   - Descargar desde: https://git-scm.com/downloads

4. **pip** (gestor de paquetes de Python)
   - Viene incluido con Python

---

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/MarcPrays/smaquina.git
cd smaquina
```



### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```



### 3. Configurar la Base de Datos

#### a) Crear la base de datos en MySQL

🔧 Solución 3: Usar MySQL Workbench (GUI)
Si tienes MySQL Workbench instalado:

- Abre MySQL Workbench
- Conecta a tu servidor local



Ejecuta los siguientes comandos SQL:

```sql
CREATE DATABASE bdmaquinaria;
USE bdmaquinaria;
```

#### b) Configurar credenciales de conexión

Abre el archivo `bd/database.py` y modifica las credenciales según tu configuración:

```python
# Variables de conexion
MYSQL_USER = "root"              # Tu usuario de MySQL
MYSQL_PASSWORD = ""         # Tu contraseña de MySQL (Si es que tienes, no agregues nada si no tienes contra)
MYSQL_HOST = "localhost"          # Host de MySQL
MYSQL_DB = "bdmaquinaria"         # Nombre de la base de datos
```

⚠️ **IMPORTANTE**: Para producción, usa variables de entorno en lugar de credenciales hardcodeadas.

### 4. Crear las Tablas

Las tablas se crean automáticamente al ejecutar la aplicación por primera vez gracias a:

```python
Base.metadata.create_all(bind=engine)
```

---

## ▶️ Ejecutar el Proyecto (terminal)

### Opción 1: Ejecución Normal

```bash
fastapi dev main.py
```



---

## 🌐 Acceso a la Aplicación

Una vez que el servidor esté corriendo, accede a:

- **API Principal**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

---

## 📁 Estructura del Proyecto

```
smaquina/
├── bd/
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy (Machine, MachineData, Alert)
│   └── schemas.py           # Esquemas Pydantic para validación
├── crud/
│   ├── machines.py          # Operaciones CRUD para máquinas
│   └── machine_data.py      # Operaciones CRUD para datos
├── routers/
│   ├── machines.py          # Endpoints de máquinas
│   ├── machine_data.py      # Endpoints de datos
│   ├── alerts.py            # Endpoints de alertas
│   ├── realtime.py          # WebSocket para tiempo real
│   └── simulator_control.py # Control del simulador
├── analisys/
│   └── predictive.py        # Análisis predictivo y detección de anomalías
├── simulator.py             # Simulador de datos sintéticos
├── main.py                  # Aplicación principal FastAPI
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

---

## 🧪 Probar la API

### 1. Crear una Máquina

```bash
curl -X POST "http://localhost:8000/new_machine" \
  -F "name=Compresor Industrial A1" \
  -F "description=Compresor de aire de alta presión"
```

### 2. Listar Máquinas

```bash
curl -X GET "http://localhost:8000/machines"
```

### 3. Iniciar Simulación

```bash
curl -X POST "http://localhost:8000/simulator/start/?machine_id=1"
```

### 4. Consultar Datos en Tiempo Real

Usa un cliente WebSocket (como Postman o código JavaScript) para conectarte a:

```
ws://localhost:8000/realtime/machine/?machine_id=1
```

---



### Configurar CORS (si usas frontend)

El proyecto ya tiene CORS configurado en `main.py`. Si necesitas restringir orígenes:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Umbrales de Alerta

Los umbrales predeterminados están en `analisys/predictive.py`:

```python
THRESHOLDS = {
    "temperature": 80.0,       # °C
    "vibration": 3.5,          # g
    "energy_consumption": 700  # W
}
```

Puedes modificarlos según tus necesidades.

---



---

## 📝 Generar requirements.txt

Si modificas las dependencias, genera un nuevo archivo:

```bash
pip freeze > requirements.txt
```

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **MarcPrays** - [GitHub](https://github.com/TU_USUARIO)


---

## 🎯 Próximos Pasos

- [ ] Implementar autenticación JWT
- [ ] Agregar más algoritmos de ML
- [ ] Dockerizar el proyecto
- [ ] Crear tests unitarios
- [ ] Implementar logs con Loguru

---

## 📚 Documentación Adicional

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**¡Gracias por usar este sistema! 🚀**