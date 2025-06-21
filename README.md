# EC2 Manager API

## 🎯 Desafío Técnico - MercadoLibre DBA Team

API REST que simula la gestión de instancias EC2 para equipos DBA, desarrollada para el rol de **Ssr Backend Software Engineer**.

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


---

**Desarrollado por**: Felipe Bursa | **Para**: MercadoLibre DBA Team | **Junio 2025**
