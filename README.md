# Chatear con PDFs

## LangChain y OpenAI

> To do: Detallar mejor el paso a paso

- Crear python venv
- Instalar dependencies from `requirements.txt`
- añadir `.env` file
- Tener una API key de OpenAI para usar y agregarla a `.env`
- Para usar `streamlit run app.py`

## Explicacion simplificada

La idea general es cargar archivos pdfs, pueden ser varios, y poder escribir una pregunta  
y tener una respuesta acorde al contenido de los pdfs.

Basicamente lo que ocurre es:

- Primero se extraen y separan los textos de los pdfs y se unifican en una sola string
- Se crea un *Embedding* de todo el texto y se guarda en una *Base de datos Vectoriales* en este caso `FAISS`
- Tambien se crea una memoria para ir guardando las consecuentes preguntas y respuesta para mayor contexto
- Al momento de hacer una pregunta tambien se crea un *Embedding*, en corta es convertir texto a un vector  
- Y con esa informacion se la pasamos al `LLM` o *Large Language Model* en este caso de OpenAI para que responda con contexto de los pdfs y preguntas previas del usuarios y respuesta previas de la misma AI

Se puede usar localmente instalando un *Embedding* y *LLM* de HuggingFace en vez de OpenAI.  
En el `requirements.txt` y en `app.py` ambas opciones de HuggingFace estan comentadas pero pueden ser intercambiadas con las de OpenAI para usarlo gratis (Si es que la pc aguanta)



