import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    return pd.read_csv('telco_customer_churn.csv')

df = load_data()

st.title('Análisis de Churn en Customers de Telco')
st.markdown("Dashboard para identificar clientes en riesgo de Churn")
st.divider()

st.header("Situación actual de Churn en Telco")

col1, col2, col3, col4 = st.columns(4)

total_customers = len(df)
churn_customers = len(df[df['Churn'] == 'Yes'])
churn_rate = (churn_customers / total_customers) * 100
lost_income = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()


col1.metric("Total de Customers", total_customers)
col2.metric("Customers con Churn", churn_customers)
col3.metric("Tasa de churn ", f"{churn_rate:.2f}%")
col4.metric("Lost monthly income ", f"${lost_income:.2f}")

st.header("Indicadores cruciales de Churn en Customers")

tab1, tab2, tab3 = st.tabs(["Antigüedad", "Cargos Mensuales", "Tipo de Contrato"])

with tab1:
    st.subheader("Antigüedad del cliente y su relación con el churn")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(df[df['Churn']=='No']['tenure'], bins=30, alpha=0.6, label='No Churn', color='blue', edgecolor='black')
    ax.hist(df[df['Churn']=='Yes']['tenure'], bins=30, alpha=0.6, label='Churn', color='skyblue', edgecolor='black')
    ax.set_xlabel('Meses como cliente')
    ax.set_ylabel('Frecuencia')
    ax.legend()
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    col1.metric("Se quedan", f"{df[df['Churn']=='No']['tenure'].mean():.1f} meses")
    col2.metric("Se van", f"{df[df['Churn']=='Yes']['tenure'].mean():.1f} meses")

with tab2:
    st.subheader("Cargos mensuales y su impacto en el abandono")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(df[df['Churn']=='No']['MonthlyCharges'], bins=30, alpha=0.6, label='No Churn', edgecolor='black')
    ax.hist(df[df['Churn']=='Yes']['MonthlyCharges'], bins=30, alpha=0.6, label='Churn', edgecolor='black')
    ax.set_xlabel('Cargo Mensual ($)')
    ax.set_ylabel('Frecuencia')
    ax.legend()
    st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    col1.metric("Se quedan", f"${df[df['Churn']=='No']['MonthlyCharges'].mean():.2f}")
    col2.metric("Se van", f"${df[df['Churn']=='Yes']['MonthlyCharges'].mean():.2f}")

with tab3:
    st.subheader("Tipo de contrato como predictor de churn")
    
    churn_by_contract = pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100
    
    fig, ax = plt.subplots(figsize=(8, 4))
    churn_by_contract.plot(kind='bar', ax=ax, edgecolor='black')
    ax.set_xlabel('Tipo de Contrato')
    ax.set_ylabel('Porcentaje ')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(['No Churn', 'Churn'])
    st.pyplot(fig)
    
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