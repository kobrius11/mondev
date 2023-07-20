export RUN_AS_USER=$(id -un)
export RUN_AS_GROUP=$(id -gn)
docker-compose build
