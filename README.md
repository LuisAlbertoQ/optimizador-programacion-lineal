# 📊 Optimizador de Programación Lineal

Una aplicación web interactiva para resolver problemas de programación lineal con 2 variables.

## 🚀 Características

- Maximización y minimización de funciones objetivo
- Soporte para restricciones de igualdad y desigualdad
- Visualización gráfica de la región factible
- Evaluación automática de restricciones
- Interfaz intuitiva y fácil de usar

## 💻 Uso

1. Define tu función objetivo (coeficientes y tipo)
2. Agrega las restricciones necesarias
3. Presiona "Resolver Problema"
4. Observa la solución en el gráfico y tabla de resultados

## 🔧 Tecnologías

- Streamlit
- SciPy (método Simplex)
- Matplotlib
- NumPy
- Pandas

## 🔧 Instalacion (solo si quieres probar localmente)
Primero: Clonamos el repositorio con
```
git clone https://github.com/LuisAlbertoQ/optimizador-programacion-lineal.git
```
Segundo: Creamos un entorno virtual en la carpeta donde clonamos el repositorio
```
python -m venv <nombre del entorno virtual>
ejemplo👇
python -m venv env
```
Tercero: Activamos el entorno virtual e Instalamos las librerias requeridas:
```
<nombre del entorno virtual>\Scripts\activate
ejemplo👇
env\Scripts\activate
```
librerias👇
```
pip inatall Streamlit
pip install SciPy
pip install Matplotlib
pip install NumPy
pip install Pandas
```
Utiliza este comando para iniciar el programa
```
streamlit run app.py
```
Listo eso seria todo 😁
---
Desarrollado para facilitar el aprendizaje de programación lineal.
