# Guide
## Setup
Clone Repository<br>
```
git clone https://github.com/CGU-IST-303-Alola/group-project.git
```

Change Directory to Project<br>
```
cd group-project
```

Create & Activate venv<br>
```
python -m venv venv
.\venv\Scripts\activate
```

Install Required Libraries<br>
```
pip install -r requirements.txt
```

## Running
Run flask app using<br>
```
cd app
flask --app ./run.py run
# or 
flask --app ./run.py --debug run
```

## Testing
Run pytests<br>
```
cd app
pytest pytests.py -v
```