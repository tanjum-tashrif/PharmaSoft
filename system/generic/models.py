from django.db import models
from system.middleware.thread_local import _thread_local
from datetime import datetime


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Check if user is available in thread-local storage
        if hasattr(_thread_local, 'user'):
            current_user = _thread_local.user
        else:
            current_user = None
        # print('current user : ', current_user)
        # print('anonymous : ', current_user.is_anonymous)
        # Set 'updated_by' and 'created_by' based on thread-local user
        if self.id:
            if hasattr(self, 'updated_by'):
                if current_user and not current_user.is_anonymous:
                    self.updated_by = current_user.id
                else:
                    self.updated_by = '0'  # Or your default value for unauthenticated users
            if hasattr(self, 'updated_at'):
                self.updated_at = datetime.now()
        else:
            if hasattr(self, 'created_by'):
                if current_user and not current_user.is_anonymous:
                    self.created_by = current_user.id
                else:
                    self.created_by = '0'  # Or your default value for unauthenticated users
            if hasattr(self, 'created_at'):
                self.created_at = datetime.now()
            if hasattr(self, 'updated_by'):
                if current_user and not current_user.is_anonymous:
                    self.updated_by = current_user.id
                else:
                    self.updated_by = '0'
            if hasattr(self, 'updated_at'):
                self.updated_at = datetime.now()

        super(BaseModel, self).save(*args, **kwargs)

