"""
✅ Verificador de Keys - Script para validar keys de acceso
Conecta con la API local para verificar la validez de las keys
"""

import requests
import json
import sys
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://127.0.0.1:8000"

def print_banner():
    """Muestra el banner del verificador de keys"""
    print("=" * 60)
    print("✅ VERIFICADOR DE KEYS - Key Generator & Validator")
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

def verify_key(key):
    """Verifica una key usando la API"""
    try:
        data = {"key": key}
        
        response = requests.post(
            f"{API_BASE_URL}/validate-key",
            json=data,
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

def get_key_info(key):
    """Obtiene información detallada de una key"""
    try:
        response = requests.get(f"{API_BASE_URL}/key-info/{key}", timeout=10)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
            
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Error de conexión: {str(e)}"}
    except Exception as e:
        return False, {"error": f"Error inesperado: {str(e)}"}

def main():
    """Función principal del verificador de keys"""
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
    
    while True:
        print("📝 Opciones disponibles:")
        print("1. 🔍 Verificar una key")
        print("2. ℹ️  Obtener información de una key")
        print("3. 🚪 Salir")
        print("-" * 40)
        
        choice = input("Selecciona una opción (1-3): ").strip()
        
        if choice == "1":
            verify_key_option()
        elif choice == "2":
            get_key_info_option()
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Selecciona 1, 2 o 3.")
        
        print("\n" + "=" * 60 + "\n")

def verify_key_option():
    """Opción para verificar una key"""
    print("\n🔍 VERIFICACIÓN DE KEY")
    print("-" * 30)
    
    key = input("🔑 Ingresa la key a verificar: ").strip()
    if not key:
        print("❌ La key no puede estar vacía")
        return
    
    print("\n🚀 Verificando key...")
    print("-" * 30)
    
    success, result = verify_key(key)
    
    if success:
        if result['success']:
            print("✅ ¡Key válida!")
            print("-" * 20)
            print(f"👤 Usuario: {result['data']['user_id']}")
            print(f"🔄 Usos restantes: {result['data']['remaining_uses']}")
            print(f"⏱️  Expira: {result['data']['expires_at']}")
            print(f"📅 Verificada: {result['timestamp']}")
            
            # Guardar verificación exitosa
            try:
                with open("key_verifications.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*40}\n")
                    f.write(f"✅ VERIFICACIÓN EXITOSA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Key: {key}\n")
                    f.write(f"Usuario: {result['data']['user_id']}\n")
                    f.write(f"Usos restantes: {result['data']['remaining_uses']}\n")
                    f.write(f"Expira: {result['data']['expires_at']}\n")
                    f.write(f"{'='*40}\n")
            except Exception as e:
                print(f"⚠️  No se pudo guardar la verificación: {e}")
                
        else:
            print("❌ Key inválida")
            print(f"📝 Razón: {result['message']}")
            print(f"📅 Verificada: {result['timestamp']}")
            
            # Guardar verificación fallida
            try:
                with open("key_verifications.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*40}\n")
                    f.write(f"❌ VERIFICACIÓN FALLIDA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Key: {key}\n")
                    f.write(f"Razón: {result['message']}\n")
                    f.write(f"{'='*40}\n")
            except Exception as e:
                print(f"⚠️  No se pudo guardar la verificación: {e}")
    else:
        print("❌ Error al verificar la key:")
        if "detail" in result:
            print(f"   {result['detail']}")
        elif "error" in result:
            print(f"   {result['error']}")
        else:
            print(f"   {result}")

def get_key_info_option():
    """Opción para obtener información de una key"""
    print("\nℹ️  INFORMACIÓN DE KEY")
    print("-" * 30)
    
    key = input("🔑 Ingresa la key para obtener información: ").strip()
    if not key:
        print("❌ La key no puede estar vacía")
        return
    
    print("\n🚀 Obteniendo información...")
    print("-" * 30)
    
    success, result = get_key_info(key)
    
    if success:
        print("✅ Información obtenida:")
        print("-" * 20)
        print(f"🔑 Key: {result['key']}")
        print(f"👤 Usuario: {result['user_id']}")
        print(f"📅 Creada: {result['created_at']}")
        print(f"⏱️  Expira: {result['expires_at']}")
        print(f"🔄 Usos máximos: {result['max_uses']}")
        print(f"🔄 Usos actuales: {result['current_uses']}")
        print(f"📊 Estado: {'🟢 Activa' if result['is_active'] else '🔴 Revocada'}")
        
        # Verificar si ha expirado
        try:
            expires_at = datetime.fromisoformat(result['expires_at'])
            if datetime.now() > expires_at:
                print("⚠️  Esta key ha expirado")
        except:
            pass
            
    else:
        print("❌ Error al obtener información:")
        if "detail" in result:
            print(f"   {result['detail']}")
        elif "error" in result:
            print(f"   {result['error']}")
        else:
            print(f"   {result}")

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
