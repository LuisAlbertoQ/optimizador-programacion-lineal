import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Optimizador de Programación Lineal - 2 Variables",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .restriction-formula {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-family: monospace;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">📊 Optimizador de Programación Lineal</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Resuelve problemas de optimización con 2 variables</p>', unsafe_allow_html=True)
st.markdown("---")

# Inicializar el estado de la sesión
if 'restricciones' not in st.session_state:
    st.session_state.restricciones = [
        {'x': 1.0, 'y': 1.0, 'comparacion': '<=', 'valor': 10.0},
        {'x': 2.0, 'y': 1.0, 'comparacion': '<=', 'valor': 15.0}
    ]

if 'resultado' not in st.session_state:
    st.session_state.resultado = None

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Función Objetivo
    st.subheader("🎯 Función Objetivo")
    objetivo_tipo = st.selectbox("Tipo de optimización", ["Maximizar", "Minimizar"], key="objetivo_tipo")
    
    col_coef1, col_coef2 = st.columns(2)
    with col_coef1:
        coef_x = st.number_input("Coeficiente de X", value=1.0, step=0.1, key="coef_x")
    with col_coef2:
        coef_y = st.number_input("Coeficiente de Y", value=1.0, step=0.1, key="coef_y")
    
    st.markdown(f'<div class="restriction-formula"><strong>{objetivo_tipo}:</strong> {coef_x}x + {coef_y}y</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Restricciones
    st.subheader("📋 Restricciones")
    
    # Botones para manejar restricciones
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ Agregar", key="add_restriction"):
            st.session_state.restricciones.append({'x': 1.0, 'y': 1.0, 'comparacion': '<=', 'valor': 10.0})
            st.rerun()
    
    with col_btn2:
        if st.button("🗑️ Limpiar", key="clear_restrictions"):
            st.session_state.restricciones = [
                {'x': 1.0, 'y': 1.0, 'comparacion': '<=', 'valor': 10.0},
                {'x': 2.0, 'y': 1.0, 'comparacion': '<=', 'valor': 15.0}
            ]
            st.session_state.resultado = None
            st.rerun()
    
    # Mostrar restricciones actuales
    restricciones_modificadas = []
    for i, restriccion in enumerate(st.session_state.restricciones):
        st.markdown(f"**Restricción {i+1}:**")
        
        col1, col2 = st.columns(2)
        with col1:
            x_val = st.number_input("X", value=restriccion['x'], step=0.1, key=f"x_{i}")
        with col2:
            y_val = st.number_input("Y", value=restriccion['y'], step=0.1, key=f"y_{i}")
        
        col3, col4, col5 = st.columns([1, 1, 0.3])
        with col3:
            comp_val = st.selectbox("", ["<=", ">=", "="], 
                                  index=["<=", ">=", "="].index(restriccion['comparacion']), 
                                  key=f"comp_{i}")
        with col4:
            valor_val = st.number_input("Valor", value=restriccion['valor'], step=0.1, key=f"val_{i}")
        with col5:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.restricciones.pop(i)
                st.rerun()
        
        # Actualizar la restricción
        restriccion_actualizada = {
            'x': x_val,
            'y': y_val,
            'comparacion': comp_val,
            'valor': valor_val
        }
        restricciones_modificadas.append(restriccion_actualizada)
        
        # Mostrar la fórmula
        st.markdown(f'<div class="restriction-formula">{x_val}x + {y_val}y {comp_val} {valor_val}</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    # Actualizar las restricciones en el estado
    st.session_state.restricciones = restricciones_modificadas
    
    # Botón resolver
    st.markdown("### 🚀 Acción")
    resolver = st.button("**RESOLVER PROBLEMA**", type="primary", use_container_width=True)

# Área principal - Dividida en dos columnas
col_main1, col_main2 = st.columns([1, 1])

with col_main1:
    st.header("📋 Resumen del Problema")
    
    # Mostrar función objetivo
    st.subheader("Función Objetivo:")
    objetivo_texto = f"**{objetivo_tipo}:** {coef_x}x + {coef_y}y"
    st.markdown(f'<div style="font-size: 1.2rem; padding: 1rem; background-color: #e8f4f8; border-radius: 0.5rem;">{objetivo_texto}</div>', unsafe_allow_html=True)
    
    # Mostrar restricciones
    st.subheader("Restricciones:")
    for i, restriccion in enumerate(st.session_state.restricciones):
        restriccion_texto = f"{restriccion['x']}x + {restriccion['y']}y {restriccion['comparacion']} {restriccion['valor']}"
        st.markdown(f"**{i+1}.** {restriccion_texto}")
    
    st.markdown("**Restricciones implícitas:** x ≥ 0, y ≥ 0")
    
    # Mostrar resultados si existen
    if st.session_state.resultado and st.session_state.resultado.get('success'):
        st.markdown("---")
        st.header("✅ Resultados")
        
        resultado = st.session_state.resultado
        
        # Métricas principales
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Valor de X", f"{resultado['x']:.4f}")
        with col_res2:
            st.metric("Valor de Y", f"{resultado['y']:.4f}")
        with col_res3:
            st.metric("Función Objetivo", f"{resultado['objetivo']:.4f}")
        
        # Tabla de evaluación de restricciones
        st.subheader("📊 Evaluación de Restricciones")
        eval_data = []
        for i, restriccion in enumerate(st.session_state.restricciones):
            valor_izq = restriccion['x'] * resultado['x'] + restriccion['y'] * resultado['y']
            cumple = "✅" if (
                (restriccion['comparacion'] == '<=' and valor_izq <= restriccion['valor'] + 1e-6) or
                (restriccion['comparacion'] == '>=' and valor_izq >= restriccion['valor'] - 1e-6) or
                (restriccion['comparacion'] == '=' and abs(valor_izq - restriccion['valor']) <= 1e-6)
            ) else "❌"
            
            eval_data.append({
                'Restricción': f"{restriccion['x']}x + {restriccion['y']}y {restriccion['comparacion']} {restriccion['valor']}",
                'Valor Calculado': f"{valor_izq:.4f}",
                'Valor Límite': f"{restriccion['valor']:.4f}",
                'Cumple': cumple
            })
        
        df_eval = pd.DataFrame(eval_data)
        st.dataframe(df_eval, use_container_width=True, hide_index=True)
    
    elif st.session_state.resultado and not st.session_state.resultado.get('success'):
        st.error("❌ No se encontró solución factible")
        st.write(f"**Mensaje:** {st.session_state.resultado.get('message', 'Error desconocido')}")

with col_main2:
    st.header("📈 Visualización Gráfica")
    
    if resolver:
        with st.spinner("Resolviendo problema de programación lineal..."):
            try:
                # Preparar los datos para linprog
                c = [0, 0]
                c[0] = -coef_x if objetivo_tipo == "Maximizar" else coef_x
                c[1] = -coef_y if objetivo_tipo == "Maximizar" else coef_y
                
                # Procesar restricciones
                A_le = []
                b_le = []
                A_ge = []
                b_ge = []
                A_eq = []
                b_eq = []
                
                for restriccion in st.session_state.restricciones:
                    a = [restriccion['x'], restriccion['y']]
                    b = restriccion['valor']
                    
                    if restriccion['comparacion'] == "<=":
                        A_le.append(a)
                        b_le.append(b)
                    elif restriccion['comparacion'] == ">=":
                        A_ge.append(a)
                        b_ge.append(b)
                    else:  # "="
                        A_eq.append(a)
                        b_eq.append(b)
                
                # Convertir a arrays
                A_le = np.array(A_le) if A_le else None
                b_le = np.array(b_le) if b_le else None
                A_ge = np.array(A_ge) if A_ge else None
                b_ge = np.array(b_ge) if b_ge else None
                A_eq = np.array(A_eq) if A_eq else None
                b_eq = np.array(b_eq) if b_eq else None
                
                # Convertir >= a <=
                if A_ge is not None:
                    if A_le is None:
                        A_le = -A_ge
                        b_le = -b_ge
                    else:
                        A_le = np.vstack([A_le, -A_ge])
                        b_le = np.append(b_le, -b_ge)
                
                # Restricciones de no negatividad
                bounds = [(0, None), (0, None)]
                
                # Resolver
                result = linprog(
                    c=c,
                    A_ub=A_le,
                    b_ub=b_le,
                    A_eq=A_eq,
                    b_eq=b_eq,
                    bounds=bounds,
                    method='highs'
                )
                
                if result.success:
                    # Calcular valor objetivo real
                    valor_objetivo = result.x[0] * coef_x + result.x[1] * coef_y
                    
                    # Guardar resultado en session_state
                    st.session_state.resultado = {
                        'success': True,
                        'x': result.x[0],
                        'y': result.x[1],
                        'objetivo': valor_objetivo,
                        'result_obj': result
                    }
                    
                    st.success("✅ ¡Solución encontrada!")
                else:
                    st.session_state.resultado = {
                        'success': False,
                        'message': result.message
                    }
                    
            except Exception as e:
                st.error(f"❌ Error al resolver: {str(e)}")
                st.session_state.resultado = {'success': False, 'message': str(e)}
    
    # Mostrar gráfico si hay resultado exitoso
    if st.session_state.resultado and st.session_state.resultado.get('success'):
        resultado = st.session_state.resultado
        
        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Límites del gráfico
        x_max = max(20, resultado['x'] * 1.5) if resultado['x'] > 0 else 20
        y_max = max(20, resultado['y'] * 1.5) if resultado['y'] > 0 else 20
        
        # Crear la cuadrícula
        x = np.linspace(0, x_max, 1000)
        y = np.linspace(0, y_max, 1000)
        X, Y = np.meshgrid(x, y)
        
        # Región factible inicial (todo el primer cuadrante)
        region_factible = (X >= 0) & (Y >= 0)
        
        # Aplicar restricciones
        for restriccion in st.session_state.restricciones:
            a, b = restriccion['x'], restriccion['y']
            valor = restriccion['valor']
            
            if restriccion['comparacion'] == "<=":
                region_factible &= (a * X + b * Y <= valor)
            elif restriccion['comparacion'] == ">=":
                region_factible &= (a * X + b * Y >= valor)
            else:  # "="
                region_factible &= np.isclose(a * X + b * Y, valor, atol=1e-2)
        
        # Colorear región factible
        ax.imshow(
            region_factible,
            extent=(0, x_max, 0, y_max),
            origin='lower',
            cmap='Blues',
            alpha=0.3,
            aspect='auto'
        )
        
        # Graficar líneas de restricción
        x_vals = np.linspace(0, x_max, 100)
        colors = ['red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
        
        for i, restriccion in enumerate(st.session_state.restricciones):
            a, b = restriccion['x'], restriccion['y']
            valor = restriccion['valor']
            color = colors[i % len(colors)]
            
            if b != 0:
                y_vals = (valor - a * x_vals) / b
                valid_mask = (y_vals >= 0) & (y_vals <= y_max)
                ax.plot(x_vals[valid_mask], y_vals[valid_mask], 
                       color=color, linewidth=2, alpha=0.8,
                       label=f"R{i+1}: {a}x + {b}y {restriccion['comparacion']} {valor}")
            elif a != 0:
                x_line = valor / a
                if 0 <= x_line <= x_max:
                    ax.axvline(x=x_line, color=color, linewidth=2, alpha=0.8,
                             label=f"R{i+1}: {a}x + {b}y {restriccion['comparacion']} {valor}")
        
        # Punto óptimo
        ax.plot(resultado['x'], resultado['y'], 'ro', markersize=12, 
               markeredgecolor='darkred', markeredgewidth=2, label='Punto Óptimo')
        ax.annotate(f'Óptimo\n({resultado["x"]:.2f}, {resultado["y"]:.2f})', 
                   xy=(resultado['x'], resultado['y']), 
                   xytext=(resultado['x']+x_max*0.05, resultado['y']+y_max*0.05),
                   arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8),
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
        
        # Configurar gráfico
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, y_max)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y', fontsize=12, fontweight='bold')
        ax.set_title('Solución Gráfica del Problema de Programación Lineal', 
                    fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Mostrar gráfico
        plt.tight_layout()
        st.pyplot(fig)
    
    else:
        # Mostrar gráfico de ejemplo o instrucciones
        st.info("👆 Configura tu problema en el panel lateral y presiona 'RESOLVER PROBLEMA' para ver la solución gráfica.")
        
        # Gráfico de ejemplo
        fig, ax = plt.subplots(figsize=(8, 6))
        x = np.linspace(0, 10, 100)
        y1 = 10 - x
        y2 = (15 - 2*x)
        
        ax.fill_between(x, 0, np.minimum(y1, y2), where=(np.minimum(y1, y2) >= 0), 
                       alpha=0.3, color='blue', label='Región Factible')
        ax.plot(x, y1, 'r-', label='x + y ≤ 10')
        ax.plot(x, y2, 'g-', label='2x + y ≤ 15')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Ejemplo de Problema de Programación Lineal')
        ax.legend()
        
        st.pyplot(fig)

# Información adicional
st.markdown("---")
with st.expander("ℹ️ Cómo usar esta aplicación"):
    st.markdown("""
    ### 📋 Instrucciones de uso:
    
    1. **Configura la función objetivo**:
       - Elige si quieres maximizar o minimizar
       - Ingresa los coeficientes para X e Y
    
    2. **Define las restricciones**:
       - Usa el panel lateral para agregar/modificar restricciones
       - Cada restricción tiene la forma: ax + by ≤/≥/= c
       - Puedes agregar tantas restricciones como necesites
    
    3. **Resuelve el problema**:
       - Presiona el botón "RESOLVER PROBLEMA"
       - Observa la solución en el gráfico y los resultados numéricos
    
    4. **Interpreta los resultados**:
       - El punto rojo en el gráfico es la solución óptima
       - La región azul muestra todas las soluciones factibles
       - Las líneas de colores representan las restricciones
    
    ### 🔧 Características:
    - ✅ Resolución automática usando el método Simplex
    - ✅ Visualización gráfica interactiva
    - ✅ Evaluación automática de restricciones
    - ✅ Soporte para maximización y minimización
    - ✅ Restricciones de igualdad, desigualdad menor y mayor
    
    ### ⚠️ Notas importantes:
    - Las variables X e Y son automáticamente no negativas (X ≥ 0, Y ≥ 0)
    - Si no existe solución factible, se mostrará un mensaje de error
    - El gráfico se ajusta automáticamente según la solución encontrada
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    💡 <strong>Optimizador de Programación Lineal</strong> | 
    Desarrollado con Streamlit | 
    🔬 Método Simplex implementado con SciPy
</div>
""", unsafe_allow_html=True)