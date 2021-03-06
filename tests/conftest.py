from tempfile import TemporaryDirectory

import dotenv
import pytest

from metabulo.app import create_app
from metabulo.models import CSVFileSchema, db

csv_file_schema = CSVFileSchema()


@pytest.fixture(autouse=True)
def mock_load_dotenv(monkeypatch):
    def do_nothing(*args, **kwargs):
        pass

    monkeypatch.setattr(dotenv, 'load_dotenv', do_nothing)


@pytest.fixture
def app():
    with TemporaryDirectory() as upload_folder:
        app = create_app({
            'ENV': 'testing',
            'SQLALCHEMY_DATABASE_URI': f'sqlite://',
            'UPLOAD_FOLDER': upload_folder,
            'OPENCPU_API_ROOT': 'http://localhost:8004/ocpu/library'
        })

        with app.app_context():
            db.create_all()

        yield app


@pytest.fixture
def client(app):
    with app.test_request_context(), app.test_client() as client:
        yield client


@pytest.fixture
def csv_file(client):
    csv_file = csv_file_schema.load({
        'table': 'id,col1,col2\nrow1,0.5,2.0\nrow2,1.5,0\n',
        'name': 'test_csv_file.csv'
    })
    db.session.add(csv_file)
    db.session.commit()
    yield csv_file
