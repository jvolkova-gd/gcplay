**Python 3.6 required**
export PYTHONPATH=${PYTHONPATH}:/path/to/project/gcplay/pubsub
Before work with project - generate your own GCC auth key::

    https://cloud.google.com/pubsub/docs/reference/libraries

After git clone if you have such error "ModuleNotFoundError: No module named 'gcplay'"::

    export PYTHONPATH=${PYTHONPATH}:/path/to/project/gcplay/pubsub

where gcplay folder with README.rst file, not python package folder

Set your path to GCC auth key in conf.ini::

    ./config/conf.ini
    "~/" - it's a HOME dir path


Run only publisher (to generates events in Topic) from main project folder with::

    python /path/to/project/gcplay/pubsub/pubsub/publisher.py


Run subscriber and publisher::

    python /path/to/project/gcplay/pubsub/pubsub/subscriber.py

It will send output to console with messages



**SSH Connect for compute engine use this guide:**

https://www.cyberciti.biz/faq/google-cloud-compute-engin-ssh-into-an-instance-from-linux-unix-appleosx/

**How to connect with command**
ssh -o UserKnownHostsFile=/dev/null -o CheckHostIP=no -o StrictHostKeyChecking=no -i $HOME/.ssh/google_compute_engine -A -p 22 $USER@

after adding
ssh xnuinside@35.226.71.118 'cd gcplay && export PYTHONPATH=${PYTHONPATH}:./gcplay && env/bin/python gcplay/gcplay/publisher.py'
