from flask import url_for
import pytest

from metabulo.models import CSVFileSchema, db

csv_file_schema = CSVFileSchema()

table_data = """
id,meta,col1,col2
row1,a,0.5,2.0
row2,b,1.5,0
row3,b,4,0.5
"""


@pytest.fixture
def table(client):
    csv_file = csv_file_schema.load({
        'table': table_data,
        'name': 'test_csv_file.csv'
    })
    db.session.add(csv_file)
    db.session.commit()
    yield csv_file


def test_list_columns(client, table):
    resp = client.get(
        url_for('csv.list_columns', csv_id=table.id))
    assert resp.status_code == 200
    assert resp.json == [{
        'column_header': 'id',
        'column_index': 0,
        'column_mask': None,
        'column_type': 'primary-id'
    }, {
        'column_header': 'meta',
        'column_index': 1,
        'column_mask': False,
        'column_type': 'qualitative'
    }, {
        'column_header': 'col1',
        'column_index': 2,
        'column_mask': False,
        'column_type': 'numeric'
    }, {
        'column_header': 'col2',
        'column_index': 3,
        'column_mask': False,
        'column_type': 'numeric'
    }]


def test_list_rows(client, table):
    resp = client.get(
        url_for('csv.list_rows', csv_id=table.id))
    assert resp.status_code == 200
    assert resp.json == [{
        'row_name': '',
        'row_index': 0,
        'row_mask': None,
        'row_type': 'header'
    }, {
        'row_name': 'row1',
        'row_index': 1,
        'row_mask': False,
        'row_type': 'sample'
    }, {
        'row_name': 'row2',
        'row_index': 2,
        'row_mask': False,
        'row_type': 'sample'
    }, {
        'row_name': 'row3',
        'row_index': 3,
        'row_mask': False,
        'row_type': 'sample'
    }]


def test_get_column(client, table):
    resp = client.get(
        url_for('csv.get_column', csv_id=table.id, column_index=1))
    assert resp.status_code == 200
    assert resp.json == {
        'column_header': 'meta',
        'column_index': 1,
        'column_mask': False,
        'column_type': 'qualitative'
    }


def test_get_row(client, table):
    resp = client.get(
        url_for('csv.get_row', csv_id=table.id, row_index=1))
    assert resp.status_code == 200
    assert resp.json == {
        'row_name': 'row1',
        'row_index': 1,
        'row_mask': False,
        'row_type': 'sample'
    }


def test_modify_column(client, table):
    resp = client.put(
        url_for('csv.modify_column', csv_id=table.id, column_index=1),
        json={
            'column_type': 'secondary-id',
            'column_mask': None
        }
    )
    assert resp.status_code == 200
    assert resp.json == {
        'column_header': 'meta',
        'column_index': 1,
        'column_mask': None,
        'column_type': 'secondary-id'
    }


def test_modify_row(client, table):
    resp = client.put(
        url_for('csv.modify_row', csv_id=table.id, row_index=1),
        json={
            'row_mask': True,
            'row_type': 'other'
        }
    )
    assert resp.status_code == 200
    assert resp.json == {
        'row_name': 'row1',
        'row_index': 1,
        'row_mask': True,
        'row_type': 'other'
    }
