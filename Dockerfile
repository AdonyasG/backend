FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SPOTIFY_CLIENT_ID="c69241eaef7445cea1c2ce5b0bee3193"
ENV SPOTIFY_CLIENT_SECRET="b5afe5079c364db6837a013f27946c7c"
ENV SPOTIFY_REDIRECT_URI="http://localhost:8000/callback"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]