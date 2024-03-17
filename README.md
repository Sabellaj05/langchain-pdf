# Chatear con PDFs

> Testeado con Python 3.11.4

- Crear python venv `python3 -m venv <nombre>`
- Activarlo `. /venv/bin/activate` Bash, `/venv/bin/Activate.Ps1` PS
- Instalar dependencies  `pip3 install -r requirements.txt`
- Renombrar `.env.example` a `.env`
- Tener una API key de OpenAI (y HuggingFace) para usar y agregarla al `.env`
- Para usar run: `streamlit run app.py`

## Explicacion simplificada

La idea general es cargar archivos pdfs, pueden ser varios, y poder escribir una pregunta  
y tener una respuesta acorde al contenido de los pdfs y las preguntas y respuestas previas durante la interaccion 

Basicamente lo que ocurre es:

- Primero se extraen y separan los textos de los pdfs y se unifican en una sola string
- Se crea un *Embedding* de todo el texto y se guarda en una *Base de datos Vectoriales* en este caso `FAISS`
- Tambien se crea una memoria para ir guardando las consecuentes preguntas y respuesta para mayor contexto
- Al momento de hacer una pregunta tambien se crea un *Embedding*, en corta es convertir texto a un vector  
- Con esa informacion se la pasamos al `LLM` en este caso de OpenAI para que responda con contexto de los pdfs, preguntas previas del usuarios y respuesta previas de la misma AI

Se puede usar localmente instalando un *Embedding* y *LLM* de HuggingFace en vez de OpenAI.  
En el `requirements.txt` y en `app.py` ambas opciones de HuggingFace estan comentadas pero pueden ser intercambiadas con las de OpenAI para usarlo gratis localmente o usar [Google Colab](https://colab.google)



