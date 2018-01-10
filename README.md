# Flask app template - RQ

> a simple Flask app template for task queue.
> work for python3
> Thanks to: Miguel Grinberg <Flask Web Development>

For advanced Flask template, check here: https://github.com/kevinqqnj/flask-template-advanced

## Features:
- configurations in `/config.py`
- Flask_Script: manage application, deployment, command line
- Blueprint for main and api, easy for expansion


## Install

``` bash
# git clone
# create virtual env
python3 -m venv venv
source venv/bin/activate
# install python modules
pip3 install -r requirements.txt
```

## Start up
```
python manage.py runserver
```
Bingo! Check app in your web browser at: http://localhost:5000

## deploy to Heroku Server
ready for deploy to [Heroku](https://www.heroku.com)
`Procfile` and `runtime.txt` are included.
```
create app in heroku
git push to heroku
configure env. variables
```
refer to: https://devcenter.heroku.com/articles/getting-started-with-python

## Expansion
For production app, you can easily expand functions as you wish, such as:
- Flask_Compress
- Flask_Cache
- Flask_Redis
- [flask-template-advanced](https://github.com/kevinqqnj/flask-template-advanced)

> For a detailed explanation on how things work, check out the [guide (CHN)](https://www.jianshu.com/p/f37871e31231).
