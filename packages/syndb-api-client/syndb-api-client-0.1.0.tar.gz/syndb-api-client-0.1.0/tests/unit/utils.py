from json import dumps


def response_assert_fail_dump(response) -> str:
    return dumps(response.json(), indent=2)
