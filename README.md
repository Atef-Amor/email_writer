# Smart Email Composer

A context-aware email writing assistant that uses RAG (Retrieval Augmented Generation) to help compose personalized emails based on previous correspondences and relevant documents.

## Features

- Upload and index documents for context
- Generate context-aware email drafts
- Modern, responsive user interface
- Integration with HuggingFace's free LLM API
- Document similarity search for relevant context

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd email_writer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your HuggingFace API token:
```
HUGGINGFACE_API_TOKEN=your_token_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Upload relevant documents (PDF, TXT, DOC, DOCX) that contain context for your emails
2. Enter the recipient's email address and subject
3. Add any additional context or requirements in the context field
4. Click "Generate Email Draft" to create a context-aware email
5. Review and edit the generated email as needed

## Technical Details

- Built with Flask for the backend
- Uses LangChain for RAG implementation
- ChromaDB for vector storage
- HuggingFace's sentence-transformers for embeddings
- Modern UI with Tailwind CSS
- Responsive design for all devices

## Contributing

Feel free to submit issues and enhancement requests! 