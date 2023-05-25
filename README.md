# recipe-app

**An application to create a cookbook of recipes.**

Backend in Python 3.10 (using FastAPI). I use Pydantic for query validation and Loguru for logging. 

For data storage I used PostgreSQL (via ORM SQLAlchemy and Alembic migration). 

For caching I configured Redis. 

Frontend is developed in Vue.js 3. 

To run it all, I configured Docker-compose.

**Commands to run the application:**

  docker compose up -d --build

  docker compose exec backend alembic upgrade head    (!!! pause before executing this command)

  docker compose ps

**URLs:**

  Frontend: http://localhost:8087/

  Backend:  http://localhost:8765

  Swagger:  http://localhost:8765/docs 