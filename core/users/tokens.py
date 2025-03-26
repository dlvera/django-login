<<<<<<< HEAD
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_verified)
        )

=======
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Combina estos valores para generar un hash único
        return (
            str(user.pk) +          # ID del usuario
            str(timestamp) +        # Marca de tiempo actual
            str(user.is_verified)   # Estado de verificación (tu campo personalizado)
        )

>>>>>>> 77aae958da2440d01975c31eec4871e5f0c8612e
account_activation_token = AccountActivationTokenGenerator()