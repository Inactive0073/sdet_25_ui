# Jenkins + Docker Compose setup

1. Сборка и запуск проекта:
   `docker compose up -d --build jenkins`
2. Откройте `http://localhost:8080`.
3. Авторизуйтесь `admin` / `admin`.
4. Запустите job\`у `bankingproject-ui-tests`.

Содержание:

- Jenkins controller with Docker CLI и Compose plugin.
- Seeded pipeline job from `Jenkinsfile`.
- Dockerized Python test runner.
- Selenoid and Selenoid UI for remote browser sessions.

Notes:

- Docker Desktop should run Linux containers.
- Test execution starts `autotests`, `selenoid`, and `selenoid-ui` together from the Jenkins pipeline.
- Allure raw results are copied to `allure-results/` and archived by Jenkins for each build.
