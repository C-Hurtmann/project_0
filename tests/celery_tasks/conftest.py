import pytest
from celery.contrib.testing.worker import start_worker


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://',
        'result_backend': 'redis://',
    }

@pytest.fixture(scope='session')
def celery_worker_parameters():
    return {
        'worker_send_task_events': True,
        'task_always_eager': True,
    }

@pytest.fixture(scope='session')
def celery_worker(celery_app, celery_worker_parameters):
    with start_worker(celery_app, **celery_worker_parameters):
        yield