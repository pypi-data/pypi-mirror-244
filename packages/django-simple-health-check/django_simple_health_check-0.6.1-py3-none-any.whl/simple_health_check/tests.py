from django.test import TestCase, override_settings


class SimpleTest(TestCase):
    def test_liveness(self):
        response = self.client.get('/liveness/')
        self.assertContains(response, b'ok')

    def test_readiness(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(SIMPLE_HEALTH_CHECKS={'simple_health_check.checks.dummy.DummyFalse': None})
    def test_no_readiness(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'down', status_code=503)

    @override_settings(
        SIMPLE_HEALTH_CHECK_ERROR_CODE=500,
        SIMPLE_HEALTH_CHECKS={'simple_health_check.checks.dummy.DummyFalse': None},
    )
    def test_other_error_code(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'down', status_code=500)

    @override_settings(
        CACHES={
            'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
        },
        SIMPLE_HEALTH_CHECKS={'simple_health_check.checks.caches.CacheBackends': None},
    )
    def test_caches(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(
        CACHES={
            'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
            'c2': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
        },
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.caches.CacheBackends': [
                dict(alias='default'),
                dict(alias='c2'),
            ],
        },
    )
    def test_cache_aliases(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(
        CACHES={
            'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
        },
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.caches.CacheBackends': [
                dict(alias='default'),
                dict(alias='c2'),
            ],
        },
    )
    def test_cache_no_rediness(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'down', status_code=503)

    @override_settings(
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.ps.DiskUsage': None,
        },
    )
    def test_ps_disk_usage_no_value(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.ps.DiskUsage': dict(max_usage_percent=99),
        },
    )
    def test_ps_disk_usage(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.ps.DiskUsage': dict(max_usage_percent=0.001),
        },
    )
    def test_ps_disk_usage_no_rediness(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'down', status_code=503)

    @override_settings(
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.ps.MemoryUsage': None,
        },
    )
    def test_ps_memory_usage_no_value(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.ps.MemoryUsage': dict(min_memory_mb=10),
        },
    )
    def test_ps_memory_usage(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'ok')

    @override_settings(
        SIMPLE_HEALTH_CHECKS={
            'simple_health_check.checks.ps.MemoryUsage': dict(min_memory_mb=100_000),
        },
    )
    def test_ps_memory_usage_no_rediness(self):
        response = self.client.get('/readiness/')
        self.assertContains(response, b'down', status_code=503)
