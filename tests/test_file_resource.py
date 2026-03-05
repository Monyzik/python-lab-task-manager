import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.common.exceptions import InvalidJsonFormat
from src.resources.file_resource import FileTaskResource


def test_multi_file_resource(fs: FakeFilesystem):
    fs.create_file("test.json", contents='[{"id": 1, "payload": "Test1"}, {"id": 2, "payload": []}]')
    tasks = list(FileTaskResource("test.json").get_tasks())
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].payload == []


def test_single_file_resource(fs: FakeFilesystem):
    fs.create_file("test.json", contents='{"id": 1, "payload": "Test1"}')
    tasks = list(FileTaskResource("test.json").get_tasks())
    assert len(tasks) == 1
    assert tasks[0].id == 1
    assert tasks[0].payload == "Test1"


def test_invalid_json_format(fs: FakeFilesystem):
    fs.create_file("test1.json", contents='123')
    with pytest.raises(InvalidJsonFormat):
        list(FileTaskResource("test1.json").get_tasks())
    fs.create_file("test2.json", contents='[{"id": 1, "payload": "Test1"}, 123]')
    with pytest.raises(InvalidJsonFormat):
        list(FileTaskResource("test2.json").get_tasks())

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        list(FileTaskResource("non_existent_file.json").get_tasks())