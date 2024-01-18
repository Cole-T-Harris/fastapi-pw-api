# fastapi-pw-api
Rebuilding an api backend originally built django and building in fastAPI. Fastapi backend is then containerized.

Original Backend Repo: [Original Full Stack Website](https://github.com/Cole-T-Harris/Django-FullStack-Website)

## Getting Started
1. To run the docker image the environment variables `KROGER_OAUTH_CLIENT_ID` and `KROGER_OAUTH_CLIENT_SECRET` must be set with your obtained client id and client secret from kroger. [Kroger API getting started](https://developer.kroger.com/documentation/public/getting-started/quick-start)
2. In this example the environmental variables are stored in a .env file.
3. While in the same directory as the Dockerfile, to build the docker container run the following command `sudo docker build -t grocery-list-fastapi-api .` 
4. To run the built docker image run the following command `sudo docker run -p 8000:80 --env-file .env grocery-list-fastapi-api`
5. The above is to test locally and to verify the application is running properly. Visit http://localhost:8000/docs and test the two api endpoints.
