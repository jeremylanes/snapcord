from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail, send_mail

from SnapCord.settings import EMAIL_HOST_USER

User = get_user_model()
snapcord_mail_address = EMAIL_HOST_USER


def send_email_customer_order(customer: object, product: object, quantity: int):
    total_price = float(product.price) * int(quantity)
    global snapcord_mail_address

    admin_user = User.objects.filter(is_staff=True)
    admin_emails = [x.email for x in admin_user]

    admin_subject = 'Une nouvelle commande sur bitYangu'

    admin_message = f"""
{customer.username} à commander le produit :{product.name}. ({quantity}) exemplaire
Adresse de livraison: {customer.address.city}
https://bituyangu.com/{product.get_absolute_url()}
"""
    # customer mail
    customer_mail_address = customer.email
    customer_subject = 'Confirmation de commande'
    customer_message = f"""

Cher/Chère {customer.get_short_name()},

Nous vous remercions d'avoir passé commande sur notre boutique en ligne. \
Nous sommes ravis que vous ayez choisi nos produits et nous espérons que \
vous en serez entièrement satisfait(e).

Voici un récapitulatif de votre commande :

- Produit : {product.name}
- Quantité : {quantity}
- Prix unitaire : {product.price}
- Frais de port : -
- Total : {total_price} $

Nous nous assurerons de la livraison dans les prochaines 120h à vôtre adresse : {customer.address} .

Si vous avez des questions ou des préoccupations concernant votre commande, \
n'hésitez pas à nous contacter à l'adresse e-mail {snapcord_mail_address} \
et nous nous ferons un plaisir de vous aider.

Nous vous remercions encore une fois d'avoir choisi notre boutique en ligne \
et nous espérons que vous passerez une excellente expérience d'achat.

Cordialement,

L'équipe bituYangu.
"""

    mail_customer = (customer_subject, customer_message, snapcord_mail_address, [customer_mail_address])
    mail_admin = (admin_subject, admin_message, snapcord_mail_address, admin_emails)
    send_mass_mail(
        datatuple=(mail_admin, mail_customer),
        fail_silently=False
    )


def send_mail_activation_user(user: object, uid: str, token: str):
    global snapcord_mail_address
    user_mail_address = [user.email]
    subject = 'Validation du compte bituYangu'
    message = f"""

Bonjour {user.get_short_name()}! Bienvenue sur la boutique en ligne bituYangu! \
Nous sommes heureux que vous ayez choisi de vous joindre à notre communauté.
Votre compte a été créé et vous pouvez maintenant le configurer et commencer à magasiner. \
Pour confirmer votre compte, veuillez cliquer sur le lien suivant et suivez les instructions: \
http://192.168.214.227:9000/accounts/user-validate/{uid}/{token}/

Cordialement,
L'équipe bituYangu.

"""
    send_mail(
        subject=subject,
        message=message,
        from_email=snapcord_mail_address,
        recipient_list=user_mail_address,
        fail_silently=False
    )
