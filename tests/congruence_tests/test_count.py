from qdrant_client.client_base import QdrantBase
from qdrant_client.http import models
from tests.congruence_tests.test_common import (
    COLLECTION_NAME,
    compare_client_results,
    generate_fixtures,
    init_client,
    init_local,
    init_remote,
)
from tests.fixtures.filters import one_random_filter_please


def count_all(client: QdrantBase) -> int:
    return client.count(
        collection_name=COLLECTION_NAME,
        count_filter=None,
    ).count


def filter_count(client: QdrantBase, count_filter: models.Filter) -> int:
    return client.count(
        collection_name=COLLECTION_NAME,
        count_filter=count_filter,
    ).count


def test_simple_search():
    fixture_records = generate_fixtures()

    local_client = init_local()
    init_client(local_client, fixture_records)

    remote_client = init_remote()
    init_client(remote_client, fixture_records)

    compare_client_results(local_client, remote_client, count_all)

    for i in range(100):
        count_filter = one_random_filter_please()
        try:
            compare_client_results(
                local_client, remote_client, filter_count, count_filter=count_filter
            )
        except AssertionError as e:
            print(f"\nFailed with filter {count_filter}")
            raise e
