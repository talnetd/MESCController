import os

from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
    AUTH_OID,
    AUTH_REMOTE_USER,
)
from flask_babel import lazy_gettext as _

basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"

# The SQLAlchemy connection string.
# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

# NOTE:
# CREATE DATABASE mesc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SQLALCHEMY_DATABASE_URI = (
    "mysql://dbuser:dbuser@192.168.64.7/mesc?charset=utf8")

# SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
# SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

# ------------------------------
# GLOBALS FOR APP Builder
# ------------------------------
# Uncomment to setup Your App name
APP_NAME = "MESC Controller"

# Uncomment to setup Setup an App icon
APP_ICON = "/static/images/mesc.png"
# APP_ICON = "https://lh3.googleusercontent.com/JJ1Co79xMZ2EOO98aX7tiJS3CjGDW4MeqjwZb0LayioFKJQUiTBF80nQasRP3aHEzwet"
# APP_ICON = "https://www.royalbellsmm.com/upload/customers_logo/mesc.png"

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
AUTH_TYPE = AUTH_DB
MYSQL_DATABASE_CHARSET = "utf8mb4"
# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = "Admin"

# Uncomment to setup Public role name, no authentication needed
AUTH_ROLE_PUBLIC = "Public"

# Will allow user self registration
# AUTH_USER_REGISTRATION = True

# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "Public"

# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "en"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "translations"
# The allowed translation for you app
LANGUAGES = {
    "en": {
        "flag": "gb",
        "name": "English"
    },
    # "pt": {"flag": "pt", "name": "Portuguese"},
    # "pt_BR": {"flag": "br", "name": "Pt Brazil"},
    # "es": {"flag": "es", "name": "Spanish"},
    # "de": {"flag": "de", "name": "German"},
    # "zh": {"flag": "cn", "name": "Chinese"},
    # "ru": {"flag": "ru", "name": "Russian"},
    # "pl": {"flag": "pl", "name": "Polish"},
    "my": {
        "flag": "mm",
        "name": "မြန်မာ"
    },
}
# ---------------------------------------------------
# Image and file configuration
# ---------------------------------------------------
# The file upload folder, when using models with files
UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload url, when using models with images
IMG_UPLOAD_URL = "/static/uploads/"
# Setup image size default is (300, 200, True)
# IMG_SIZE = (300, 200, True)

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "cerulean.css"
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
APP_THEME = "spacelab.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"

FAB_API_SWAGGER_UI = True

