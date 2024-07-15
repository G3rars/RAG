import os
import json
from langdetect import detect
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.response_synthesizers import TreeSummarize
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
    PromptTemplate,
)

# Definimos las rutas absolutas para tener mejor acceso.
current_dir = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(current_dir, "storage")
DATA_DIR = os.path.join(current_dir, "../data")
LLM_CONFIG_PATH = os.path.join(current_dir, "llmConfig.json")
JSON_RES = os.path.join(current_dir, "../test.json")

file_list = '\n'.join(os.listdir(DATA_DIR))
# Abrimos el JSON con la configuracion del LLM
with open(LLM_CONFIG_PATH, 'r') as file:
    llmConfig = json.load(file)

summarizer_prompt_template = (
    "Please summarize the following information in {language}:\n"
    "--------------------------\n"
    "{text}\n"
    "--------------------------\n"
    "The summary must be provided in the specified language."
)
# Definimos como un prompt o agente (hipoteticamente) para darle ordenes al LLM
template = (
    "We have provided context information below. \n"
    "--------------------------\n"
    "{context_str}"
    "\n--------------------------\n"
    "You are an expert in human resources, your mission is to evaluate the candidates based on the job position\n"
    "Job position: {query_str}\n"
    "You should evaluate every detail of all CVs and score whether the candidates are suitable for the position or "
    "not\n"
    f"The candidates files is:\n"
    f"{file_list}\n"
    "You should return all responses in JSON format as follows:\n"
    "[\n"
    "{{\n"
    "    'candidate': 'Candidate 1',\n"
    "    'name': 'name of the Candidate in CV',\n"
    "    'experience': 'a more suitable experience from the CV for the position',\n"
    "    'score': 'a score from 1 to 10, based on the job criteria'\n"
    "}}\n"
)
qa_template = PromptTemplate(template)
# Cargamos la configuracion del LLM, los valores por defecto son mas que suficientes
# Pero mejor tener cargados parametros planos, por si esos valores la libreria los cambiase
print(llmConfig)
Settings.llm = OpenAI(
    model=llmConfig["model"],
    temperature=llmConfig["temperature"],
    max_tokens=llmConfig["max_tokens"],
    top_p=llmConfig["top_p"],
    frequency_penalty=llmConfig["frequency_penalty"],
    presence_penalty=llmConfig['presence_penalty']
)
# Elegimos el motor de embedding
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small", embed_batch_size=100
)
# configura un objeto `SentenceSplitter` que se utilizará para dividir un texto largo en trozos (chunks) más pequeños, cada uno de hasta 1024 caracteres de longitud.
Settings.text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
summarizer = TreeSummarize(verbose=True)

language_names = {
    'en': 'English',
    'es': 'Spanish',
    # Agrega más abreviaturas y nombres de idiomas según sea necesario
}


# La funcion para crear y consultar la base de datos vectorizada
# Definir la función asíncrona query
# Definir la función asíncrona query
async def query(query_user):
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine(similarity_top_k=2)
    results = query_engine.query(query_user)

    # Seleccionar el nodo con la tasa de acierto más alta
    best_node = max(results.source_nodes, key=lambda result: result.score).node
    # Detect the language of the text
    language_code = detect(best_node.text)
    language_name = language_names.get(language_code, 'English')

    summarizer_prompt = summarizer_prompt_template.format(text=best_node.text, language=language_name)
    # Crear un resumen del nodo seleccionado
    summary = await summarizer.aget_response(query_user, summarizer_prompt)
    context = f"Context:\n{summary}\n"

    prompt = qa_template.format(context_str=context, query_str=query_user)

    response = query_engine.query(prompt)

    return response
