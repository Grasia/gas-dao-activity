# gas-dao-activity

Compendium of jupyter notebooks to test causality between gas value and DAO activity.

## Download
Enter in your terminal (git must be installed) and write down:

`git clone https://github.com/Grasia/dao-analyzer`

After that, move to repository root directory with:

`cd dao-analyzer`

## Installation
All code has been tested on Linux, but it should work on Windows and macOS, 'cause it just uses the python environment.

So, you must install the following dependencies to run the tool:

* python3 (3.7 or later)
* python3-pip
* virtualenv (not essential)

Now, install the Python dependencies:

`pip3 install -r requirements.txt`

If you don't want to share Python dependencies among other projects, you should use a virtual environment, such as [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).

At first, create a folder where you are going to install all Python dependencies:

`virtualenv -p python3 venv/`

Now, you have to activate it:

`source venv/bin/activate`

Finally, you can install the dependencies:

`pip install -r requirements.txt`

## Running
Run the following command in your terminal.

`jupyter notebook`

Select in your browser the notebook you want to run.