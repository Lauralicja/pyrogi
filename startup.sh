docker compose down
docker build . -f docker/pyrogi.Dockerfile -t pyrogi --no-cache
docker build . -f docker/consumer.Dockerfile -t consumer --no-cache
docker build . -f docker/generator.Dockerfile -t mocker --no-cache
docker build . -f docker/flask.Dockerfile -t flasky --no-cache
docker compose up -d