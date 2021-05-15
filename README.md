# clip-it
A platform to optimize your bookmarks and more.

## How to run the App

1. Create and activate virtual Enviroment

```bash
python3 -m venv env
```

1.1 Activate Enviroment (Windows)
```bash
./bin/Scripts/activate
```

1.2 Activate Enviroment (Mac or Linux)
```bash
source env/bin/activate
```

2. Download dependencies

```bash
pip install -r requirements.txt
```

3. Set SECRET_KEY

```bash
touch .env
echo "SECRET_KEY=any string" > .env
```

4. Run the server
```bash
python3 manage.py runserver
```
