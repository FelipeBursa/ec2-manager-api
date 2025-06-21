# EC2 Manager API

## 🎯 Desafío Técnico - MercadoLibre DBA Team

API REST que simula la gestión de instancias EC2 para equipos DBA, desarrollada para el rol de **Ssr Backend Software Engineer**.

### Requisitos Cumplidos ✅

- **GET /instances** - Lista instancias EC2 simuladas (id, name, type, state, region)
- **POST /instances/{id}/stop** - Simula detener instancia con mensaje éxito/fallo
- **Python + boto3** con mocks (moto library)
- **Código limpio y modular** con manejo de errores
- **Tests unitarios** con 100% coverage

### Stack Tecnológico

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno
- **[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html)** - SDK de AWS
- **[moto](https://docs.getmoto.org/en/latest/)** - Mocking de servicios AWS
- **Pydantic** - Validación de datos
- **pytest** - Testing framework

## 🚀 Setup Rápido

### Prerrequisitos
- Python 3.8+ 
- pip

### Instalación

```bash
# 1. Clonar repositorio
git clone <https://github.com/FelipeBursa/ec2-manager-api.git>
cd ec2-manager-api

# 2. Instalar dependencias (NO necesita venv)
pip install -r requirements.txt

# 3. Ejecutar aplicación
python -m src.app
```

> **💡 Nota sobre venv**: No es necesario crear un entorno virtual para probar esta API. Las dependencias son estándar y no conflictúan con otros proyectos. Si prefieres usar venv, créalo con `python -m venv venv && source venv/bin/activate` antes del paso 2.

**API disponible en**: `http://localhost:8000`  
**Documentación**: `http://localhost:8000/docs`

## 📡 Endpoints

### GET /instances
Lista todas las instancias EC2 simuladas.

```json
[
  {
    "id": "i-1234567890abcdef0",
    "name": "web-server-prod",
    "type": "t3.medium",
    "state": "running",
    "region": "us-east-1"
  }
]
```

### POST /instances/{id}/stop
Detiene una instancia específica.

**Respuesta exitosa**:
```json
{
  "success": true,
  "message": "Instance i-1234567890abcdef0 is now stopping",
  "previous_state": "running",
  "current_state": "stopping"
}
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html
```

**Coverage**: 100% - Tests unitarios e integración completos.

## 🔧 Demo Rápido

```bash
# 1. Levantar API
python -m src.app

# 2. Listar instancias
curl http://localhost:8000/instances

# 3. Detener instancia
curl -X POST http://localhost:8000/instances/i-1234567890abcdef0/stop
```

## 📁 Estructura

```
ec2-manager-api/
├── src/
│   ├── app.py              # App FastAPI principal
│   ├── models/instance.py  # Modelos Pydantic
│   ├── routes/instances.py # Endpoints API
│   ├── services/ec2_service.py # Lógica negocio
│   └── utils/mock_data.py  # Datos simulados
├── tests/                  # Tests unitarios/integración
├── requirements.txt        # Dependencias
└── README.md
```

## 🎯 Highlights Técnicos

- **Simulación realista**: Estados EC2 válidos y transiciones lógicas
- **Error handling**: Validaciones robustas con códigos HTTP apropiados  
- **Mocking avanzado**: moto para simular boto3 sin AWS real
- **Documentación automática**: OpenAPI/Swagger incluido
- **Arquitectura modular**: Separación de responsabilidades clara

---

**Desarrollado por**: Felipe Bursa | **Para**: MercadoLibre DBA Team | **Junio 2025**
