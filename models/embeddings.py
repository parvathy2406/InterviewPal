
from sentence_transformers import SentenceTransformer

# Load the model once
_transformer_model = SentenceTransformer(
    'all-MiniLM-L6-v2',
    device='cpu'
)

def get_embeddings(texts):
    return _transformer_model.encode(texts).tolist()
