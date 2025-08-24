"""
🔑 Generador de Keys - Script para crear nuevas keys de acceso
Conecta con la API local para generar keys únicas
"""

import requests
import json
import sys
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://127.0.0.1:8000"
ADMIN_TOKEN = "admin_token_123"  # Token de administrador

def print_banner():
    """Muestra el banner del generador de keys"""
    print("=" * 60)
    print("🔑 GENERADOR DE KEYS - Key Generator & Validator")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_api_status():
    """Verifica si la API está funcionando"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def generate_key(user_id, duration_hours=24, max_uses=1):
    """Genera una nueva key usando la API"""
    try:
        headers = {
            "Authorization": f"Bearer {ADMIN_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "user_id": user_id,
            "duration_hours": duration_hours,
            "max_uses": max_uses
        }
        
        response = requests.post(
            f"{API_BASE_URL}/generate-key",
            json=data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return True, result
        else:
            return False, response.json()
            
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Error de conexión: {str(e)}"}
    except Exception as e:
        return False, {"error": f"Error inesperado: {str(e)}"}

def main():
    """Función principal del generador de keys"""
    print_banner()
    
    # Verificar estado de la API
    print("🔍 Verificando estado de la API...")
    if not check_api_status():
        print("❌ Error: La API no está funcionando")
        print("💡 Asegúrate de que la API esté ejecutándose en http://127.0.0.1:8000")
        print("💡 Ejecuta: cd api && python main.py")
        input("\nPresiona Enter para salir...")
        return
    
    print("✅ API funcionando correctamente\n")
    
    # Solicitar información para generar la key
    print("📝 Configuración de la nueva key:")
    print("-" * 40)
    
    # User ID
    while True:
        user_id = input("👤 ID del usuario: ").strip()
        if user_id:
            break
        print("❌ El ID del usuario no puede estar vacío")
    
    # Duración
    while True:
        try:
            duration_input = input("⏱️  Duración en horas (24): ").strip()
            if not duration_input:
                duration_hours = 24
                break
            duration_hours = int(duration_input)
            if duration_hours > 0:
                break
            print("❌ La duración debe ser mayor a 0")
        except ValueError:
            print("❌ Ingresa un número válido")
    
    # Usos máximos
    while True:
        try:
            max_uses_input = input("🔄 Usos máximos (1): ").strip()
            if not max_uses_input:
                max_uses = 1
                break
            max_uses = int(max_uses_input)
            if max_uses > 0:
                break
            print("❌ Los usos máximos deben ser mayor a 0")
        except ValueError:
            print("❌ Ingresa un número válido")
    
    print("\n" + "=" * 60)
    print("🚀 Generando key...")
    print("=" * 60)
    
    # Generar la key
    success, result = generate_key(user_id, duration_hours, max_uses)
    
    if success:
        print("✅ ¡Key generada exitosamente!")
        print("-" * 40)
        print(f"🔑 Key: {result['data']['key']}")
        print(f"👤 Usuario: {result['data']['user_id']}")
        print(f"⏱️  Expira: {result['data']['expires_at']}")
        print(f"🔄 Usos máximos: {result['data']['max_uses']}")
        print(f"📅 Generada: {result['timestamp']}")
        print("-" * 40)
        
        # Guardar en archivo
        try:
            with open("generated_keys.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Key generada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Key: {result['data']['key']}\n")
                f.write(f"Usuario: {result['data']['user_id']}\n")
                f.write(f"Expira: {result['data']['expires_at']}\n")
                f.write(f"Usos máximos: {result['data']['max_uses']}\n")
                f.write(f"{'='*50}\n")
            print("💾 Key guardada en 'generated_keys.txt'")
        except Exception as e:
            print(f"⚠️  No se pudo guardar en archivo: {e}")
        
    else:
        print("❌ Error al generar la key:")
        if "detail" in result:
            print(f"   {result['detail']}")
        elif "error" in result:
            print(f"   {result['error']}")
        else:
            print(f"   {result}")
    
    print("\n" + "=" * 60)
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        input("Presiona Enter para salir...")
        sys.exit(1)
