
def test_verify_fail(default_art_parser_fixture):
    for file in ['test_bad_atomic.yml']:
        data = default_art_parser_fixture.verify_yaml(f'./data/{file}')
        if data:
            # if data returns true then it means that the test files are looked at as valid which is false
            assert False
