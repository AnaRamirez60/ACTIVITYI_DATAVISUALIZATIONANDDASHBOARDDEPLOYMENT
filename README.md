## PARA EJECUTAR streamlit run app.py

## Ana Rosa Ramirez Lopez
## Jesus Gabriel Gudiño Lara

## Descripción del Proyecto

Este proyecto es un dashboard interactivo desarrollado en Streamlit para visualizar y analizar datos de admisiones, retención y satisfacción estudiantil en una universidad. Proporciona insights clave sobre el desempeño académico a lo largo del tiempo y entre diferentes departamentos.

## Objetivos

- Analizar tendencias de retención estudiantil a lo largo del tiempo
- Evaluar la satisfacción estudiantil por año académico
- Comparar el desempeño entre trimestres Spring y Fall
- Visualizar la distribución de estudiantes por departamentos
- Proporcionar métricas clave para la toma de decisiones académicas

## Estructura del Dataset
Columnas Principales

Year (int64): El año académico al que corresponde el registro (ej. 2015, 2016).

Term (object): El período académico dentro del año (Spring o Fall).

Applications (int64): El número total de solicitudes recibidas por la universidad en ese período. Este es un indicador clave del proceso de admisión.

Admitted (int64): El número de solicitantes que recibieron una oferta de admisión.

Enrolled (int64): El número de estudiantes admitidos que aceptaron la oferta y se matricularon. Este es el indicador principal del proceso de matriculación (enrollment).

Retention Rate (%) (int64): Un indicador clave de retención. Representa el porcentaje de estudiantes (probablemente de primer año) que continuaron sus estudios en la universidad al período siguiente (usualmente, del primer al segundo año).

Student Satisfaction (%) (int64): Una métrica clave de satisfacción. Probablemente sea el resultado de encuestas, indicando el porcentaje de estudiantes que reportan estar satisfechos con su experiencia.
s
Engineering Enrolled (int64): El número de estudiantes matriculados (de la columna Enrolled) que ingresaron al departamento de Ingeniería.

Business Enrolled (int64): El número de estudiantes matriculados que ingresaron al departamento de Negocios.

Arts Enrolled (int64): El número de estudiantes matriculados que ingresaron al departamento de Artes.

Science Enrolled (int64): El número de estudiantes matriculados que ingresaron al departamento de Ciencias.

## Características del Dashboard

Filtros Interactivos

- Selección de Años: Filtra datos por rango de años académicos
- Selección de Trimestres: Spring, Fall o ambos
- Selección de Departamentos: Ingeniería, Negocios, Artes, Ciencias

Visualizaciones Principales

- Tendencias de Retención
Gráfico de líneas que muestra la evolución de las tasas de retención por departamento
Análisis comparativo entre trimestres

- Satisfacción Estudiantil
Seguimiento de las puntuaciones de satisfacción por año
Comparación entre departamentos

- Matrículas por Departamento
Gráfico de barras agrupadas mostrando distribución estudiantil
Evolución temporal de las inscripciones
- Comparación Spring vs Fall
Gráfico de donut mostrando distribución entre trimestres
Análisis detallado por departamento
Métricas KPI

- Total de estudiantes inscritos
- Tasa de retención promedio
- Nivel de satisfacción promedio
- Ratio Spring/Fall