# eureka
eureka chat bot interaction

# Instructions

1. Install dependencies
```
pip install -r requirements.txt
```

2. Set up environment variables
in config/.env create a variable ENV=prod and config/.env.prod fill missing variables

3. run alembic migrations
```
alembic upgrade head
```
4. create mysql database

5. Run the app
```
python main.py
```
The should be running on port 8001

To make api calls you need to use the api key in the header X-API-Key with the value set in the SUPERSECRETKEY variable in the config/.env.prod file