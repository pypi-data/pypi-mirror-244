import random

first_names_male = (
    "David",
    "Paul",
    "Christopher",
    "Thomas",
    "John",
    "Mark",
    "James",
    "Stephen",
    "Andrew",
    "Jack",
    "Michael",
    "Daniel",
    "Peter",
    "Richard",
    "Matthew",
    "Robert",
    "Ryan",
    "Joshua",
    "Alan",
    "Ian",
    "Simon",
    "Luke",
    "Samuel",
    "Jordan",
    "Anthony",
    "Adam",
    "Lee",
    "Alexander",
    "William",
    "Kevin",
    "Darren",
    "Benjamin",
    "Philip",
    "Gary",
    "Joseph",
    "Brian",
    "Steven",
    "Liam",
    "Keith",
    "Martin",
    "Jason",
    "Jonathan",
    "Jake",
    "Graham",
    "Nicholas",
    "Craig",
    "George",
    "Colin",
    "Neil",
    "Lewis",
    "Nigel",
    "Oliver",
    "Timothy",
    "Stuart",
    "Kenneth",
    "Raymond",
    "Jamie",
    "Nathan",
    "Geoffrey",
    "Connor",
    "Terence",
    "Trevor",
    "Adrian",
    "Harry",
    "Malcolm",
    "Scott",
    "Callum",
    "Wayne",
    "Aaron",
    "Barry",
    "Ashley",
    "Bradley",
    "Patrick",
    "Gareth",
    "Jacob",
    "Sean",
    "Kieran",
    "Derek",
    "Carl",
    "Dean",
    "Charles",
    "Sam",
    "Shaun",
    "Ben",
    "Roger",
    "Mohammed",
    "Leslie",
    "Ronald",
    "Kyle",
    "Clive",
    "Edward",
    "Antony",
    "Jeremy",
    "Justin",
    "Jeffrey",
    "Christian",
    "Roy",
    "Karl",
    "Alex",
    "Gordon",
    "Dominic",
    "Joe",
    "Marc",
    "Reece",
    "Dennis",
    "Russell",
    "Gavin",
    "Rhys",
    "Phillip",
    "Allan",
    "Robin",
    "Charlie",
    "Gerald",
    "Ross",
    "Francis",
    "Eric",
    "Julian",
    "Bernard",
    "Dale",
    "Donald",
    "Damian",
    "Frank",
    "Shane",
    "Cameron",
    "Norman",
    "Duncan",
    "Louis",
    "Frederick",
    "Tony",
    "Howard",
    "Conor",
    "Douglas",
    "Garry",
    "Elliot",
    "Marcus",
    "Arthur",
    "Vincent",
    "Max",
    "Mathew",
    "Abdul",
    "Henry",
    "Martyn",
    "Ricky",
    "Leonard",
    "Lawrence",
    "Glen",
    "Mitchell",
    "Gerard",
    "Gregory",
    "Iain",
    "Billy",
    "Bryan",
    "Joel",
    "Clifford",
    "Josh",
    "Leon",
    "Stewart",
    "Mohammad",
    "Dylan",
    "Graeme",
    "Terry",
    "Guy",
    "Elliott",
    "Stanley",
    "Danny",
    "Brandon",
    "Victor",
    "Toby",
    "Hugh",
    "Mohamed",
    "Brett",
    "Albert",
    "Tom",
    "Declan",
    "Maurice",
    "Glenn",
    "Leigh",
    "Denis",
    "Damien",
    "Bruce",
    "Jay",
    "Owen",
)

