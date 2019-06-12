Camping Kafka Game Engine
=========================

This repository contains the game engine used by the online adventure
game [Camping Kafka](https://www.campingkafka.nl/game/). The `game`
module contains the Django models, views and templates, as well as a
nice visual graph editor based on [Graphviz](https://www.graphviz.org/).

To get up and running, install Python 3 and run the following commands:

     python -m venv ~/.virtualenvs/kafka
     . ~/.virtualenvs/kafka/bin/activate
     pip install -r requirements.txt
     ./manage.py migrate
     ./manage.py createsuperuser
     ./manage.py runserver

Then point your webbrowser to http://localhost:8000/admin/ and add
some content! The visual graph editor can be found at
http://localhost:8000/game/graph/

Have fun :)