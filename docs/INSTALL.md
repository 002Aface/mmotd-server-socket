Development Environment Setup
=============================


**Note:** The plan here is to build a vagrant box to make setup really quick and easy, but until then you'll have to do things manually. Luckily it's not that hard.


Requirements:
-------------

- MongoDB
- Redis
- Python 2.7
- Virtualenv


Steps
-----

- Clone this repository `git clone git@github.com:paddycarey/sockeTD.git`
- Create the virtualenv `mkvirtualenv sockeTD`
- Install the virtualenv `pip install -r requirements.txt`
- Run! `python runserver.py`
