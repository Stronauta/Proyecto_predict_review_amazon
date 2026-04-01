# Amazon Review Analyzer App

Proyecto desarrollado con Flask, MySQL y Machine Learning para clasificar títulos de reseñas de Amazon en español en cinco niveles de sentimiento.

## Descripción

Este proyecto implementa una aplicación web que permite registrar usuarios, iniciar sesión, analizar el sentimiento de un texto y almacenar predicciones en una base de datos MySQL.

El modelo de Machine Learning fue entrenado utilizando un dataset de reseñas de Amazon en español obtenido desde Hugging Face. Para el entrenamiento se utilizó la columna `review_title` como variable independiente y la columna `stars` como variable dependiente.

Las clases del modelo fueron transformadas de la siguiente manera:

* 1 = Muy malo
* 2 = Malo
* 3 = Regular
* 4 = Bueno
* 5 = Excelente

Además del entrenamiento del modelo, el proyecto incluye una aplicación web con autenticación, sesiones y persistencia de predicciones.

---

## Objetivos del proyecto

El proyecto final consistió en cumplir los siguientes pasos:

1. Descargar y cargar el dataset desde Hugging Face.
2. Tomar `review_title` como variable independiente y `stars` como variable dependiente.
3. Reemplazar los valores numéricos de `stars` por sus etiquetas correspondientes.
4. Realizar preprocesamiento de texto.
5. Crear un pipeline con vectorización y entrenamiento del modelo.
6. Evaluar el modelo con `classification_report`.
7. Crear una base de datos MySQL con las tablas `usuarios` y `predicciones`.
8. Crear una aplicación Flask con las rutas `register`, `login`, `predict` y `logout`.
9. Crear las pantallas HTML correspondientes.
10. Guardar y reutilizar el modelo entrenado en formato `.pkl`.

---

## Dataset utilizado

El dataset fue cargado de la siguiente forma:

```python
splits = {
    'train': 'data/train-00000-of-00001.parquet',
    'validation': 'data/validation-00000-of-00001.parquet',
    'test': 'data/test-00000-of-00001.parquet'
}

df = pd.read_parquet("hf://datasets/KRadim/edit_amazon_reviews_multi_es/" + splits["train"])
```

Se utilizó el split de entrenamiento para construir el modelo.

---

## Modelo de Machine Learning

El modelo fue entrenado en un archivo `.ipynb` utilizando:

* Preprocesamiento de texto
* Vectorización con TF-IDF
* Clasificación con LinearSVC

El pipeline entrenado fue exportado en formato `.pkl` para luego ser cargado desde la aplicación Flask.

---

## Base de datos

El proyecto utiliza MySQL con una base de datos llamada `bd_proyecto`.

### Tabla `usuarios`

Campos:

* `id_usuario`
* `nombre`
* `usuario`
* `clave`

### Tabla `predicciones`

Campos:

* `id_predict`
* `texto`
* `prediccion`

---

## Funcionalidades de la aplicación

### Register

Permite registrar un nuevo usuario desde una interfaz HTML y guardar sus datos en la tabla `usuarios`.

### Login

Permite iniciar sesión comparando el usuario y la clave con los registros almacenados en MySQL.
Si las credenciales son correctas, se genera un token JWT bearer que se guarda en `session` y se redirige a la pantalla de predicción.

### Predict

Permite ingresar un texto desde la interfaz HTML.
La aplicación primero verifica si ese texto ya existe en la tabla `predicciones`:

* Si existe, muestra la predicción almacenada.
* Si no existe, utiliza el pipeline entrenado para generar una nueva predicción, la guarda en la base de datos y la muestra en pantalla.

### Logout

Cierra la sesión del usuario, elimina el token de `session` y redirige nuevamente al login.

---

## Estructura del proyecto

```text
amazon-review-sentiment-app/
│
├── Modelo/
│   ├── modelo.ipynb
│   └── pipeline_sentimientos.pkl
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── predict.html
│
├── sql/
│   └── dbproyecto_tarea4.sql
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Tecnologías utilizadas

* Python
* Flask
* Flask-JWT-Extended
* Flask-MySQLdb
* Pandas
* Scikit-learn
* Joblib
* NLTK
* MySQL
* HTML
* CSS

---

## Resultados del modelo

El modelo fue evaluado mediante `classification_report`, cumpliendo el requerimiento del proyecto.
La clasificación se realizó sobre cinco clases de sentimiento:

* Muy malo
* Malo
* Regular
* Bueno
* Excelente

Dado que se trabajó únicamente con `review_title`, algunas clases intermedias presentan mayor dificultad de separación que las clases extremas.

---

## Autor

Samir Ernesto Castillo Paredez
