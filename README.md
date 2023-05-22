# recipe-app
An application to create a cookbook of recipes.  

Backend in Python 3.10 (using FastAPI). I use Pydantic for query validation and Loguru for logging. 
For data storage I used PostgreSQL (via ORM SQLAlchemy and Alembic migration). 
For caching I configured Redis. 
Frontend is developed in Vue.js 3. 
To run it all, I configured Docker-compose.
