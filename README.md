<h1>Cars2Go (Used Car Portal) </h1>

cars2go is a web application deployed on heroku platform (https://cars2go.herokuapp.com)
It provides an user interface to search for used cars. The website has various search parameters like car make, model, year, price range etc.
The database currently has used cars infromation from truecar.com and autotrader.com. 
This can be extended to more websites.

The web crawler and scrapper are run locally and database is updated at the heroku platform.
Information about used cars are updated once a week.

<h2> Steps to setup the Web Crawler and running Web App on localhost </h2>
Python Version: *3.9.0*

1. First create a virtual enviorment
    ```
    python -m venv env
    pip install -r requirements.txt
    ```

2. Configure the app settings and DATABASE_URL info in .env file. 
    ```
    source .env 
    ```
    
3. Running web crawler
    ```
    python setup_crawler_truecar.py setup_crawler_autotrader.py
    python reset_db.py
    python crawler_truecar.py crawler_autotrader.py
    ```
    
4. Migrating local database
    ```
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

5. Running web app on localhost (127.0.0.1:5000)
    ```
    python app.py
    ```

