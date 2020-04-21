# Django Project Training

SUN* has many technical books that all employees can read. To manage and use them effectively, the management and reviewing system is needed.

## Getting Started

### Prerequisites
- OS: Linux/MacOS
- Database: PostgreSQL, MongoDb
- Github

### Installing

- Installing Python 3.7.x
```sh
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
tar -zxvf Python-3.7.4.tar.xz
cd Python-3.7.4
./configure
make
make test
sudo make install
rm Python-3.7.4.tar.xz && rm -rf Python-3.7.4
```
- Installing python pip

```sh
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
rm get-pip.py
```

- Install virtualenv

```sh
sudo pip install virtualenv
```

### Configuration

Clone code

```sh
https://github.com/minhhh-0927/brs.git
cd brs
```

Create virtual environment

```sh
virtualenv venv -p python3
```

Activate vitual environment and install python dependencies

```sh
source venv/bin/activate
pip install -r requirements.txt
```

Config variable environment

```sh
cp .env.example .env
```

You need create a database. Then, put data infomation into `.env` file

## Running the tests

Migrate database

```sh
python manage.py migrate
```

Run server

```sh
python manage.py runserver
```

### And coding style tests

Updating

## Deployment

Create static folder. Example:

```sh
cd brs
mkdir root_static
```

Put name `root_static` into `.env` file.

Collectstatic

```sh
$ python manage.py collectstatic
1986 static files copied to '/Users/minhhahao/workspace/first-project-training/brs/root_static'.
```

Config project path and log in `uwsgi.ini`

```ini
base=path-to-project
daemonize=path-to-log-file
```

Run code in server

```sh
uwsgi --ini uwsgi.ini
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Pip](https://pypi.org/) - Dependency Management
* [Heroku](https://www.heroku.com/) - Cloud Application Platform
* [PostgreSQL](https://www.postgresql.org/docs/) - The world's most advanced open source database

## Contributing

Updating

## Versioning

Updating

## Authors

* **Ha Hao Minh** - *Initial work* - [PurpleBooth](https://github.com/minhhh-0927)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
