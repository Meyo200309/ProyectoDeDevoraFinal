import re

# Rutas de los archivos de entrada y salida
input_file = "ventas_historicas.sql"
output_file = "ventas_historicas_normalizado.sql"

# Expresiones regulares para identificar y capturar los componentes de las fechas
# 1. Identifica el formato largo 'AAAA-MM-DD HH:MM:SS' y captura solo el año-mes-día
pattern_datetime = re.compile(r"'(\d{4}-\d{2}-\d{2}) \d{2}:\d{2}:\d{2}'")

# 2. Identifica el formato corto con barras 'DD/MM/AA' y captura día (\1), mes (\2) y año (\3)
pattern_slash = re.compile(r"'(\d{2})/(\d{2})/(\d{2})'")

lineas_procesadas = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        # Paso 1: Normalizar el formato Datetime eliminando las horas, minutos y segundos
        line = pattern_datetime.sub(r"'\1'", line)
        
        # Paso 2: Convertir 'DD/MM/AA' reorganizando los grupos a '20AA-MM-DD'
        line = pattern_slash.sub(r"'20\3-\2-\1'", line)
        
        # Paso 3: Optimizar la estructura de la tabla (cambiar VARCHAR por DATE nativo)
        if "fecha VARCHAR(50)" in line:
            line = line.replace("fecha VARCHAR(50)", "fecha DATE")
            
        lineas_procesadas.append(line)

# Guardar los cambios estructurales en el nuevo archivo limpio
with open(output_file, "w", encoding="utf-8") as f_out:
    f_out.writelines(lineas_procesadas)

print(f"El archivo ha sido procesado y guardado como: {output_file}")
