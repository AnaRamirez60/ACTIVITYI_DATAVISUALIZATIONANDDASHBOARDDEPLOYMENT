import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("university_student_data.csv")

st.set_page_config(
    page_title="DATA VISUALIZATION AND DASHBOARD DEPLOYMENT",
    layout="wide"
)

# Titulo del dashboard
st.title("DATA VISUALIZATION AND DASHBOARD DEPLOYMENT")
st.markdown("Analisis y visualización de datos de estudiantes universitarios")

# Analisis exploratorio del dataset
st.header("Analisis exploratorio del dataset")

with st.expander("Analisis exploratorio del dataset"):
    st.subheader("Dataset Info")
    
    # Mostrar información básica del dataset
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Number of Rows", df.shape[0])
    with col2:
        st.metric("Number of Columns", df.shape[1])
    with col3:
        st.metric("Data Types", f"{len(df.dtypes.unique())} unique types")
    
    # Mostrar tipos de datos
    st.subheader("Data Types")
    dtype_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum()
    })
    st.dataframe(dtype_info)
    
    # Mostrar estadísticas descriptivas
    st.subheader("Estadísticas descriptivas")
    st.dataframe(df.describe())
    
    # Mostrar primeras filas
    st.subheader("Primeras 5 Filas")
    st.dataframe(df.head())

# Preprocesar datos 
def process_data(df):
    id_cols = ['Year', 'Term']
    
    # Columnas de enrollment por departamento
    enrolled_cols = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
    
    df_enrollment = df.melt(
        id_vars=id_cols,
        value_vars=enrolled_cols,
        var_name='Department',
        value_name='Enrollment'
    )
    df_enrollment['Department'] = df_enrollment['Department'].str.replace(' Enrolled', '')
    
    df_retention = df.melt(
        id_vars=id_cols,
        value_vars=['Retention Rate (%)'],  
        var_name='Department',
        value_name='Retention Rate'
    )
    # Crear una fila por cada departamento con la misma tasa de retención
    retention_expanded = []
    for dept in ['Engineering', 'Business', 'Arts', 'Science']:
        temp_df = df_retention.copy()
        temp_df['Department'] = dept
        retention_expanded.append(temp_df)
    df_retention = pd.concat(retention_expanded, ignore_index=True)
    
    df_satisfaction = df.melt(
        id_vars=id_cols,
        value_vars=['Student Satisfaction (%)'],  
        var_name='Department',
        value_name='Satisfaction Score'
    )
    # Crear una fila por cada departamento con la misma satisfacción
    satisfaction_expanded = []
    for dept in ['Engineering', 'Business', 'Arts', 'Science']:
        temp_df = df_satisfaction.copy()
        temp_df['Department'] = dept
        satisfaction_expanded.append(temp_df)
    df_satisfaction = pd.concat(satisfaction_expanded, ignore_index=True)
    
    return df_enrollment, df_retention, df_satisfaction

df_enrollment, df_retention, df_satisfaction = process_data(df)

# Filtros
st.sidebar.header("Filtros")

# Filtro por año
available_years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Seleccionar Años:",
    options=available_years,
    default=available_years
)

# Filtro por trimestre
available_terms = df['Term'].unique().tolist()
selected_terms = st.sidebar.multiselect(
    "Seleccionar Trimestres:",
    options=available_terms,
    default=available_terms
)

# Filtro por departamento
available_departments = ['Engineering', 'Business', 'Arts', 'Science']
selected_departments = st.sidebar.multiselect(
    "Seleccionar Departamentos:",
    options=available_departments,
    default=available_departments
)

# Filtrar datos
def filter_data(df, years, terms, departments):
    filtered_df = df[
        (df['Year'].isin(years)) & 
        (df['Term'].isin(terms)) &
        (df['Department'].isin(departments))
    ]
    return filtered_df

filtered_enrollment = filter_data(df_enrollment, selected_years, selected_terms, selected_departments)
filtered_retention = filter_data(df_retention, selected_years, selected_terms, selected_departments)
filtered_satisfaction = filter_data(df_satisfaction, selected_years, selected_terms, selected_departments)

# Visualizaciones

# KPI
st.header("KPI")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_enrollment = filtered_enrollment['Enrollment'].sum()
    st.metric("Total Estudiantes Inscritos", f"{total_enrollment:,}")

with col2:
    avg_retention = filtered_retention['Retention Rate'].mean()
    st.metric("Tasa de Retención Promedio", f"{avg_retention:.1f}%")

with col3:
    avg_satisfaction = filtered_satisfaction['Satisfaction Score'].mean()
    st.metric("Satisfacción Promedio", f"{avg_satisfaction:.1f}%")

with col4:
    spring_enrollment = filtered_enrollment[filtered_enrollment['Term'] == 'Spring']['Enrollment'].sum()
    fall_enrollment = filtered_enrollment[filtered_enrollment['Term'] == 'Fall']['Enrollment'].sum()
    total_enrollment_term = spring_enrollment + fall_enrollment
    if total_enrollment_term > 0:
        spring_ratio = (spring_enrollment / total_enrollment_term) * 100
        st.metric("Ratio Spring/Fall", f"{spring_ratio:.1f}%")

# Enrollment con Retention
col1, col2 = st.columns(2)

