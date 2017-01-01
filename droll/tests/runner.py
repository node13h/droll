from django.test.runner import DiscoverRunner


class DrollDiscoverRunner(DiscoverRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        if not test_labels:
            test_labels = ['droll']

        return super().build_suite(test_labels, *args, **kwargs)
