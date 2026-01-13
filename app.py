import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('telco_customer_churn.csv')

df = load_data()

st.title('Análisis de Churn en Customers de Telco')
st.markdown("Dashboard para identificar clientes en riesgo de Churn")
st.divider()

st.header("Situación actual de Churn en Telco")


col1, col2, col3, col4 = st.columns(4)

total_clientes = len(df)
churn_clientes = len(df[df['Churn'] == 'Yes'])
churn_rate = (churn_clientes / total_clientes) * 100
ingresos_perdidos = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()

col1.metric("Total Clientes", f"{total_clientes:,}")
col2.metric("Clientes Perdidos", f"{churn_clientes:,}")
col3.metric("Tasa de Churn", f"{churn_rate:.1f}%")
col4.metric("Ingresos Mensuales Perdidos", f"${ingresos_perdidos:,.0f}")

st.divider()

st.header("Indicadores cruciales de Churn en Customers")

hist_tenure = st.checkbox('Mostrar distribución de antigüedad')
if hist_tenure:
    st.subheader("Antigüedad del cliente y su relación con el churn")
    
    df_plot = df.copy()
    df_plot['Tipo'] = df_plot['Churn'].map({'Yes': 'Se van', 'No': 'Se quedan'})
    
    fig = px.histogram(df_plot, x='tenure', color='Tipo', 
                       nbins=30, 
                       labels={'tenure': 'Meses como cliente', 'Tipo': ''},
                       color_discrete_map={'Se van': 'blue', 'Se quedan': 'skyblue'})
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Se quedan", f"{df[df['Churn']=='No']['tenure'].mean():.1f} meses")
    col2.metric("Se van", f"{df[df['Churn']=='Yes']['tenure'].mean():.1f} meses")

hist_charges = st.checkbox('Mostrar distribución de cargos mensuales')
if hist_charges:
    st.subheader("Cargos mensuales y su impacto en el abandono")
    
    df_plot = df.copy()
    df_plot['Tipo'] = df_plot['Churn'].map({'Yes': 'Se van', 'No': 'Se quedan'})
    
    fig = px.histogram(df_plot, x='MonthlyCharges', color='Tipo',
                       nbins=30,
                       labels={'MonthlyCharges': 'Cargo Mensual ($)', 'Tipo': ''},
                       color_discrete_map={'Se van': 'blue', 'Se quedan': 'skyblue'})
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Se quedan", f"${df[df['Churn']=='No']['MonthlyCharges'].mean():.2f}")
    col2.metric("Se van", f"${df[df['Churn']=='Yes']['MonthlyCharges'].mean():.2f}")

scatter_button = st.button('Mostrar relación entre antigüedad y cargos')
if scatter_button:
    st.subheader("Relación entre antigüedad y cargos mensuales")
    
    df_plot = df.copy()
    df_plot['Tipo'] = df_plot['Churn'].map({'Yes': 'Se van', 'No': 'Se quedan'})
    
    fig = px.scatter(df_plot, x='tenure', y='MonthlyCharges', color='Tipo',
                     labels={'tenure': 'Meses como cliente', 
                             'MonthlyCharges': 'Cargo Mensual ($)',
                             'Tipo': ''},
                     color_discrete_map={'Se van': 'blue', 'Se quedan': 'skyblue'})
    st.plotly_chart(fig, use_container_width=True)

bar_contract = st.checkbox('Mostrar impacto del tipo de contrato')
if bar_contract:
    st.subheader("Tipo de contrato como predictor de churn")
    
    churn_by_contract = pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100
    churn_by_contract_melted = churn_by_contract.reset_index().melt(id_vars='Contract', 
                                                                      var_name='Tipo',
                                                                      value_name='Porcentaje')
    
    fig = px.bar(churn_by_contract_melted, x='Contract', y='Porcentaje', color='Tipo',
                 barmode='group',
                 labels={'Contract': 'Tipo de Contrato', 'Porcentaje': 'Porcentaje (%)'},
                 color_discrete_map={'Yes': 'blue', 'No': 'skyblue'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Los contratos Month-to-month tienen 42.7% de churn vs 2.8% de los bianuales")

st.divider()


st.header("Segmento de Ultra-Alto Riesgo")

st.markdown("Perfil crítico: Clientes con contratos mensuales, cargos superiores a $70 y antigüedad menor a 12 meses")

contratos_mensuales = df[df['Contract'] == 'Month-to-month']
combo_peligroso = contratos_mensuales[
    (contratos_mensuales['MonthlyCharges'] > 70) & 
    (contratos_mensuales['tenure'] < 12)
]

total_combo = len(combo_peligroso)
se_van_combo = len(combo_peligroso[combo_peligroso['Churn'] == 'Yes'])
tasa_churn_combo = (se_van_combo / total_combo) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Clientes en este segmento", f"{total_combo}")
col2.metric("Ya se fueron", f"{se_van_combo}")
col3.metric("Tasa de Churn", f"{tasa_churn_combo:.1f}%")

st.info(f"Este segmento tiene {tasa_churn_combo / churn_rate:.1f}x más churn que el promedio general")

st.divider()

st.header("Conclusiones")

st.markdown("""
- Priorizar una conversión a contratos largos mediante incentivos para migrar customers Month-to-month hacia compromisos anuales o bianuales
- Buscar e implementar forma de retención temprana con intervención activa durante los primeros 6 a 12 meses
- Revisar propuesta de valor premium para evaluar si los planes superiores a $70 justifican su precio
- Focalizar recursos en los 814 clientes de alto riesgo que requieren atención inmediata
"""
)
st.success("En Telco, los customers siguen un patrón que los conduce a Churn. La compañía tiene la oportunidad de identificar estas circunstancias y actuar con estrategias proactivas para mitigar ésta pérdida de valuable customers ")