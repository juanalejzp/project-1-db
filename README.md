Create and activate Python virtual environment
python -m venv venv
source .\venv\Scripts\Activate
Install dependencies
Create file requirements.txt

pip install -r requirements.txt
Run streamlit project
streamlit run app.py
Utilities
Steps to remove virtual environment
deactivate
rm -rf venv
