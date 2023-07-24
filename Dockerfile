FROM python:3.9.4

# COPY SCRIPTS TO IMAGES
RUN mkdir app
COPY /src ./app/src
COPY /images ./app/images
COPY config.py ./app/config.py
COPY /styling ./app/styling


WORKDIR ./app

COPY requirements.txt requirements.txt

# SET PYTHON PATH
ENV PYTHONPATH "${PYTHONPATH}:."
ENV ROOT_DIR "."

# INSTALL REQUIREMENTS
# Mount a volume to cache intalled packaged
# and save time when building the image again
RUN pip install -r requirements.txt

# EXPOSE PORT
EXPOSE 8501

# COMMAND
# CMD echo OPENAI_API_KEY > /app/.env
CMD ["streamlit","run","src/home.py","--server.port=8501","--server.address=0.0.0.0"]
