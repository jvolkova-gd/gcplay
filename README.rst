Before work with project - generate your own GCC auth key::

    https://cloud.google.com/pubsub/docs/reference/libraries

After git clone if you have such error "ModuleNotFoundError: No module named 'gcplay'"::

    export PYTHONPATH=${PYTHONPATH}:/path/to/project/gcplay

where gcplay folder with README.rst file, not python package folder

Set your path to GCC auth key in conf.ini::

    ./config/conf.ini
    "~/" - it's a HOME dir path


Run only publisher (to generates events in Topic) from main project folder with::

    python /path/to/project/gcplay/gcplay/publisher.py


Run subscriber and publisher::

    python /path/to/project/gcplay/gcplay/subscriber.py

It will send output to console with messages

