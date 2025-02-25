def llm(
    milvus_uri        : str,
    milvus_username   : str,
    milvus_password   : str,
    milvus_collection : str,
    inference_server  : str,
    model_name        : str,
    pvc_directory     : str,
    pvc_filename      : str
):
    """
    Removes the watermark from the pdf file.

    Parameters:
        - pvc_directory    (str)  : The PVC directory where the file is saved.
        - pvc_filename     (str)  : The PVC filename in which the watermark will be removed.
        - remove_watermark (bool) : Flag that indicates whether this step should be executed or not.
    """

    import os
    from langchain.chat_models                   import ChatOpenAI
    from langchain.callbacks.streaming_stdout    import StreamingStdOutCallbackHandler
    from langchain.schema                        import SystemMessage, HumanMessage
    from langchain_community.vectorstores.milvus import Milvus
    from sentence_transformers                   import SentenceTransformer

    class EmbeddingFunctionWrapper:

        def __init__(self, model):
            self.model = model

        def embed_query(self, query):
            return self.model.encode(query)

        def embed_documents(self, documents):
            return self.model.encode(documents)

    embedding_model    = SentenceTransformer('all-MiniLM-L6-v2')
    embedding_function = EmbeddingFunctionWrapper(embedding_model)

    milvus_connection_args = {
        'uri'      : milvus_uri,
        'user'     : milvus_username,
        'password' : milvus_password
    }

    milvus = Milvus(
        connection_args    = milvus_connection_args,
        collection_name    = milvus_collection,
        embedding_function = embedding_function,
        auto_id            = True,
        drop_old           = False
    )

    llm = ChatOpenAI(
        openai_api_key   = 'EMPTY',
        openai_api_base  = f'{inference_server}/v1',
        model_name       = model_name,
        top_p            = 0.92,
        temperature      = 0.01,
        max_tokens       = 512,
        presence_penalty = 1.03,
        streaming        = True,
        callbacks        = [StreamingStdOutCallbackHandler()]
    )

    query = """
        Converter as informações para o formato XML.
    """

    documents = milvus.search(
        query = query,
        k     = 1,
        search_type = 'similarity',
        filter      = {
            'source' : pvc_filename
        }
    )

    context_parts    = [document.page_content for document in documents]
    context_combined = '\n'.join(context_parts)

    messages = [
        SystemMessage(content = """
            Você é um assistente especialista em realizar conversões.
            Seu único objetivo é realizar a conversão das informações apresentadas para o formato XML.
            Sua resposta deve ser apenas o XML resultado, e somente o XML, nenhum comentário ou texto adicional.
        """),
        HumanMessage(content = f"""
            Baseado nas informações abaixo, realize a conversão para o formato XML.
            INPUT:
            {context_combined}
            XML OUTPUT:
        """)
        ]

    response = llm.predict_messages(messages)
    print(response.content)


if __name__ == '__main__':
    """
    Elyra Pipelines
    """

    import os

    llm(
        milvus_uri        = os.getenv('mulvis_uri'),
        milvus_username   = os.getenv('milvus_username'),
        milvus_password   = os.getenv('milvus_password'),
        milvus_collection = os.getenv('milvus_collection'),
        inference_server  = os.getenv('inference_server'),
        model_name        = os.getenv('model_name'),
        pvc_directory     = os.getenv('pvc_directory'),
        pvc_filename      = os.getenv('pvc_filename')
    )