with col1:
    st.subheader("Estudiantes Inscritos por Departamento")
    
    enrollment_by_year_dept = filtered_enrollment.groupby(['Year', 'Department'])['Enrollment'].sum().reset_index()
    
    fig_enrollment = px.bar(
        enrollment_by_year_dept,
        x='Year',
        y='Enrollment',
        color='Department',
        barmode='group',
        title="Estudiantes Inscritos por Departamento y Año"
    )
    fig_enrollment.update_layout(xaxis_type='category')
    st.plotly_chart(fig_enrollment, use_container_width=True)

with col2:
    st.subheader("Tasas de Retención por Departamento")
    
    retention_trends = filtered_retention.groupby(['Year', 'Department'])['Retention Rate'].mean().reset_index()
    
    fig_retention = px.line(
        retention_trends,
        x='Year',
        y='Retention Rate',
        color='Department',
        title='Tendencias de Tasa de Retención',
        markers=True
    )
    fig_retention.update_layout(yaxis_title="Tasa de Retención (%)")
    st.plotly_chart(fig_retention, use_container_width=True)

# Satisfacción y comparación de trimestres
col1, col2 = st.columns(2)

with col1:
    st.subheader("Puntuaciones de Satisfacción Estudiantil")

    satisfaction_by_year_dept = filtered_satisfaction.groupby(['Year', 'Department'])['Satisfaction Score'].mean().reset_index()
    
    fig_satisfaction = px.line(
        satisfaction_by_year_dept,
        x='Year',
        y='Satisfaction Score',
        color='Department',
        title='Tendencias de Satisfacción Estudiantil',
        markers=True
    )
    fig_satisfaction.update_layout(yaxis_title="Satisfacción (%)")
    st.plotly_chart(fig_satisfaction, use_container_width=True)

with col2:
    st.subheader("Comparación de Trimestres: Primavera vs Otoño")

    term_enrollment = filtered_enrollment.groupby('Term')['Enrollment'].sum().reset_index()
    
    fig_term = px.pie(
        term_enrollment,
        values='Enrollment',
        names='Term',
        hole=0.4,
        title='Distribución de Inscripciones: Spring vs Fall'
    )
    st.plotly_chart(fig_term, use_container_width=True)

# Análisis adicional
st.header("Análisis Comparativo")

tab1, tab2, tab3 = st.tabs(["Retención por Trimestre", "Satisfacción por Trimestre", "Evolución General"])

with tab1:
    retention_by_term = filtered_retention.groupby(['Term', 'Department'])['Retention Rate'].mean().reset_index()
    fig_retention_term = px.bar(
        retention_by_term,
        x='Department',
        y='Retention Rate',
        color='Term',
        barmode='group',
        title='Tasa de Retención por Departamento y Trimestre'
    )
    fig_retention_term.update_layout(yaxis_title="Tasa de Retención (%)")
    st.plotly_chart(fig_retention_term, use_container_width=True)

with tab2:
    satisfaction_by_term = filtered_satisfaction.groupby(['Term', 'Department'])['Satisfaction Score'].mean().reset_index()
    fig_satisfaction_term = px.bar(
        satisfaction_by_term,
        x='Department',
        y='Satisfaction Score',
        color='Term',
        barmode='group',
        title='Satisfacción por Departamento y Trimestre'
    )
    fig_satisfaction_term.update_layout(yaxis_title="Satisfacción (%)")
    st.plotly_chart(fig_satisfaction_term, use_container_width=True)

with tab3:
    # Evolución de todas las métricas
    fig_evolution = go.Figure()
    
    # Agregar enrollment
    enrollment_evolution = filtered_enrollment.groupby('Year')['Enrollment'].sum().reset_index()
    fig_evolution.add_trace(go.Scatter(
        x=enrollment_evolution['Year'],
        y=enrollment_evolution['Enrollment'],
        name='Total Inscritos',
        line=dict(color='blue')
    ))
    
    # Agregar retención
    retention_evolution = filtered_retention.groupby('Year')['Retention Rate'].mean().reset_index()
    fig_evolution.add_trace(go.Scatter(
        x=retention_evolution['Year'],
        y=retention_evolution['Retention Rate'],
        name='Retención (%)',
        line=dict(color='green'),
        yaxis='y2'
    ))
    
    # Agregar satisfacción
    satisfaction_evolution = filtered_satisfaction.groupby('Year')['Satisfaction Score'].mean().reset_index()
    fig_evolution.add_trace(go.Scatter(
        x=satisfaction_evolution['Year'],
        y=satisfaction_evolution['Satisfaction Score'],
        name='Satisfacción (%)',
        line=dict(color='orange'),
        yaxis='y2'
    ))
    
    fig_evolution.update_layout(
        title='Evolución de Todas las Métricas',
        xaxis=dict(title='Año'),
        yaxis=dict(title='Total Inscritos', side='left'),
        yaxis2=dict(title='Porcentaje (%)', side='right', overlaying='y'),
        showlegend=True
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)

# Data Summary
st.header("Resumen de Datos")

with st.expander("Ver Datos Filtrados"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Datos de Inscripción")
        st.dataframe(filtered_enrollment, use_container_width=True)
    
    with col2:
        st.subheader("Datos de Tasa de Retención")
        st.dataframe(filtered_retention, use_container_width=True)
    
    with col3:
        st.subheader("Datos de Satisfacción")
        st.dataframe(filtered_satisfaction, use_container_width=True)

st.caption("Elaborado por Ana Rosa Ramirez Lopez y Jesus Gabriel Gudiño Lara")
