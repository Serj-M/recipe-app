# recipe-app

**An application to create a cookbook of recipes.**

**Backend** in Python 3.10 (using FastAPI). I use Pydantic for query validation, Loguru for logging and Pytest. 

For **data storage** I used PostgreSQL (via ORM SQLAlchemy with AsyncSession and Alembic migration). 

For **caching** I configured Redis. 

**Frontend** is developed in Vue.js 3. 

**To run** it all, I configured Docker-compose.

_______________________________________________________________________________________________________________

**Commands to run the application:**

  docker compose up -d --build
  
  docker compose ps

  docker compose exec backend alembic upgrade head    (!!! pause before executing this command)
  
_______________________________________________________________________________________________________________

**URLs:**

  Frontend: http://localhost:8087/

  Backend:  http://localhost:8765

  Swagger:  http://localhost:8765/docs 

_______________________________________________________________________________________________________________

**The application is also hosted and can be accessed via a link:**

  UI:       https://frontend-recipes.onrender.com/ 

  Swagger:  https://recipes-backend-ns4l.onrender.com/docs#/ -  On hosting. Here you can see the available endpoints and descriptions.