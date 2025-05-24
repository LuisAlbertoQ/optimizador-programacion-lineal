import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from scipy.optimize import linprog

class RestriccionFrame(ttk.Frame):
    def __init__(self, parent, numero, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.numero = numero
        
        # Variables para la restricción
        self.var_x = tk.DoubleVar(value=1.0)
        self.var_y = tk.DoubleVar(value=1.0)
        self.var_comparacion = tk.StringVar(value="<=")
        self.var_valor = tk.DoubleVar(value=10.0)
        
        # Crear widgets
        ttk.Label(self, text=f"Restricción {numero}:").grid(row=0, column=0, padx=5)
        
        ttk.Entry(self, textvariable=self.var_x, width=5).grid(row=0, column=1, padx=5)
        ttk.Label(self, text="x  +").grid(row=0, column=2)
        
        ttk.Entry(self, textvariable=self.var_y, width=5).grid(row=0, column=3, padx=5)
        ttk.Label(self, text="y").grid(row=0, column=4)
        
        comparacion_combo = ttk.Combobox(self, textvariable=self.var_comparacion, 
                                        values=["<=", ">=", "="], width=3, state="readonly")
        comparacion_combo.grid(row=0, column=5, padx=5)
        
        ttk.Entry(self, textvariable=self.var_valor, width=5).grid(row=0, column=6, padx=5)
        
        # Botón para eliminar la restricción
        ttk.Button(self, text="X", width=2, command=self.eliminar_restriccion).grid(row=0, column=7, padx=5)
    
    def eliminar_restriccion(self):
        self.master.eliminar_restriccion(self.numero)
    
    def obtener_datos(self):
        return {
            "x": self.var_x.get(),
            "y": self.var_y.get(),
            "comparacion": self.var_comparacion.get(),
            "valor": self.var_valor.get()
        }

class OptimizadorPL(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimizador de Programación Lineal - 2 Variables")
        self.geometry("900x700")
        
        # Variables de configuración
        self.restricciones_frames = {}
        self.contador_restricciones = 0
        
        # Variables para la función objetivo
        self.var_objetivo_x = tk.DoubleVar(value=1.0)
        self.var_objetivo_y = tk.DoubleVar(value=1.0)
        self.var_objetivo_tipo = tk.StringVar(value="Maximizar")
        
        # Crear frames principales
        self.frame_entrada = ttk.Frame(self, padding="10")
        self.frame_entrada.pack(fill="x", padx=10, pady=10)
        
        self.frame_restricciones = ttk.LabelFrame(self, text="Restricciones", padding="10")
        self.frame_restricciones.pack(fill="x", padx=10, pady=5)
        
        self.frame_botones_restricciones = ttk.Frame(self.frame_restricciones, padding="5")
        self.frame_botones_restricciones.pack(fill="x")
        
        self.frame_lista_restricciones = ttk.Frame(self.frame_restricciones, padding="5")
        self.frame_lista_restricciones.pack(fill="x")
        
        self.frame_acciones = ttk.Frame(self, padding="10")
        self.frame_acciones.pack(fill="x", padx=10, pady=5)
        
        self.frame_resultado = ttk.LabelFrame(self, text="Resultado", padding="10")
        self.frame_resultado.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configuración de función objetivo
        ttk.Label(self.frame_entrada, text="Función objetivo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        ttk.Combobox(self.frame_entrada, textvariable=self.var_objetivo_tipo, 
                     values=["Maximizar", "Minimizar"], width=10, state="readonly").grid(row=0, column=1, padx=5)
        
        ttk.Entry(self.frame_entrada, textvariable=self.var_objetivo_x, width=5).grid(row=0, column=2, padx=5)
        ttk.Label(self.frame_entrada, text="x  +").grid(row=0, column=3)
        
        ttk.Entry(self.frame_entrada, textvariable=self.var_objetivo_y, width=5).grid(row=0, column=4, padx=5)
        ttk.Label(self.frame_entrada, text="y").grid(row=0, column=5)
        
        # Botón para agregar restricciones
        ttk.Button(self.frame_botones_restricciones, text="Agregar restricción", 
                   command=self.agregar_restriccion).pack(side="left", padx=5)
        
        # Botones de acción
        ttk.Button(self.frame_acciones, text="Resolver", command=self.resolver).pack(side="left", padx=5)
        ttk.Button(self.frame_acciones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        
        # Área de resultado con texto y gráfico
        self.frame_resultado_texto = ttk.Frame(self.frame_resultado)
        self.frame_resultado_texto.pack(side="left", fill="y", padx=5, pady=5)
        
        self.resultado_texto = tk.Text(self.frame_resultado_texto, height=10, width=40)
        self.resultado_texto.pack(fill="both", expand=True)
        
        self.frame_grafico = ttk.Frame(self.frame_resultado)
        self.frame_grafico.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Figura para el gráfico
        self.fig = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_grafico)
        self.toolbar.update()
        self.toolbar.pack(side="top", fill="x")
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Agregar algunas restricciones iniciales
        self.agregar_restriccion()
        self.agregar_restriccion()
    
    def agregar_restriccion(self):
        self.contador_restricciones += 1
        restriccion_frame = RestriccionFrame(self.frame_lista_restricciones, self.contador_restricciones)
        restriccion_frame.pack(fill="x", pady=2)
        self.restricciones_frames[self.contador_restricciones] = restriccion_frame
    
    def eliminar_restriccion(self, numero):
        if numero in self.restricciones_frames:
            self.restricciones_frames[numero].destroy()
            del self.restricciones_frames[numero]
    
    def limpiar(self):
        # Eliminar todas las restricciones
        for num in list(self.restricciones_frames.keys()):
            self.eliminar_restriccion(num)
        
        # Resetear variables
        self.var_objetivo_x.set(1.0)
        self.var_objetivo_y.set(1.0)
        self.var_objetivo_tipo.set("Maximizar")
        
        # Limpiar resultado
        self.resultado_texto.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()
        
        # Agregar algunas restricciones iniciales
        self.agregar_restriccion()
        self.agregar_restriccion()
    
    def resolver(self):
        try:
            # Obtener datos de la función objetivo
            c = [0, 0]
            c[0] = -self.var_objetivo_x.get() if self.var_objetivo_tipo.get() == "Maximizar" else self.var_objetivo_x.get()
            c[1] = -self.var_objetivo_y.get() if self.var_objetivo_tipo.get() == "Maximizar" else self.var_objetivo_y.get()
            
            # Obtener restricciones
            A_le = []
            b_le = []
            A_ge = []
            b_ge = []
            A_eq = []
            b_eq = []
            
            for frame in self.restricciones_frames.values():
                datos = frame.obtener_datos()
                a = [datos["x"], datos["y"]]
                b = datos["valor"]
                
                if datos["comparacion"] == "<=":
                    A_le.append(a)
                    b_le.append(b)
                elif datos["comparacion"] == ">=":
                    A_ge.append(a)
                    b_ge.append(b)
                else:  # "="
                    A_eq.append(a)
                    b_eq.append(b)
            
            # Convertir a arrays de numpy
            A_le = np.array(A_le) if A_le else None
            b_le = np.array(b_le) if b_le else None
            A_ge = np.array(A_ge) if A_ge else None
            b_ge = np.array(b_ge) if b_ge else None
            A_eq = np.array(A_eq) if A_eq else None
            b_eq = np.array(b_eq) if b_eq else None
            
            # Convertir restricciones >= a formato <=
            if A_ge is not None:
                if A_le is None:
                    A_le = -A_ge
                    b_le = -b_ge
                else:
                    A_le = np.vstack([A_le, -A_ge])
                    b_le = np.append(b_le, -b_ge)
            
            # Añadir restricciones de no negatividad (x, y >= 0)
            bounds = [(0, None), (0, None)]
            
            # Resolver el problema de programación lineal
            result = linprog(
                c=c,
                A_ub=A_le,
                b_ub=b_le,
                A_eq=A_eq,
                b_eq=b_eq,
                bounds=bounds,
                method='highs'
            )
            
            # Mostrar resultados
            self.resultado_texto.delete(1.0, tk.END)
            if result.success:
                # Calcular el valor real de la función objetivo (para maximización)
                valor_objetivo = result.x[0] * self.var_objetivo_x.get() + result.x[1] * self.var_objetivo_y.get()
                if self.var_objetivo_tipo.get() == "Maximizar":
                    valor_objetivo = -result.fun
                else:
                    valor_objetivo = result.fun
                
                self.resultado_texto.insert(tk.END, "Solución encontrada:\n\n")
                self.resultado_texto.insert(tk.END, f"x = {result.x[0]:.4f}\n")
                self.resultado_texto.insert(tk.END, f"y = {result.x[1]:.4f}\n\n")
                self.resultado_texto.insert(tk.END, f"Valor de la función objetivo: {valor_objetivo:.4f}\n")
                
                # Mostrar gráfico
                self.graficar_solucion(result.x, A_le, b_le, A_eq, b_eq)
            else:
                self.resultado_texto.insert(tk.END, "No se encontró solución:\n\n")
                self.resultado_texto.insert(tk.END, result.message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver: {str(e)}")
    
    def graficar_solucion(self, optimo, A_le, b_le, A_eq, b_eq):
        self.ax.clear()
        
        # Límites del gráfico
        x_max = max(20, optimo[0] * 1.5)
        y_max = max(20, optimo[1] * 1.5)
        
        # Crear la cuadrícula de puntos
        x = np.linspace(0, x_max, 1000)
        y = np.linspace(0, y_max, 1000)
        X, Y = np.meshgrid(x, y)
        
        # Graficar la región factible
        region_factible = np.ones_like(X, dtype=bool)
        
        # Aplicar restricciones <=
        if A_le is not None:
            for i in range(len(A_le)):
                a, b = A_le[i]
                region_factible &= (a * X + b * Y <= b_le[i])
        
        # Aplicar restricciones =
        if A_eq is not None:
            for i in range(len(A_eq)):
                a, b = A_eq[i]
                region_factible &= np.isclose(a * X + b * Y, b_eq[i], atol=1e-2)
        
        # Colorear la región factible
        self.ax.imshow(
            region_factible,
            extent=(0, x_max, 0, y_max),
            origin='lower',
            cmap='Blues',
            alpha=0.3
        )
        
        # Graficar las líneas de restricción
        x_vals = np.linspace(0, x_max, 100)
        
        # Líneas para restricciones <=
        if A_le is not None:
            for i in range(len(A_le)):
                a, b = A_le[i]
                if b == 0:
                    continue  # Evitar división por cero
                
                if a == 0:
                    # Línea horizontal
                    self.ax.axhline(y=b_le[i]/b, color='gray', linestyle='-', alpha=0.7)
                else:
                    # Línea normal
                    y_vals = (b_le[i] - a * x_vals) / b if b != 0 else np.zeros_like(x_vals)
                    self.ax.plot(x_vals, y_vals, 'gray', alpha=0.7)
        
        # Líneas para restricciones =
        if A_eq is not None:
            for i in range(len(A_eq)):
                a, b = A_eq[i]
                if b == 0:
                    continue  # Evitar división por cero
                
                if a == 0:
                    # Línea horizontal
                    self.ax.axhline(y=b_eq[i]/b, color='blue', linestyle='-', alpha=0.7)
                else:
                    # Línea normal
                    y_vals = (b_eq[i] - a * x_vals) / b if b != 0 else np.zeros_like(x_vals)
                    self.ax.plot(x_vals, y_vals, 'blue', alpha=0.7)
        
        # Graficar el punto óptimo
        self.ax.plot(optimo[0], optimo[1], 'ro', markersize=10)
        self.ax.annotate(f'Óptimo ({optimo[0]:.2f}, {optimo[1]:.2f})', 
                         xy=(optimo[0], optimo[1]), 
                         xytext=(optimo[0]+0.5, optimo[1]+0.5),
                         arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=7))
        
        # Ajustar límites del gráfico
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, y_max)
        
        # Añadir cuadrícula y etiquetas
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Solución Gráfica')
        
        # Dibujar
        self.canvas.draw()

if __name__ == "__main__":
    app = OptimizadorPL()
    app.mainloop()