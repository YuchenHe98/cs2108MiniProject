# cs2108MiniProject
## Requirements
1. Python 3
2. Anaconda installed with default env(root) https://www.anaconda.com/download
3. flask-sqlalchemy

## Install flask if it is not already installed
``` bash
# type inside terminal
conda install -c anaconda flask 
```

## Install flask-sqlalchemy for simple database

``` bash
conda install -c conda-forge flask-sqlalchemy 
```

## How to regenerate test data
1. open database.db using a sqlite tool
2. copy everything inside seedAll.sql 
3. paste under 'query'

## How to run 
``` bash
# type inside terminal 
python app.py
# and then open browser at http://127.0.0.1:5000/, make sure that port is not being used
```