first_names_female = (
    "Susan",
    "Sarah",
    "Rebecca",
    "Linda",
    "Julie",
    "Claire",
    "Laura",
    "Lauren",
    "Christine",
    "Karen",
    "Nicola",
    "Gemma",
    "Jessica",
    "Margaret",
    "Jacqueline",
    "Emma",
    "Charlotte",
    "Janet",
    "Deborah",
    "Lisa",
    "Hannah",
    "Patricia",
    "Tracey",
    "Joanne",
    "Sophie",
    "Carol",
    "Jane",
    "Michelle",
    "Victoria",
    "Amy",
    "Elizabeth",
    "Helen",
    "Samantha",
    "Emily",
    "Mary",
    "Diane",
    "Rachel",
    "Anne",
    "Sharon",
    "Ann",
    "Tracy",
    "Amanda",
    "Jennifer",
    "Chloe",
    "Angela",
    "Louise",
    "Katie",
    "Lucy",
    "Barbara",
    "Alison",
    "Sandra",
    "Caroline",
    "Clare",
    "Kelly",
    "Bethany",
    "Gillian",
    "Natalie",
    "Jade",
    "Pauline",
    "Megan",
    "Elaine",
    "Alice",
    "Lesley",
    "Catherine",
    "Hayley",
    "Pamela",
    "Danielle",
    "Holly",
    "Wendy",
    "Abigail",
    "Valerie",
    "Olivia",
    "Jean",
    "Dawn",
    "Donna",
    "Stephanie",
    "Leanne",
    "Kathleen",
    "Natasha",
    "Denise",
    "Sally",
    "Katherine",
    "Georgia",
    "Maureen",
    "Maria",
    "Zoe",
    "Judith",
    "Kerry",
    "Debra",
    "Melanie",
    "Stacey",
    "Eleanor",
    "Paula",
    "Shannon",
    "Sheila",
    "Joanna",
    "Paige",
    "Janice",
    "Lorraine",
    "Georgina",
    "Lynn",
    "Andrea",
    "Suzanne",
    "Nicole",
    "Yvonne",
    "Chelsea",
    "Lynne",
    "Anna",
    "Kirsty",
    "Shirley",
    "Alexandra",
    "Marion",
    "Beverley",
    "Melissa",
    "Rosemary",
    "Kimberley",
    "Carole",
    "Fiona",
    "Kate",
    "Joan",
    "Marie",
    "Jenna",
    "Marilyn",
    "Jodie",
    "June",
    "Grace",
    "Mandy",
    "Rachael",
    "Lynda",
    "Tina",
    "Kathryn",
    "Molly",
    "Jayne",
    "Amber",
    "Marian",
    "Jasmine",
    "Brenda",
    "Sara",
    "Kayleigh",
    "Teresa",
    "Harriet",
    "Julia",
    "Ashleigh",
    "Heather",
    "Kim",
    "Ruth",
    "Jemma",
    "Carly",
    "Leah",
    "Eileen",
    "Francesca",
    "Naomi",
    "Hilary",
    "Abbie",
    "Sylvia",
    "Katy",
    "Irene",
    "Cheryl",
    "Rosie",
    "Dorothy",
    "Aimee",
    "Vanessa",
    "Ellie",
    "Frances",
    "Sian",
    "Josephine",
    "Gail",
    "Jill",
    "Lydia",
    "Joyce",
    "Charlene",
    "Hollie",
    "Hazel",
    "Annette",
    "Bethan",
    "Amelia",
    "Beth",
    "Rita",
    "Geraldine",
    "Diana",
    "Lindsey",
    "Carolyn",
)

# fmt: off
surname = (
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Valentine", "Rich", "Boyd"
    "Sullivan", "Gonzales", "Peters", "Fox", "Ray", "Bradley", "Jensen",
    "Burke", "Black", "Dunn", "Hunter", "Fields", "Owen", "Riley",
    "Goodwin", "Banks", "Gilbert", "Cain", "Nash", "Stevens", "Ford",
    "Cross", "Moss", "Hopkins", "Curry", "McLaughlin", "Harmon",
    "Monroe", "Vincent", "Perry", "Shields", "Kerr", "Townsend",
    "Blake", "Glover", "Pope", "Schwartz", "Lamb", "Manning", "Walter",
    "Leonard", "Dean", "Conway", "Boone", "Church", "Morse", "Dodson",
    "Flynn", "Shea", "Sheppard", "Osborne", "Cochran", "Prince", "Case",
    "Barr", "Rosales", "York", "Winters", "McLean", "Giles", "McKee",
    "Glass", "Dickson", "Hancock", "Gaines", "Fry", "Skinner", "Wiggins",
    "Cameron", "Clements", "Christensen", "Klein", "Pratt", "Briggs",
    "Osborn", "Bond", "Rush", "Churchill", "Corbin", "Leblanc", "Daley",
    "Mullen", "Pham", "Charles", "Graves", "Justice", "Mayer", "Donald",
    "Lyons", "Hines", "Gallagher", "Dorsey", "Shepherd", "Kaiser",
    "Cline", "Joyce", "Hawkins", "Montgomery", "Daugherty", "Hoover",
    "Baird", "Wiley", "Cooke", "Holt", "Duffy", "Buckley", "Haley",
)
# fmt: on

formats = (
    "{first_names_male} {surname}",
    "{first_names_male} {surname}",
    "{first_names_male} {surname}",
    "{first_names_male} {surname}",
    "{first_names_female} {surname}",
    "{first_names_female} {surname}",
    "{first_names_female} {surname}",
    "{first_names_female} {surname}",
    "{first_names_male} {surname}-{second_surname}",
    "{first_names_female} {surname}-{second_surname}",
)


def generate_random_name() -> str:
    """
    Generates a random name based on the given name tuples and formats.

    Returns:
        str: A randomly generated name.
    """
    selected_format = random.choice(formats)
    placeholders = {
        "first_names_male": random.choice(first_names_male)
        if "{first_names_male}" in selected_format
        else "",
        "first_names_female": random.choice(first_names_female)
        if "{first_names_female}" in selected_format
        else "",
        "surname": random.choice(surname) if "{surname}" in selected_format else "",
        "second_surname": random.choice(surname) if "{second_surname}" in selected_format else "",
    }

    return selected_format.format(**placeholders)
