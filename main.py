from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import secrets
import string
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64

# Crear la aplicación FastAPI
app = FastAPI(
    title="Key Generator & Validator API",
    description="API para generar y verificar keys de acceso",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de seguridad
SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)
security = HTTPBearer()

# Almacenamiento de keys (en producción usarías una base de datos)
keys_database = {}

# Modelos de datos
class KeyRequest(BaseModel):
    user_id: str
    duration_hours: int = 24  # Duración por defecto: 24 horas
    max_uses: int = 1  # Usos máximos por defecto: 1

class KeyValidation(BaseModel):
    key: str

class KeyInfo(BaseModel):
    key: str
    user_id: str
    created_at: str
    expires_at: str
    max_uses: int
    current_uses: int
    is_active: bool

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    timestamp: str

# Función para generar keys únicas
def generate_key(length: int = 32) -> str:
    """Genera una key única y segura"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Función para encriptar datos
def encrypt_data(data: str) -> str:
    """Encripta datos usando Fernet"""
    return cipher_suite.encrypt(data.encode()).decode()

# Función para desencriptar datos
def decrypt_data(encrypted_data: str) -> str:
    """Desencripta datos usando Fernet"""
    try:
        return cipher_suite.decrypt(encrypted_data.encode()).decode()
    except:
        return None

# Función para verificar token de administrador
async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica si el token es válido para operaciones de administrador"""
    # En producción, verificarías contra una base de datos de tokens válidos
    admin_tokens = ["admin_token_123", "super_admin_456"]  # Ejemplo
    
    if credentials.credentials not in admin_tokens:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token de administrador inválido"
        )
    return credentials.credentials

# Endpoints
@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Key Generator & Validator API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "generate_key": "/generate-key",
            "validate_key": "/validate-key",
            "get_key_info": "/key-info/{key}",
            "list_keys": "/keys",
            "revoke_key": "/revoke-key/{key}"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate-key", response_model=ApiResponse)
async def generate_key_endpoint(
    key_request: KeyRequest,
    admin_token: str = Depends(verify_admin_token)
):
    """Genera una nueva key de acceso"""
    try:
        # Generar key única
        new_key = generate_key()
        
        # Calcular fechas
        now = datetime.now()
        expires_at = now + timedelta(hours=key_request.duration_hours)
        
        # Crear información de la key
        key_info = {
            "key": new_key,
            "user_id": key_request.user_id,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "max_uses": key_request.max_uses,
            "current_uses": 0,
            "is_active": True
        }
        
        # Almacenar en la base de datos
        keys_database[new_key] = key_info
        
        return ApiResponse(
            success=True,
            message="Key generada exitosamente",
            data={
                "key": new_key,
                "user_id": key_request.user_id,
                "expires_at": expires_at.isoformat(),
                "max_uses": key_request.max_uses
            },
            timestamp=now.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-key", response_model=ApiResponse)
async def validate_key_endpoint(key_validation: KeyValidation):
    """Valida una key de acceso"""
    try:
        key = key_validation.key
        
        if key not in keys_database:
            return ApiResponse(
                success=False,
                message="Key inválida",
                timestamp=datetime.now().isoformat()
            )
        
        key_info = keys_database[key]
        
        # Verificar si la key está activa
        if not key_info["is_active"]:
            return ApiResponse(
                success=False,
                message="Key revocada",
                timestamp=datetime.now().isoformat()
            )
        
        # Verificar si ha expirado
        expires_at = datetime.fromisoformat(key_info["expires_at"])
        if datetime.now() > expires_at:
            return ApiResponse(
                success=False,
                message="Key expirada",
                timestamp=datetime.now().isoformat()
            )
        
        # Verificar si se ha excedido el límite de usos
        if key_info["current_uses"] >= key_info["max_uses"]:
            return ApiResponse(
                success=False,
                message="Key ha alcanzado el límite de usos",
                timestamp=datetime.now().isoformat()
            )
        
        # Incrementar contador de usos
        key_info["current_uses"] += 1
        
        return ApiResponse(
            success=True,
            message="Key válida",
            data={
                "user_id": key_info["user_id"],
                "remaining_uses": key_info["max_uses"] - key_info["current_uses"],
                "expires_at": key_info["expires_at"]
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/key-info/{key}", response_model=KeyInfo)
async def get_key_info(key: str):
    """Obtiene información detallada de una key"""
    if key not in keys_database:
        raise HTTPException(status_code=404, detail="Key no encontrada")
    
    return KeyInfo(**keys_database[key])

@app.get("/keys", response_model=List[KeyInfo])
async def list_keys(admin_token: str = Depends(verify_admin_token)):
    """Lista todas las keys (solo administradores)"""
    return [KeyInfo(**key_info) for key_info in keys_database.values()]

@app.delete("/revoke-key/{key}", response_model=ApiResponse)
async def revoke_key(key: str, admin_token: str = Depends(verify_admin_token)):
    """Revoca una key (solo administradores)"""
    if key not in keys_database:
        raise HTTPException(status_code=404, detail="Key no encontrada")
    
    keys_database[key]["is_active"] = False
    
    return ApiResponse(
        success=True,
        message="Key revocada exitosamente",
        data={"key": key},
        timestamp=datetime.now().isoformat()
    )

@app.get("/stats")
async def get_stats(admin_token: str = Depends(verify_admin_token)):
    """Obtiene estadísticas de las keys (solo administradores)"""
    total_keys = len(keys_database)
    active_keys = sum(1 for k in keys_database.values() if k["is_active"])
    expired_keys = sum(1 for k in keys_database.values() if datetime.now() > datetime.fromisoformat(k["expires_at"]))
    
    return {
        "total_keys": total_keys,
        "active_keys": active_keys,
        "expired_keys": expired_keys,
        "timestamp": datetime.now().isoformat()
    }

# Para desarrollo local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
