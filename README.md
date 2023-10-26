# Chatear con PDFs

## LangChain y OpenAI

> Detallar mejor el paso a paso

- Crear python venv
- Instalar dependencies del `requirements.txt`
- añadir `.env` file
- Tener una API key de OpenAI para usar y agregarla `.env`
- Para usar `streamlit run app.py`

## Explicacion simplificada

La idea general es cargar archivos pdfs, pueden ser varios, y poder escribir una pregunta  
y tener una respuesta acorde al contenido de los pdfs.

Basicamente lo que ocurre es:

- Primero se crea un *Embedding* del texto de nuestra pregunta, en corta se convierte en un vector
- Se guardan ese vector en una *Base de datos vectoriales* en este caso `FAISS`
- Tambien se crea una memoria para ir guardando las consecuentes preguntas y respuesta para mayor contexto
- Y con esa informacion se la pasamos al `LLM` o *Large Language Model* en este caso de OpenAI para que responda

Se puede usar localmente instalando un *Embedding* y *LLM* de HuggingFace en vez de OpenAI  
En el `requirements.txt` y en `app.py` ambas opciones de HuggingFace estan comentadas pero pueden ser intercambiadas  
con las de OpenAI para usarlo gratis (Si es que la pc aguanta)



