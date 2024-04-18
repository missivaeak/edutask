import pytest
import os
import json
from unittest.mock import MagicMock, patch
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture
def dao():
    with patch('src.util.dao.getValidator', autospec=True) as mocked_getValidator:
        mocked_getValidator.return_value = json.loads('{' \
            '"$jsonSchema": {' \
                '"bsonType": "object",' \
                '"required": ["required"],' \
                '"properties": {' \
                    '"string": {' \
                        '"bsonType": "string",' \
                        '"description": "property must be a string"' \
                    '},' \
                    '"boolean": {' \
                        '"bsonType": "bool",' \
                        '"description": "property must be a bool"' \
                    '},' \
                    '"unique": {' \
                        '"bsonType": "string",' \
                        '"description": "property must be unique",' \
                        '"uniqueItems": true' \
                    '},' \
                    '"required": {' \
                        '"bsonType": "string",' \
                        '"description": "property is required"' \
                    '}'
                '}' \
            '}' \
        '}')

        os.environ['MONGO_URL'] = 'mongodb://root:root@localhost:27017/'
        dao = DAO('test')

    existing_data = {
        "required": "this is a string",
        "unique": "email"
    }
    dao.collection.insert_one(existing_data)

    yield dao

    # TODO: kolla om detta är rätt vis att deletea
    dao.collection.database.drop_collection('test')

@pytest.mark.integration
@pytest.mark.parametrize('constraint, data', [
    (
        'required',
        {'required': 'aa'}
    ),
    (
        'unique',
        {'required': 'aa', 'unique': 'second_email'}
    ),
    (
        'string',
        {'required': 'aa', 'string': 'bbbbb'}
    ),
    (
        'boolean',
        {'required': 'aa', 'boolean': False}
    ),
    ])
def test_createReturnDocument(dao: DAO, constraint: str, data: dict):
    result = dao.create(data)
    assert result[constraint] == data[constraint]

@pytest.mark.integration
@pytest.mark.parametrize('data', [
    ( {'notrequired': 'aa'} ),
    ( {'required': 'aa', 'unique': 'email'} ),
    ( {'required': 'aa', 'string': True} ),
    ( {'required': 'aa', 'boolean': 'bbbbbb'} ),
    ])
def test_createRaiseWriteError(dao: DAO, data: dict):
    with pytest.raises(WriteError):
        dao.create(data)


