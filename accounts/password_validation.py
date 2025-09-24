import re
from django.core.exceptions import (
    ValidationError,
)
from django.utils.translation import gettext as _


class ComplexityValidation:
    """
    Validates that the password contains a mix of uppercase letters, lowercase letters, digits, and special characters
    to ensure adequate complexity.
    """

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least one uppercase letter."))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must contain at least one lowercase letter."))
        if not re.search(r'\d', password):
            raise ValidationError(_("Password must contain at least one digit."))
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_("Password must contain at least one special character."))

    def get_help_text(self):
        return _("Your password contains a mix of uppercase letters, lowercase letters, digits, and special characters.")
