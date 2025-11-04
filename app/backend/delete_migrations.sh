#!/bin/bash

BASE_DIR=$(pwd)

echo "Buscando y eliminando archivos de migrations y base sqlite..."

# Buscar y eliminar archivos .py (excluyendo __init__.py), listando lo eliminado
mapfile -t deleted_py < <(find "$BASE_DIR" -type f -path "*/migrations/*.py" ! -name "__init__.py" -print -delete)

# Buscar y eliminar archivos .pyc en migrations, listando lo eliminado
mapfile -t deleted_pyc < <(find "$BASE_DIR" -type f -path "*/migrations/*.pyc" -print -delete)

# Buscar y eliminar bases de datos sqlite llamadas db.sqlite3
mapfile -t deleted_db < <(find "$BASE_DIR" -type f -name "db.sqlite3" -print -delete)

total=$(( ${#deleted_py[@]} + ${#deleted_pyc[@]} + ${#deleted_db[@]} ))

if [ "$total" -eq 0 ]; then
	echo "No se encontraron archivos para eliminar."
else
	if [ ${#deleted_py[@]} -gt 0 ]; then
		echo "\nArchivos .py eliminados:"
		for f in "${deleted_py[@]}"; do
			echo " - $f"
		done
	fi

	if [ ${#deleted_pyc[@]} -gt 0 ]; then
		echo "\nArchivos .pyc eliminados:"
		for f in "${deleted_pyc[@]}"; do
			echo " - $f"
		done
	fi

	if [ ${#deleted_db[@]} -gt 0 ]; then
		echo "\nBases de datos eliminadas:"
		for f in "${deleted_db[@]}"; do
			echo " - $f"
		done
	fi

	echo "\nResumen: se eliminaron $total archivos."
fi

echo "Operación completada."