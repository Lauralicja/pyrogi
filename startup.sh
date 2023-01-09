docker compose down
docker build . -f docker/pyrogi.Dockerfile -t pyrogi
docker build . -f docker/generator.Dockerfile -t mocker
docker compose up -d