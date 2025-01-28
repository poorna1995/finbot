FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
COPY .env . 
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src/ src/
RUN mkdir -p /app/db_data

ENV STREAMLIT_SERVER_PORT=8502
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "src/app.py", "--server.address", "0.0.0.0", "--server.port", "8502"]
