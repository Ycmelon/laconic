from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.exceptions import PutError


class RecordModel(Model):
    class Meta:
        table_name = "coffee-hummingbird-suitCyclicDB"
        region = "eu-central-1"

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    url = UnicodeAttribute()


RecordModel.create_table(read_capacity_units=1, write_capacity_units=1)


def create_record(alias: str, url: str):
    record = RecordModel(alias, alias, url=url)

    try:
        record.save(RecordModel.pk.does_not_exist())
    except PutError as e:
        if e.cause_response_code == "ConditionalCheckFailedException":
            raise ValueError("Alias already in use")


def get_record(alias: str) -> str:
    try:
        record = RecordModel.get(alias, alias)
    except RecordModel.DoesNotExist:
        raise KeyError

    return record.url


def record_exists(alias: str) -> bool:
    try:
        record = RecordModel.get(alias, alias)
    except RecordModel.DoesNotExist:
        return False
    return True


def delete_record(alias: str):
    try:
        record = RecordModel.get(alias, alias)
    except RecordModel.DoesNotExist:
        raise KeyError

    record.delete()
