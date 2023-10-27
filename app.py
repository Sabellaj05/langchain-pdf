import streamlit as st                                           # ui
from dotenv import load_dotenv                                   # env    
from PyPDF2 import PdfReader                                     # read pdf
from langchain.text_splitter import CharacterTextSplitter        # split text
from langchain.embeddings import OpenAIEmbeddings                # embedding de OpenAI
# from langchain.embeddings import HuggingFaceInstructEmbeddings # embeding de HuggingFace
from langchain.vectorstores import FAISS                         # vector store   
from langchain.chat_models import ChatOpenAI                     # llm   
# from langchain.llms import HuggingFaceHub                        # llm local          
from langchain.memory import ConversationBufferMemory            # memory para contexto  
from langchain.chains import ConversationalRetrievalChain        # interaccion Q/A con vector store   
from htmlformat import css, AI_format, user_format       # mas ui

## ---------------------------------------------------------------------------------------------
# Si se quiere usar local con huggingface descomentar en requirements.txt de no haberlo hecho
# e intercambiar llm y embedding de OpenAI en las funciones de vectorstore y conversation chain 
## ---------------------------------------------------------------------------------------------


# --- Extraer texto de los pdfs ---
# convertir todo el texto de todos los pdfs a una single string

def get_pdf_text(pdf_docs):
    text = ""                         # donde se guarda el texto completo
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)   # instaciamos el PdfReader para cada pdf y leemos todas paginas 
        for page in pdf_reader.pages:     # se itera por pagina y saca el texto
            text += page.extract_text()   # se suman todos los textos
    return text  # final string

# --- Separar el texto en "chunks" con un overlap de 200
# Agarramos esa variable con todo el texto y la dividimos en partes

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(   # separamos el texto en pedazos 
        separator="\n",           # criterio de separacion
        chunk_size=1000,          # tamaño de separacion (1000 caracteres) 
        chunk_overlap=200,        # para evitar cortar oraciones a la mitad
        length_function=len       # como medir que son x caracteres, 
                                  ## from docs: "Function that measures the length of given chunks"
    )
    chunks = text_splitter.split_text(text)
    return chunks

# --- Crear la vectorstore ---
# esta db se guarda localmente, no es cloud por lo tanto al cerrar la app se borra todo
## `pendiente modificar y probar con alguna vectorstore en la nube`

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()      # instanciamos 
    # huggingFace para probar local (testeado y frozeada la pc xD)
    ## `pendiente investigar los requisitos`
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    # el nombre viene de la pagina https://huggingface.co/hkunlp/instructor-large
    
    # creamos vectore store y le pasamos los textos, y el modelo 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# --- Logica de conversacion con memoria ---

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()                    # instanciamos llm
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(                         # memoria para responder con contexto
        memory_key='chat_history', return_messages=True)       # hay distintas memory_keys, investigar
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,                                     # llm to use
        retriever=vectorstore.as_retriever(),        # vector store
        memory=memory                                # memoria inicializada anteriormente 
    )
    return conversation_chain

# --- Agarrar el input del user, guardar en la memoria del bot y responder ---
    # Agarramos la variable que ya contiene el text embedido y guardado en vectorstore
    # el objeto contiene keys como: question con la pregunta del user,
    # "answer" con la respuesta de la AI en si,
    # y "chat_history", con con las distintas preguntas del user y respuestas de la AI 

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Iteramos sobre el history y agarramos la pregunta del user que es par y la
    # respuesta de la AI que es impar acorde al index, extraemos el "content" del objeto
    # y formateamos acorde al html, css del user e AI
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_format.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
                                                                   # replace MSG con Q/A
        else:
            st.write(AI_format.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()                                  # load api keys
    st.set_page_config(page_title="Chatpdf",       # page title and icon
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)          # cargamos el css
   
    # inicializamos conversation y history si es que no lo estaban ya
    if "conversation" not in st.session_state:    
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # `Buscar mejores emojis`
    st.header("Chatea con tus PDF's :books:")      # Heading 

    # input para que el usuario pregunte, si hay pregunta calls functions
    user_question = st.text_input("Pregunta acerca de tus documentos:")
    if user_question:
        handle_userinput(user_question)

# --- Sidebar ---
    with st.sidebar:                               # sidebar para cargar y procesar los pdfs
        st.subheader("Tus documentos")
        pdf_docs = st.file_uploader(               # st element para subir archivos, multiples_files = True
            "Subi tus PDF's y toca en 'Procesar'", accept_multiple_files=True)

        if st.button("Procesar"):                  # boton para procesar, <true only if pressed>
            with st.spinner("Procesando"):
                # Extraer texto de los pdfs 
                raw_text = get_pdf_text(pdf_docs)

                # Extraer los pedazos de los pdfs
                text_chunks = get_text_chunks(raw_text)
                # para probar, `aparece en la sidebar`
                # st.write(text_chunks)

                # Crear la vector store 
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                # importante usar session_state ya que streamlit suele recargar el codigo ante ciertas interacciones
                # por lo tanto eso borraria nuestra memoria y perderiamos el contexto al momento de hacer multiples preguntas
                # tambien es util para usar la variable fuera del scope en este caso de la sidebar, de lo contrario no se podria
                st.session_state.conversation = get_conversation_chain(vectorstore)       # pasamos como argumento la vector store 


if __name__ == '__main__':
    main()
