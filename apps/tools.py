from uuid import uuid4
import os


def upload_to_and_rename(path, filed_name):
    def wrapper(instance, filename):
        if instance.pk:
            try:
                current = type(instance).objects.filter(pk=instance.pk).first()
                if hasattr(current, filed_name):
                    getattr(current, filed_name).delete()
            except (OSError, FileNotFoundError) as _:
                pass
        ext = filename.split('.')[-1]
        return os.path.join(path, f'{uuid4()}.{ext}')
    return wrapper
