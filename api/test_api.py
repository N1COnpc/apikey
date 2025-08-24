"""
Script de prueba para la API de Keys
Ejecuta este archivo para probar los endpoints de la API
"""

import requests
import json

# URL base de la API (cambia esto por tu URL de Vercel cuando la despliegues)
BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("🧪 Probando la API de Keys...\n")
    
    # 1. Verificar estado de la API
    print("1. Verificando estado de la API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # 2. Verificar health check
    print("2. Verificando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # 3. Generar una key (requiere token de admin)
    print("3. Generando una key...")
    try:
        headers = {"Authorization": "Bearer admin_token_123"}
        data = {
            "user_id": "test_user_001",
            "duration_hours": 24,
            "max_uses": 5
        }
        response = requests.post(f"{BASE_URL}/generate-key", json=data, headers=headers)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"🔑 Key generada: {result['data']['key']}")
            test_key = result['data']['key']
        else:
            print(f"❌ Error: {response.json()}")
            test_key = "test_key_example"
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        test_key = "test_key_example"
        print()
    
    # 4. Validar la key generada
    print("4. Validando la key...")
    try:
        data = {"key": test_key}
        response = requests.post(f"{BASE_URL}/validate-key", json=data)
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # 5. Obtener información de la key
    print("5. Obteniendo información de la key...")
    try:
        response = requests.get(f"{BASE_URL}/key-info/{test_key}")
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # 6. Obtener estadísticas (requiere token de admin)
    print("6. Obteniendo estadísticas...")
    try:
        headers = {"Authorization": "Bearer admin_token_123"}
        response = requests.get(f"{BASE_URL}/stats", headers=headers)
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    test_api()
