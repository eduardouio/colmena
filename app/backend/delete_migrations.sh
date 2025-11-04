#!/bin/bash

BASE_DIR=$(pwd)

echo "Buscando y eliminando archivos de migrations y base sqlite..."

mapfile -t deleted_py < <(find "$BASE_DIR" -type f -path "*/migrations/*.py" ! -name "__init__.py" -print -delete)

mapfile -t deleted_pyc < <(find "$BASE_DIR" -type f -path "*/migrations/*.pyc" -print -delete)


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