import urllib.request
import urllib.error
import json
from datetime import datetime

ONPE_BASE = 'https://resultadoelectoral.onpe.gob.pe'
ENDPOINTS = [
    f'{ONPE_BASE}/api/presidencial/resumen',
    f'{ONPE_BASE}/api/v1/presidencial/resumen',
    f'{ONPE_BASE}/api/resultados/presidencial',
    f'{ONPE_BASE}/api/v1/resultados/presidencial',
    f'{ONPE_BASE}/presidencial/api/resumen',
]

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    for url in ENDPOINTS:
        try:
            print(f"Probando endpoint: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue
            
    return None

def main():
    print(f"[{datetime.now()}] Iniciando actualización de datos ONPE...")
    data = fetch_data()
    if data:
        with open('onpe_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Datos actualizados correctamente en onpe_data.json")
    else:
        print("No se pudo obtener datos de la ONPE. Creando onpe_data.json vacío para evitar errores...")
        # Create a dummy JSON so git add doesn't fail
        fallback_data = {"error": "API no disponible", "timestamp": str(datetime.now())}
        with open('onpe_data.json', 'w', encoding='utf-8') as f:
            json.dump(fallback_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
