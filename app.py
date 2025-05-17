from flask import Flask, render_template, request, jsonify
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Initialize embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Initialize vector store (will be populated with documents)
vector_store = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read and process the document
    content = file.read().decode('utf-8')
    texts = text_splitter.split_text(content)
    
    # Update vector store with new document
    global vector_store
    if vector_store is None:
        vector_store = Chroma.from_texts(texts, embeddings)
    else:
        vector_store.add_texts(texts)
    
    return jsonify({'message': 'Document processed successfully'})

@app.route('/compose', methods=['POST'])
def compose_email():
    try:
        data = request.json
        context = data.get('context', '')
        recipient = data.get('recipient', '')
        subject = data.get('subject', '')
        
        # Check if HuggingFace API token is set
        if not os.getenv('HUGGINGFACE_API_TOKEN'):
            logger.error("HUGGINGFACE_API_TOKEN not found in environment variables")
            return jsonify({'error': 'HuggingFace API token not configured'}), 500
        
        # Retrieve relevant context from vector store
        if vector_store:
            relevant_docs = vector_store.similarity_search(context, k=3)
            context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # Generate email using LLM
        try:
            llm = HuggingFaceHub(
                repo_id="google/flan-t5-base",
                model_kwargs={"temperature": 0.7, "max_length": 512}
            )
            prompt = f"""Based on the following context and requirements, write a professional email:
            Context: {context}
            Recipient: {recipient}
            Subject: {subject}
            Write a professional email that incorporates relevant information from the context."""
            
            response = llm(prompt)
            
            return jsonify({
                'draft': response,
                'context_used': context
            })
        except Exception as e:
            logger.error(f"Error calling HuggingFace API: {str(e)}")
            return jsonify({'error': f'Error generating email: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in compose_email: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 