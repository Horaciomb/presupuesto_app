import json
from pathlib import Path
from typing import Optional, Any

class FileManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._crear_directorios()
    
    def _crear_directorios(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def guardar(self, data: Any):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Datos guardados en {self.file_path}")
    
    def cargar(self) -> Optional[dict]:
        if not self.file_path.exists():
            print(f"⚠️ Archivo {self.file_path} no encontrado")
            return None
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error al leer JSON: {e}")
            return None