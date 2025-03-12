from submit_job_docs.urls import api_url_path, correct_url_path


def test_api_url_path(settings):
    test_path = 'test'
    test_version = 'test'
    assert api_url_path(test_path, api_version=test_version) == correct_url_path(
        settings.API_URL) + '/v1' + '/' + test_path + '/'

    test_version = '6'
    assert api_url_path(test_path, api_version=test_version) == correct_url_path(
        settings.API_URL) + '/v' + test_version + '/' + test_path + '/'


def test_correct_url_path():
    test_url = 'testUrl'
    urls = correct_url_path(test_url, test_url)
    assert len(urls) == 2 and urls[0] == test_url
