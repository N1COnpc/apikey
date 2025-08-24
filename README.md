# 🔑 Key Generator & Validator API

API para generar y verificar keys de acceso con sistema de autenticación y control de uso.

## 🚀 Características

- **Generación de Keys**: Crea keys únicas y seguras
- **Validación de Keys**: Verifica la validez de las keys
- **Control de Expiración**: Keys con tiempo de vida configurable
- **Límite de Usos**: Control del número máximo de usos por key
- **Sistema de Admin**: Endpoints protegidos para administradores
- **Encriptación**: Datos seguros usando Fernet
- **Documentación Automática**: Swagger UI integrado

## 📋 Endpoints

### 🔓 Públicos
- `GET /` - Información de la API
- `GET /health` - Estado de salud de la API
- `POST /validate-key` - Validar una key
- `GET /key-info/{key}` - Información de una key específica

### 🔒 Administradores (Requieren Token)
- `POST /generate-key` - Generar una nueva key
- `GET /keys` - Listar todas las keys
- `DELETE /revoke-key/{key}` - Revocar una key
- `GET /stats` - Estadísticas de las keys

## 🛠️ Instalación Local

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Ejecutar la API:**
```bash
python main.py
```

3. **Acceder a la documentación:**
```
http://localhost:8000/docs
```

## 📖 Uso de la API

### Generar una Key (Admin)
```bash
curl -X POST "http://localhost:8000/generate-key" \
  -H "Authorization: Bearer admin_token_123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usuario_001",
    "duration_hours": 24,
    "max_uses": 5
  }'
```

### Validar una Key
```bash
curl -X POST "http://localhost:8000/validate-key" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "tu_key_aqui"
  }'
```

### Obtener Información de una Key
```bash
curl "http://localhost:8000/key-info/tu_key_aqui"
```

### Obtener Estadísticas (Admin)
```bash
curl -H "Authorization: Bearer admin_token_123" \
  "http://localhost:8000/stats"
```

## 🔐 Tokens de Administrador

Por defecto, la API acepta estos tokens de administrador:
- `admin_token_123`
- `super_admin_456`

**⚠️ IMPORTANTE:** Cambia estos tokens en producción por tokens seguros.

## 🧪 Pruebas

Ejecuta el script de pruebas:
```bash
python test_api.py
```

## 🚀 Despliegue en Vercel

1. **Sube tu código a GitHub**
2. **Conecta tu repositorio en Vercel**
3. **Configura el directorio raíz como `api/`**
4. **Despliega**

## 📊 Estructura de Respuesta

### Respuesta Exitosa
```json
{
  "success": true,
  "message": "Operación exitosa",
  "data": {
    "key": "abc123...",
    "user_id": "usuario_001",
    "expires_at": "2024-01-01T00:00:00"
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### Respuesta de Error
```json
{
  "success": false,
  "message": "Key inválida",
  "timestamp": "2024-01-01T00:00:00"
}
```

## 🔧 Configuración

### Variables de Entorno
- `SECRET_KEY`: Clave secreta para encriptación (se genera automáticamente)

### Personalización
- Modifica `admin_tokens` en `main.py` para cambiar los tokens de administrador
- Ajusta la duración por defecto de las keys en `KeyRequest`
- Personaliza el formato de las keys en `generate_key()`

## 📝 Notas de Producción

- **Base de Datos**: Reemplaza `keys_database` por una base de datos real
- **Autenticación**: Implementa un sistema de autenticación robusto
- **Logging**: Agrega logging para auditoría
- **Rate Limiting**: Implementa límites de velocidad
- **HTTPS**: Usa siempre HTTPS en producción

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
