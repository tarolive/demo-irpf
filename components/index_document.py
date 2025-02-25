def index_document(
    milvus_host       : str,
    milvus_port       : str,
    milvus_username   : str,
    milvus_password   : str,
    milvus_collection : str,
    pvc_directory     : str,
    pvc_filename      : str
):
    """
    Indexes the document in Milvus.

    Parameters:
        - milvus_host       (str) : The host of the Milvus database.
        - milvus_port       (str) : The port of the Milvus database.
        - milvus_username   (str) : The username of the Milvus for authentication.
        - milvus_password   (str) : The password of the Milvus for authentication.
        - milvus_collection (str) : The Milvus collection where the document will be indexed.
        - pvc_directory     (str) : The PVC directory where the file is saved.
        - pvc_filename      (str) : The PVC filename in which the text will be indexed.
    """

    import os
    from langchain_milvus      import Milvus
    from sentence_transformers import SentenceTransformer

    pvc_filename_txt = os.path.join(pvc_directory, pvc_filename)
    pvc_filename_txt = '{0}_no_watermark.txt'.format(*os.path.splitext(pvc_filename_txt))

    with open(pvc_filename_txt) as file:

        extracted_text = file.read()

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
        'host'     : milvus_host,
        'port'     : milvus_port,
        'user'     : milvus_username,
        'password' : milvus_password,
        'timeout'  : 30
    }

    milvus = Milvus(
        connection_args    = milvus_connection_args,
        collection_name    = milvus_collection,
        metadata_field     = 'metadata',
        text_field         = 'page_content',
        drop_old           = False,
        auto_id            = True,
        embedding_function = embedding_function
    )

    words          = extracted_text.split()
    parts          = []
    current_part   = []
    current_length = 0
    max_length     = 60000

    for word in words:

        if current_length + len(word) + 1 <= max_length:

            current_part.append(word)
            current_length += len(word) + 1

        else:

            parts.append(' '.join(current_part))
            current_part   = [word]
            current_length = len(word) + 1

    if current_part:

        parts.append(' '.join(current_part))

    for index, part in enumerate(parts):

        metadata = {
            'source' : pvc_filename,
            'part'   : index
        }

        milvus.add_texts([part], metadatas = [metadata])


if __name__ == '__main__':
    """
    Elyra Pipelines
    """

    import os

    index_document(
        milvus_host       = os.getenv('milvus_host'),
        milvus_port       = os.getenv('milvus_port'),
        milvus_username   = os.getenv('milvus_username'),
        milvus_password   = os.getenv('milvus_password'),
        milvus_collection = os.getenv('milvus_collection'),
        pvc_directory     = os.getenv('pvc_directory'),
        pvc_filename      = os.getenv('pvc_filename')
    )
