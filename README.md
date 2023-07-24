## Installation
(_On Windows replace forward slashes with back slashes._)

### Install Python with pyenv on UNIX systems

**Create virtual env with python 3.9 (assuming pyenv)**
```bash
$ pyenv install -v 3.9.0
```

**Set python to local or global**
```bash
$ pyenv local 3.9.0
OR
$ pyenv global 3.9.0
```

**Check everything is ok**
```bash
$ pyenv versions

  system
* 3.9.0 (set by /<amazing path>/.pyenv/version)
  3.9.1
```

**Install poetry if not installed**
```bash
$ pip install poetry
```

**Copy the path of your virtual env python**
```bash
$ pyenv which python

/<amazing path>/.pyenv/versions/3.9.0/bin/python
```

**Cd to your project folder and create your virtual env with the python path**
```bash
$ cd /<amazing project path>/
$ poetry config virtualenvs.in-project true
$ poetry env use /<amazing path>/.pyenv/versions/3.9.0/bin/python

Creating virtualenv <amazing project folder> in /<amazing project path>/.venv
Using virtualenv: /<amazing project path>/.venv
```

**You can check that you have a folder .venv in your project and activate you env**
```bash
$ poetry shell

Spawning shell within /<amazing project path>/.venv
. /<amazing project path>/.venv/bin/activate
```

**Success you are in your new env, now you can install all the dependencies**
```bash
$ (<amazing project name>-py3.9) poetry install
```

**Install the git hook scripts**
```bash
$ (<amazing project name>-py3.9) pre-commit install
```

**Install new libraries**

With poetry, we use the notion of groups to separate dev libraries from main
libraries. [link to poetry doc on groups](https://python-poetry.org/docs/master/managing-dependencies/)

***To install on main***
```bash
$ (<amazing project name>-py3.9) poetry add library
```

***To install on dev***
```bash
$ (<amazing project name>-py3.9) poetry add library --group dev
```

***Create requirements files***

Pre-commit is used to automate the freezing of requirements to create
requirements/main.txt, and requirements/dev.txt by freezing only the library
in the dev group.
- requirements/main.txt will be used in the docker image
- requirements/dev.txt will be used in gitlab-ci in the lint stage.

**Run streamlit on docker**

- Env variables
Create a .env file with variables : 
    - ROOT_DIR
    - DOCKER_IMAGE_NAME

- Run
```bash
$ (<amazing project name>-py3.9) docker build -t $DOCKER_IMAGE_NAME .
$ (<amazing project name>-py3.9) docker run -p 8501:8501 $DOCKER_IMAGE_NAME
```
on Mac m1, you must specify the option --platform linux/arm64/v8 with the
docker build if you want to push it to dockerhub.


`

Pour ce qui concerne le chemin abosut
`export PYTHONPATH="${PYTHONPATH}:/chemin/absolu/vers"`
export PYTHONPATH="${PYTHONPATH}:/home/thomas/Documents/LBC/streamlit_app"
streamlit run src/home.py 