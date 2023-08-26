from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser

# Create your models here.

USER_ROL = (('A', 'Admin'),('C', 'Colaborador'))

class Universe(models.Model):
    universe = models.CharField(max_length=50, null=False, blank=False, verbose_name='universo', unique=True)

    def __str__(self):
        return str(self.universe)

    class Meta:
        verbose_name = 'Universo'
        verbose_name_plural = 'Universos'

        constraints = [
            models.UniqueConstraint(
                Lower('universe'),
                name='universe_unique',
            ),
        ]


class CustomUser(AbstractUser):

    is_resting = models.BooleanField(default=False, verbose_name='Descanso', help_text='Indica si este usuario está en un descanso temporal.')

    rol = models.CharField(max_length=3, choices=USER_ROL, null=True, blank=True)
    universe = models.ManyToManyField(Universe, blank=True, related_name='user_universe', symmetrical=False)
    notes = models.TextField(null=True, blank=True, verbose_name='Notas')
    timeoff_date = models.DateField(null=True, blank=True, verbose_name='Fecha de descanso')
    out_date = models.DateField(null=True, blank=True, verbose_name='Fecha de salida')

    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse('username', args=[str(self.username)])


