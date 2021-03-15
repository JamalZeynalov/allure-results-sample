IMAGE_NAME="$1"
CONTAINER_NAME="test-container"

echo "Cleanup local results"
rm -rf target;
rm -f swagger-coverage-report-petstore.html

echo "Run docker container"
docker run -d -w /allure-results-sample -it --name $CONTAINER_NAME "$IMAGE_NAME"

echo "Setup testing environment in the container"
docker cp . $CONTAINER_NAME:/allure-results-sample/
docker exec -it $CONTAINER_NAME pip install --no-cache-dir -r requirements.txt

echo "Run tests in the container"
docker exec -it $CONTAINER_NAME pytest -s

echo "Copy tests results from the container"
docker cp $CONTAINER_NAME:/allure-results-sample/target/ .
docker cp $CONTAINER_NAME:/allure-results-sample/swagger-coverage-report-petstore.html .

echo "Cleanup"
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME