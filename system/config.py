class GlobalConfig:
    @staticmethod
    def no_auth_url_list():
        no_auth_url_list = []
        from django.conf import settings
        # from main import settings
        return settings.NO_AUTH
