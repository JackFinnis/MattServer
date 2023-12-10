# Matt Server

pip freeze > requirements.txt
[15] europe-west1
gcloud run deploy
python3.11 -m venv env
source env/bin/activate
testing-54a06
gcloud builds submit --tag gcr.io/testing-54a06/matt
gcloud run deploy --image gcr.io/testing-54a06/matt

gcloud functions deploy detect_new_cartoon --trigger-topic=detect_new_cartoon --region=europe-west1 --runtime=python311 --docker-registry=artifact-registry
