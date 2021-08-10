# Flask SOS

> Send SOS alerts to your contacts in case of emergency with a signle button click

### Tech Stacks

- Flask
- Flask SQLAlchemy
- Flask Login
- Jinja 2

## Development

### Prerequisites

- Python v3.8
- MySQL or PostgreSQL

### Installation

- Go to a convenient directory/folder and clone the repo

```bash
git clone https://github.com/aseerkt/flask_sos.git
```

- Move into the `flask_sos` directory (`cd flask_sos`)

- Create virtual environment

```bash
python3.8 -m venv venv
```

- Install python modules

```bash
pip install -r requirements.txt
```

- Create `.env` file from `.env.example` (`cp .env.example .env`) and fill in necessary details

```env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=
DATABASE_URL=
BULK_SMS_BASIC_AUTH=

```

- Connect to database and create all model tables

```bash
flask init-db
```

- Run the application

```bash
flask run
```

- Go to url [http://localhost:5000](http://localhost:5000)

### Roadmap

- [x] Regiser User
- [x] Login User
- [x] Edit Message Template
- [x] Add contacts (upto 3)
- [ ] Send alert via bulk messaging API
