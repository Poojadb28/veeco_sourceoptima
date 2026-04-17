import random

def generate_random_email(template):
    random_number = random.randint(1000, 9999)
    return template.replace("{random}", str(random_number))