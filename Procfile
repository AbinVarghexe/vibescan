# Heroku Procfile
web: cd web && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60
streamlit: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0