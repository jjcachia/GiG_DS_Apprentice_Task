## GiG Datascience Apprentice Task

A simple Q&A chatbot designed to answer a small collection of internal documentation snippets. The chatbot, developed for the Data Science Apprenticeship Role at GiG, uses text cleaning, tokenization and a vector-based search (TF-IDF/CountVectorizer and cosine similarity) to retrieve relevant answer snippets based on a users question.

### Project Structure

```
GiG_DS_Apprentice_Task/
├── data/                              # Input and processed datasets
│   ├── gig_docs.csv                   # mock dataset
│   ├── cleaned_gig_docs.csv           # Pandas ready dataset
│   ├── gig_docs_tokenized.pkl         # Tokenized version of question+answer pairs for term frequency search and doc ID for answer retrieval
│   ├── countvector_data.pkl           # CountVectorizer model + matrix for cosine similarity search and doc ID for answer retrieval
│   ├── tfidf_data.pkl                 # TF-IDF vectorizer + matrix for cosine similarity and doc ID for answer retrieval
│
├── notebooks/
│   ├── data-preparation.ipynb         # Notebook detailing the data preparation analysis
│   ├── qa-search-analysis.ipynb       # Notebook detailing the testing of different search and retrieval logic
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── utils.py                       # Text processing functions
│   ├── chatbot.py                     # Chatbot class which uses TF-IDF/term frequency based search
│   ├── chat.py                        # Chat class for session management, tracks chat history
│   ├── user.py                        # User class, tracks user history
│
│── app.py                             # Streamlit web interface for the chatbot 
```

### Running the Project

#### Requirments
- Python 3.12

~~#### Environment Setup (using '.venv')
The project includes a Python virtual environment in '.venv' which is used to run the project.~~

#### Environment Setup (manual)
Create a virtual environment and install dependencies by running the below in terminal

'''
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
'''

#### Preprocessing the Data
The processed data is included in the project, however, running notebooks/data-preparation.ipynb will process and save all necessary data using gig_docs.csv

#### Launching the Web Interfact
Once environment and data is set, the chatbot web interface can be launched by running the below in terminal.

> streamlit run app.py

### Approach and Design Decisions

#### Data Exploration and Preparation

During initial data exploration, it was found that `gig_docs.csv` was not immediately suitable for loading into a Pandas DataFrame. The issue stemmed from unescaped commas in the `Answer_Snippet` column, which caused the answers to be split into multiple columns. To resolve this, the file was processed line-by-line: everything after the third field was grouped and wrapped in quotes before being written into a cleaned CSV file.

This was a realistic challenge, as real-world data is rarely "pandas-ready." Once cleaned, the dataset was loaded and inspected for missing values. Documents missing `Doc_ID` or `Answer_Snippet` were removed, as both are critical for chatbot functionality. Missing `Question_Example` or `Topic` fields were filled with empty strings.

The dataset was then prepared for text-based retrieval. The preprocessing pipeline, inspired by [this article on NLP preprocessing](https://www.geeksforgeeks.org/text-preprocessing-for-nlp-tasks/#regular-expressions), included:
- Lowercasing 
- Removal of special characters and extra whitespaces
- Expansion of abbreviations and contractions using a domain-specific map
- Tokenization and Stopword removal using `nltk`
- Lemmatization using POS tagging and WordNet

Expanding abbreviations was especially important, as the dataset included domain-specific technical terms that might be abbreviated differently in user queries. The goal was to normalize both the user input and the documents to maximize matching quality. A robust preprocessing pipeline was essential—garbage in, garbage out.

#### The Core: A Simple Q&A Function

Early Q&A functions were prototyped in the `qa-search-analysis.ipynb` Jupyter notebook. A key design principle was that both user input and document content should be processed through the same pipeline to ensure meaningful comparisons.

The initial approach used a simple term frequency (TF) match: the number of shared tokens between the user question and each document was counted. However, this method had issues:
- It favored longer answers (due to more word matches)
- It failed on example questions where context mattered more
- It was computationally inefficient due to Python loops

To improve performance, a CountVectorizer + Cosine Similarity-based method was introduced. It worked similarly but stored all document vectors in a matrix, allowing fast cosine similarity comparisons. Despite this, it still lacked depth as word meaning and context weren’t considered.

This led to utilising TF-IDF + Cosine Similarity, which provided better results without significant changes to the code. TF-IDF downweighted common terms and improved the chatbot’s ability to identify more meaningful matches in a computationally efficient way.

#### A Simple Web Interface
Not having much experience developing websites, I was pleased at how developer friendly streamlit was for developing this style of app. 

Though, before developing a the web interface I decided to neatly organize my code into classes. This makes the project, not only nicer to read, but also scalable in the future. Inspiration for the class sctructure was taken from this following blog post https://medium.com/@zarina.kozhurkina/chat-bot-using-python-classes-part-3-02fed72a975b. The chatbot class was first implemented which included the functions analysed in the jupyter notebook, however, a user and chat class were then introduced such that user log and chat history could be maintained, allowing for a user to open multiple chats at once, each having a history of the entire conversation which could be then further used to generate better responses in the future. The website was then design, taking inspiration from a few youtube videos (https://www.youtube.com/watch?v=jYY24eNTYNg, https://www.youtube.com/watch?v=j2WTq82rUr0)

When developing the web interface it was made sure that in the limited scope of the task, it could still be scalable where I to continue working on this. 

#### A Simple Web Interface

Streamlit was chosen for the interface due to its simplicity. Before development, code was refactored into classes to ensure clarity and scalability:
- `Chatbot`: Handles search and retrieval
- `User`: Tracks user identity and history
- `Chat`: Manages a single chat session and conversation log

This structure was inspired by [this tutorial on chatbot architecture](https://medium.com/@zarina.kozhurkina/chat-bot-using-python-classes-part-3-02fed72a975b), and allowed multiple chat sessions to be maintained in parallel, each with its own history.

The interface design was inspired by YouTube tutorials ([source 1](https://www.youtube.com/watch?v=jYY24eNTYNg), [source 2](https://www.youtube.com/watch?v=j2WTq82rUr0)). It includes:
- A user prompt to enter their questions
- A display for chatbot response history
- A sidebar to manage chat sessions

This setup provides a clean user experience which is easy to develop further.

### Challenges and Future Improvements

Although simple on the surface, the task presented realistic challenges, such as working with a messy CSV required problem-solving. However, the main challenge was to stay within scope and to focus on developing a minimal working system first within the time frame given.

Future improvements could include:
- Spelling correction using LLMs or word-distance methods.
- Routing by topic, to filter and search only within relevant document subsets
- Embedding-based search using BERT or other models to capture semantic similarity better than TF-IDF
