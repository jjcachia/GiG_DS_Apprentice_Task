import re
import string
import contractions
from unidecode import unidecode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
abbreviation_map = {
    "gig": "gaming innovation group", 
    "sql": "structured query language",
    "kpi": "key performance indicator",
    "kpis": "key performance indicators",
    "gre": "game recommendation engine",
    "rtp": "return to player",
    "atpu": "average time per user",
}

def prepare_text(text, remove_numbers=False, remove_stopwords=True, apply_lemmantization=True, remove_contractions=True, remove_abbreviations=True):
    """Prepares a string of text for search/matching"""
    
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    # Clean the text (convert to lowercase, remove accents, punctuation, and special characters)
    cleaned_text = clean_text(text, remove_numbers=remove_numbers)

    # Optional: Expand abbreviations (e.g., "gig" → "gaming innovation group")
    if remove_abbreviations:
        pattern = r'\b(' + '|'.join(re.escape(key) for key in abbreviation_map.keys()) + r')\b'
        cleaned_text = re.sub(pattern, lambda x: abbreviation_map[x.group()], cleaned_text)

    # Optional: Expand contractions (e.g., "don't" → "do not", "it's" → "it is")
    if remove_contractions:
        cleaned_text = contractions.fix(cleaned_text) 

    # Split the processed text into tokens
    tokenized_text = word_tokenize(cleaned_text)

    # Optional: Remove Stopwords (e.g., and, or, but, etc.) from tokens 
    if remove_stopwords:
        tokenized_text = [word for word in tokenized_text if word not in stop_words]

    # Optional: Lemmatize the tokens (e.g., running → run, better → good)
    if apply_lemmantization:
        tokenized_text = _lemmantize_tokens(tokenized_text)

    return tokenized_text

def clean_text(text, remove_numbers=False):
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    # Normalize unicode characters (e.g., café → cafe)
    text = unidecode(text)

    # Convert to lowercase
    text = text.lower()

    # Create a set of characters to remove
    chars_to_remove = set()

    # Add punctuation characters to the set
    chars_to_remove = chars_to_remove.union(set(string.punctuation))

    # Add whitespace characters (excluding a single space) to the set
    chars_to_remove = chars_to_remove.union(set(string.whitespace) - {' '})

    # Optional: Add numbers to the set
    chars_to_remove = chars_to_remove.union(set(string.digits)) if remove_numbers else chars_to_remove

    # Remove the set of characters from the text
    translation_table = str.maketrans('', '', ''.join(chars_to_remove))
    text = text.translate(translation_table)

    # Strip leading and trailing white spaces
    text = text.strip()

    return text

def _get_wordnet_pos(tag):
    """ Converts NLTK POS tags to WordNet POS tags. """
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN 

def _lemmantize_tokens(tokens):
    """Lemmatizes a list of tokens using WordNet lemmatization."""
    pos_tags = pos_tag(tokens)
    return [lemmatizer.lemmatize(token, _get_wordnet_pos(tag)) for token, tag in pos_tags]

