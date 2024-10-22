from django.http import JsonResponse
from rest_framework.decorators import api_view
from fuzzywuzzy import process
import spacy
from sentence_transformers import SentenceTransformer, util
import json
from django.conf import settings  # Import the settings to access BASE_DIR
import os

# Specify the file path to your JSON file
file_path = os.path.join(settings.BASE_DIR, r'.\faq\faqs.json')

# Open the JSON file and load the data into an object
with open(file_path, 'r') as file:
    faq_data = json.load(file)

# Load spaCy model and SentenceTransformer model
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

faq_list = []
for category, entries in faq_data.items():
    for entry in entries:
        faq_list.append({
            "category": category,
            "question": entry["question"],
            "answer": entry["answer"]
        })

def nlp_preprocessing(query: str):
    doc = nlp(query.lower())
    keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return keywords

def search_by_fuzzy_match(query: str):
    questions = [faq["question"] for faq in faq_list]
    best_match = process.extractOne(query, questions)
    if best_match:
        return best_match
    return None

def search_by_sbert(query: str):
    faq_questions = [faq["question"] for faq in faq_list]
    query_embedding = model.encode(query, convert_to_tensor=True)
    faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, faq_embeddings)
    best_match_index = similarities.argmax().item()
    return faq_list[best_match_index]

@api_view(['POST'])
def search_faq(request):
    query = request.data.get('query', '')
    # keywords = nlp_preprocessing(query)
    matched_question = search_by_fuzzy_match(query)

    if matched_question and matched_question[1] > 90:
        for faq in faq_list:
            if faq["question"] == matched_question[0]:
                return JsonResponse({
                    "question": faq["question"],
                    "answer": faq["answer"],
                    "category": faq["category"],
                    "matched_by": "fuzzy_matching",
                    "match_score": matched_question[1]
                })
    else:
        matched_faq = search_by_sbert(query)
        if matched_faq:
            return JsonResponse({
                "question": matched_faq["question"],
                "answer": matched_faq["answer"],
                "category": matched_faq["category"],
                "matched_by": "context_matching"
            })

    return JsonResponse({"message": "No matching FAQ found"})
# Create your views here.
