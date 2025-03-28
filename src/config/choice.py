from django.db.models import TextChoices

class RoleUser(TextChoices):
    ADMIN = 'admin'
    MEMBER = 'member'
    
class ThreadResult(TextChoices):
    OK = 'OK'
    ALREADY_RUN = 'ALREADY_RUN'
    ERROR = 'ERROR'
    INFO = 'INFO'


class StatusVessel(TextChoices):
    SCHEDULED = 'Scheduled'
    BERTHING = 'Berthing'
    PUMPING = 'Pumping'
    FINISHED = 'Finished'

class StatusJettyLog(TextChoices):
    OPEN = 'Open'
    CLOSE = 'Close'

class Actifity(TextChoices):
    LOADING = 'Loading'
    DISCHARGING = 'Discharging'