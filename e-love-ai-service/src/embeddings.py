import torch
from sentence_transformers import SentenceTransformer, util
from transformers import BertModel, BertTokenizer

# Initialize models
# TODO: refactor - magic strings (put them in config)
model_name = "bert-base-uncased"
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = BertTokenizer.from_pretrained(model_name)
bert_model = BertModel.from_pretrained(model_name)


def get_bert_embeddings(texts, model=bert_model, tokenizer=tokenizer, pooling="cls"):
    """
    Get BERT embeddings for the given texts.
    params:
        texts: list
            A list of texts to get embeddings for
        model: BertModel
            The BERT model to use for embeddings
        tokenizer: BertTokenizer
            The tokenizer to use for tokenizing the texts
        pooling: str
            The pooling strategy to use for the embeddings
    returns:
        torch.Tensor: The BERT embeddings for the given texts
    """
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    if pooling == "cls":
        return outputs.last_hidden_state[:, 0, :]
    elif pooling == "mean":
        return outputs.last_hidden_state.mean(dim=1)
    else:
        raise ValueError(f"Invalid pooling strategy: {pooling}")


def weighted_sbert_embeddings(texts, keywords=None):
    """
    Get weighted SBERT embeddings for the given texts.
    params:
        texts: list
            A list of texts to get embeddings for
        keywords: list
            A list of keywords to use for weighting the embeddings
    returns:
        torch.Tensor: The weighted SBERT embeddings for the given texts
    """
    if keywords:
        for idx, text in enumerate(texts):
            for keyword, weight in keywords.items():
                if keyword.lower() in text.lower():
                    embeddings[idx] += weight * embeddings[idx]

    return embeddings


def text_similarity_sbert(user_description, new_descriptions, keywords=None):
    """
    Calculate the similarity between the user description and new descriptions using SBERT embeddings.
    params:
        user_description: str
            The user description to compare against
        new_descriptions: list
            A list of new descriptions to compare
        keywords: dict
            A dictionary of keywords and their weights for weighting the embeddings
    returns:
        np.ndarray: The similarity scores between the user description and new descriptions
    """
    user_embedding = weighted_sbert_embeddings([user_description], keywords)
    new_embeddings = weighted_sbert_embeddings(new_descriptions, keywords)
    similarity_scores = util.pytorch_cos_sim(user_embedding, new_embeddings).squeeze(0)
    return similarity_scores.cpu().numpy()