FAB_ROLES = {
    "Provider": [
        ["public_menu_check", "menu_access"],
        ["public_submenu_check_bill_status", "menu_access"],
        ["UserDBModelView", "resetmypassword"],
        ["UserDBModelView", "can_userinfo"],
        ["UserDBModelView", "userinfoedit"],
        ["UserInfoEditView", "can_this_form_get"],
        ["UserInfoEditView", "can_this_form_post"],
        ["ResetMyPasswordView", "can_this_form_get"],
        ["ResetMyPasswordView", "can_this_form_post"],
        ["Bill", "menu_access"],
        ["Manage", "menu_access"],
        ["Meterboxes", "menu_access"],
        ["submenu_bills", "menu_access"],
        # ["submenu_bill_details", "menu_access"],
        ["Payment", "menu_access"],
        # ["Providers", "menu_access"],
        # ["Retailers", "menu_access"],
        ["submenu_payment_settings", "menu_access"],
        ["submenu_transactions", "menu_access"],
        ["submenu_payment_methods", "menu_access"],
        ["submenu_payment_info_generic", "menu_access"],
        ["submenu_payment_info_card", "menu_access"],
        # ["MeterboxView", "can_delete"],
        ["MeterboxView", "can_show"],
        ["MeterboxView", "can_edit"],
        ["MeterboxView", "can_add"],
        ["MeterboxView", "can_list"],
        ["MeterboxView", "can_download"],
        ["BillView", "can_download"],
        ["BillView", "can_edit"],
        # ["BillView", "can_delete"],
        ["BillView", "can_show"],
        ["BillView", "can_add"],
        ["BillView", "can_list"],
        # ["BillDetailView", "can_download"],
        # ["BillDetailView", "can_edit"],
        # ["BillDetailView", "can_delete"],
        # ["BillDetailView", "can_show"],
        # ["BillDetailView", "can_add"],
        # ["BillDetailView", "can_list"],
        # ["PaymentInfoCardView", "can_download"],
        # ["PaymentInfoCardView", "can_edit"],
        # ["PaymentInfoCardView", "can_delete"],
        # ["PaymentInfoCardView", "can_show"],
        # ["PaymentInfoCardView", "can_add"],
        # ["PaymentInfoCardView", "can_list"],
        # ["PaymentInfoGenericView", "can_download"],
        # ["PaymentInfoGenericView", "can_edit"],
        # ["PaymentInfoGenericView", "can_delete"],
        # ["PaymentInfoGenericView", "can_show"],
        # ["PaymentInfoGenericView", "can_add"],
        # ["PaymentInfoGenericView", "can_list"],
        # ["PaymentMethodsView", "can_download"],
        # ["PaymentMethodsView", "can_edit"],
        # ["PaymentMethodsView", "can_delete"],
        # ["PaymentMethodsView", "can_show"],
        # ["PaymentMethodsView", "can_add"],
        # ["PaymentMethodsView", "can_list"],
        # ["ProvidersView", "can_download"],
        # ["ProvidersView", "can_edit"],
        # ["ProvidersView", "can_delete"],
        # ["ProvidersView", "can_show"],
        # ["ProvidersView", "can_add"],
        # ["ProvidersView", "can_list"],
        # ["RetailersView", "can_download"],
        # ["RetailersView", "can_edit"],
        # ["RetailersView", "can_delete"],
        # ["RetailersView", "can_show"],
        # ["RetailersView", "can_add"],
        # ["RetailersView", "can_list"],
        # ["UserPaymentSettingsView", "can_download"],
        # ["UserPaymentSettingsView", "can_edit"],
        # ["UserPaymentSettingsView", "can_delete"],
        # ["UserPaymentSettingsView", "can_show"],
        # ["UserPaymentSettingsView", "can_add"],
        # ["UserPaymentSettingsView", "can_list"],
        ["Transactions", "can_download"],
        ["Transactions", "can_edit"],
        # ["Transactions", "can_delete"],
        ["Transactions", "can_show"],
        ["Transactions", "can_add"],
        ["Transactions", "can_list"],
        ["BillsAPI", "can_get"],
        ["BillsAPI", "can_put"],
        ["BillsAPI", "can_post"],
        # ["BillsAPI", "can_delete"],
        ["BillsAPI", "can_info"],
        ["BillModelApi", "can_get"],
        ["BillModelApi", "can_put"],
        ["BillModelApi", "can_post"],
        # ["BillModelApi", "can_delete"],
        ["BillModelApi", "can_info"],
    ],
    "Retailer": [
        ["UserDBModelView", "resetmypassword"],
        ["UserDBModelView", "can_userinfo"],
        ["UserDBModelView", "userinfoedit"],
        ["UserInfoEditView", "can_this_form_get"],
        ["UserInfoEditView", "can_this_form_post"],
        ["ResetMyPasswordView", "can_this_form_get"],
        ["ResetMyPasswordView", "can_this_form_post"],
        ["Bill", "menu_access"],
        ["Manage", "menu_access"],
        ["Meterboxes", "menu_access"],
        ["submenu_bills", "menu_access"],
        # ["submenu_bill_details", "menu_access"],
        ["Payment", "menu_access"],
        # ["Providers", "menu_access"],
        # ["Retailers", "menu_access"],
        ["submenu_payment_settings", "menu_access"],
        ["submenu_transactions", "menu_access"],
        ["submenu_payment_methods", "menu_access"],
        ["submenu_payment_info_generic", "menu_access"],
        ["submenu_payment_info_card", "menu_access"],
        # ["MeterboxView", "can_delete"],
        ["MeterboxView", "can_show"],
        ["MeterboxView", "can_edit"],
        ["MeterboxView", "can_add"],
        ["MeterboxView", "can_list"],
        ["MeterboxView", "can_download"],
        ["BillView", "can_download"],
        ["BillView", "can_edit"],
        # ["BillView", "can_delete"],
        ["BillView", "can_show"],
        ["BillView", "can_add"],
        ["BillView", "can_list"],
        # ["BillDetailView", "can_download"],
        # ["BillDetailView", "can_edit"],
        # ["BillDetailView", "can_delete"],
        # ["BillDetailView", "can_show"],
        # ["BillDetailView", "can_add"],
        # ["BillDetailView", "can_list"],
        # ["PaymentInfoCardView", "can_download"],
        # ["PaymentInfoCardView", "can_edit"],
        # ["PaymentInfoCardView", "can_delete"],
        # ["PaymentInfoCardView", "can_show"],
        # ["PaymentInfoCardView", "can_add"],
        # ["PaymentInfoCardView", "can_list"],
        # ["PaymentInfoGenericView", "can_download"],
        # ["PaymentInfoGenericView", "can_edit"],
        # ["PaymentInfoGenericView", "can_delete"],
        # ["PaymentInfoGenericView", "can_show"],
        # ["PaymentInfoGenericView", "can_add"],
        # ["PaymentInfoGenericView", "can_list"],
        # ["PaymentMethodsView", "can_download"],
        # ["PaymentMethodsView", "can_edit"],
        # ["PaymentMethodsView", "can_delete"],
        # ["PaymentMethodsView", "can_show"],
        # ["PaymentMethodsView", "can_add"],
        # ["PaymentMethodsView", "can_list"],
        # ["ProvidersView", "can_download"],
        # ["ProvidersView", "can_edit"],
        # ["ProvidersView", "can_delete"],
        # ["ProvidersView", "can_show"],
        # ["ProvidersView", "can_add"],
        # ["ProvidersView", "can_list"],
        # ["RetailersView", "can_download"],
        # ["RetailersView", "can_edit"],
        # ["RetailersView", "can_delete"],
        # ["RetailersView", "can_show"],
        # ["RetailersView", "can_add"],
        # ["RetailersView", "can_list"],
        # ["UserPaymentSettingsView", "can_download"],
        # ["UserPaymentSettingsView", "can_edit"],
        # ["UserPaymentSettingsView", "can_delete"],
        # ["UserPaymentSettingsView", "can_show"],
        # ["UserPaymentSettingsView", "can_add"],
        # ["UserPaymentSettingsView", "can_list"],
        ["Transactions", "can_download"],
        ["Transactions", "can_edit"],
        # ["Transactions", "can_delete"],
        ["Transactions", "can_show"],
        ["Transactions", "can_add"],
        ["Transactions", "can_list"],
        ["BillsAPI", "can_get"],
        ["BillsAPI", "can_put"],
        ["BillsAPI", "can_post"],
        # ["BillsAPI", "can_delete"],
        ["BillsAPI", "can_info"],
        ["BillModelApi", "can_get"],
        ["BillModelApi", "can_put"],
        ["BillModelApi", "can_post"],
        # ["BillModelApi", "can_delete"],
        ["BillModelApi", "can_info"],
    ],
    "User": [
        ["public_menu_check", "menu_access"],
        ["public_submenu_check_bill_status", "menu_access"],
        # profile setting
        ["UserDBModelView", "resetmypassword"],
        ["UserDBModelView", "can_userinfo"],
        ["UserDBModelView", "userinfoedit"],
        ["UserInfoEditView", "can_this_form_get"],
        ["UserInfoEditView", "can_this_form_post"],
        ["ResetMyPasswordView", "can_this_form_get"],
        ["ResetMyPasswordView", "can_this_form_post"],
        # menu access
        ["Bill", "menu_access"],
        ["Manage", "menu_access"],
        ["Meterboxes", "menu_access"],
        ["submenu_bills", "menu_access"],
        # ["submenu_bill_details", "menu_access"],
        # ["Payment", "menu_access"],
        # ["Providers", "menu_access"],
        # ["Retailers", "menu_access"],
        # ["submenu_transactions", "menu_access"],
        # ["submenu_payment_info_generic", "menu_access"],
        # ["submenu_payment_info_card", "menu_access"],
        # ["submenu_payment_methods", "menu_access"],
        # ["submenu_payment_settings", "menu_access"],
        # app menus
        # ["MeterboxView", "can_delete"],
        ["MeterboxView", "can_show"],
        # ["MeterboxView", "can_edit"],
        # ["MeterboxView", "can_add"],
        ["MeterboxView", "can_list"],
        # ["MeterboxView", "can_download"],
        # ["BillView", "can_download"],
        # ["BillView", "can_edit"],
        # ["BillView", "can_delete"],
        ["BillView", "can_show"],
        # ["BillView", "can_add"],
        ["BillView", "can_list"],
        # ["BillDetailView", "can_download"],
        # ["BillDetailView", "can_edit"],
        # ["BillDetailView", "can_delete"],
        # ["BillDetailView", "can_show"],
        # ["BillDetailView", "can_add"],
        # ["BillDetailView", "can_list"],
        # ["PaymentInfoCardView", "can_download"],
        # ["PaymentInfoCardView", "can_edit"],
        # ["PaymentInfoCardView", "can_delete"],
        # ["PaymentInfoCardView", "can_show"],
        # ["PaymentInfoCardView", "can_add"],
        # ["PaymentInfoCardView", "can_list"],
        # ["PaymentInfoGenericView", "can_download"],
        # ["PaymentInfoGenericView", "can_edit"],
        # ["PaymentInfoGenericView", "can_delete"],
        # ["PaymentInfoGenericView", "can_show"],
        # ["PaymentInfoGenericView", "can_add"],
        # ["PaymentInfoGenericView", "can_list"],
        # ["PaymentMethodsView", "can_download"],
        # ["PaymentMethodsView", "can_edit"],
        # ["PaymentMethodsView", "can_delete"],
        # ["PaymentMethodsView", "can_show"],
        # ["PaymentMethodsView", "can_add"],
        # ["PaymentMethodsView", "can_list"],
        # ["ProvidersView", "can_download"],
        # ["ProvidersView", "can_edit"],
        # ["ProvidersView", "can_delete"],
        # ["ProvidersView", "can_show"],
        # ["ProvidersView", "can_add"],
        # ["ProvidersView", "can_list"],
        # ["RetailersView", "can_download"],
        # ["RetailersView", "can_edit"],
        # ["RetailersView", "can_delete"],
        # ["RetailersView", "can_show"],
        # ["RetailersView", "can_add"],
        # ["RetailersView", "can_list"],
        # ["UserPaymentSettingsView", "can_download"],
        # ["UserPaymentSettingsView", "can_edit"],
        # ["UserPaymentSettingsView", "can_delete"],
        # ["UserPaymentSettingsView", "can_show"],
        # ["UserPaymentSettingsView", "can_add"],
        # ["UserPaymentSettingsView", "can_list"],
        # ["Transactions", "can_download"],
        # ["Transactions", "can_edit"],
        # ["Transactions", "can_delete"],
        # ["Transactions", "can_show"],
        # ["Transactions", "can_add"],
        # ["Transactions", "can_list"],
    ],
}
