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

account_activation_token = AccountActivationTokenGenerator()