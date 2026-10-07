import random
import uuid
from datetime import date, timedelta
import psycopg
from faker import Faker

fake = Faker("fr_FR")

GENDERS = [
    "Male",
    "Female",
    "Other",
]

CITIES = [
    "Paris",
    "Lyon",
    "Marseille",
    "Toulouse",
    "Bordeaux",
    "Nantes",
    "Lille",
    "Nice",
    "Strasbourg",
    "Montpellier",
    "Angouleme"
]

BIOS = [
    "J'aime voyager et découvrir de nouveaux endroits.",
    "Passionné de musique, de cinéma et de photographie.",
    "Toujours partant pour une randonnée ou un bon restaurant.",
    "Je cherche quelqu'un avec qui partager de bons moments.",
    "Amateur de sport, de voyages et de nouvelles expériences.",
    "J'adore cuisiner et découvrir de nouvelles cuisines.",
    "Plutôt calme, curieux et toujours prêt à découvrir quelque chose.",
    "Je fais du très bon café le matin. C'est sans doute la chose la plus importante à savoir sur moi.",
    "Je compte énormément sur le fait que tes critères de sélection sont plus bas que les miens.",
    "Je note les restaurants où je veux emmener des gens que j’aime bien. La liste s’allonge. Je cherche quelqu’un pour y aller.",
    "Bon public, mauvais menteur.",
    "Ici pour de vraies conversations, pas pour scroller.",
    "Mieux en vrai qu’en photo. À vérifier.",
    "Sportif du samedi, cuisinier du dimanche. Ton 3e plat préféré, c’est quoi ?",
    "Je connais trois boulangeries exceptionnelles. Devines où ?",
]

# --------------------------------------------------
#                   BIRTH DATE
# --------------------------------------------------

def random_birth_date():

    today = date.today()

    age = random.randint(18, 60)
    days = age * 365 + random.randint(0, 364)

    return today - timedelta(days=days)

# --------------------------------------------------
#                Generate profile user
# --------------------------------------------------

def generate_profile(user_id):
    gender = random.choice(GENDERS)

    if random.random() < 0.8:
        gender_pref = [random.choice(GENDERS)]
    else:
        gender_pref = ["Male", "Female"]

    tags = random.sample(
        range(1, 71),
        random.randint(0, 5),
    )

    return {
        "user_id": user_id,
        "age": random_birth_date(),
        "gender": gender,
        "gender_pref": gender_pref,
        "bio": random.choice(BIOS),
        "picture_profile_index": random.randint(0, 5),
        "popularity": random.randint(0, 5),
        "localisation": random.choice(CITIES),
        "tags": tags,
    }



def profile(db_conf, user):

    connection = psycopg.connect(**db_conf)

    cursor = connection.cursor()

    for id in user:
        profile = generate_profile(id)

        cursor.execute(
            """
            INSERT INTO userProfile (
                user_id,
                age,
                gender,
                gender_pref,
                bio,
                picture_profile_index,
                popularity,
                localisation,
                tags
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                profile["user_id"],
                profile["age"],
                profile["gender"],
                profile["gender_pref"],
                profile["bio"],
                profile["picture_profile_index"],
                profile["popularity"],
                profile["localisation"],
                profile["tags"],
            ),
        )

    connection.commit()

    cursor.close()
    connection.close()
    print(" profil created!")