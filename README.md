# Clone the repository
git clone https://github.com/KarthikaRajagopal44/Project_Doc_Rag.git

cd Project_Doc_Rag

# Create a virtual environment
python -m venv venv

source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload

