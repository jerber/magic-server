from app.magic.config import settings

email_body = f"""Hello,

We received a request to sign in to {settings.company_name} using this email address. 
If you want to sign in with <EMAIL_ADDRESS>, click this link:

<LINK>.

If you did not request this link, you can safely ignore this email.

Thanks,
The {settings.company_name} Team
"""

subject = f"Sign in to {settings.company_name}"


def make_template_and_subject(email_address: str, magic_link: str):
    new_body = email_body.replace("<LINK>", magic_link).replace(
        "<EMAIL_ADDRESS>", email_address
    )
    return new_body, subject
