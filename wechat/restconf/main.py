REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'accounts.api.permissions.custom_exception_handler',

    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'accounts.api.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES' : [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
}