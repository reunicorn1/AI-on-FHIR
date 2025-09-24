"""
### Patients

- **Demographics** (name, birthdate, gender, deceased)
- **Identifiers** (ID, MRN, SSN, etc.)
- **Contact** (phone, email, address parts)
- **Relations** (organization, GP, linked patient)
"""

PATIENT_PATTERNS = []

## Contact patterns

# Phone
phone_patterns = [
        r'\+\d{1,3}[\s-]?\d{3,4}[\s-]?\d{3,4}[\s-]?\d{3,4}',  # International
        r'\d{10,15}',                   # 10+ digits usually phone
        r'\+\d+',                       # Any number starting with +
    ]
for p in phone_patterns:
    PATIENT_PATTERNS.append({"label": "PHONE", "pattern": [{"TEXT": {"REGEX": p}}]})

# Email
PATIENT_PATTERNS.append({
    "label": "EMAIL",
    "pattern": [{"TEXT": {"REGEX": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"}}]
})
# Address is now handled by built-in spacy GPE, LOC, FAC entities

## identifier patterns
identifier_patterns = [
        r'\d{9}',                  # 123456789 (9 consecutive digits)
        r'^[A-Z0-9]{6,10}$'        # General format

    ]
for p in identifier_patterns:
    PATIENT_PATTERNS.append({"label": "IDENTIFIER", "pattern": [{"TEXT": {"REGEX": p}}]})
   
## Demongraphics
 
# Name patterns - handled by built-in spacy PERSON entity but refined here
# First / Given name triggers
given_name_patterns = [
    {"label": "GIVEN_NAME_TRIGGER", "pattern": [{"LOWER": "first"}, {"LOWER": "name"}]},
    {"label": "GIVEN_NAME_TRIGGER", "pattern": [{"LOWER": "given"}, {"LOWER": "name"}]},
    {"label": "GIVEN_NAME_TRIGGER", "pattern": [{"LOWER": "forename"}]},
    {"label": "GIVEN_NAME_TRIGGER", "pattern": [{"LOWER": "personal"}, {"LOWER": "name"}]},
]

# Last / Family name triggers
family_name_patterns = [
    {"label": "FAMILY_NAME_TRIGGER", "pattern": [{"LOWER": "last"}, {"LOWER": "name"}]},
    {"label": "FAMILY_NAME_TRIGGER", "pattern": [{"LOWER": "family"}, {"LOWER": "name"}]},
    {"label": "FAMILY_NAME_TRIGGER", "pattern": [{"LOWER": "surname"}]},
    {"label": "FAMILY_NAME_TRIGGER", "pattern": [{"LOWER": "second"}, {"LOWER": "name"}]},
    {"label": "FAMILY_NAME_TRIGGER", "pattern": [{"LOWER": "clan"}, {"LOWER": "name"}]},
    {"label": "FAMILY_NAME_TRIGGER", "pattern": [{"LOWER": "maiden"}, {"LOWER": "name"}]},
]

# General name references
general_name_patterns = [
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "name"}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "named"}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "called"}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "known"}, {"LOWER": "as"}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "alias"}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "aka"}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "a.k.a."}]},
    {"label": "NAME_GENERAL", "pattern": [{"LOWER": "middle"}, {"LOWER": "name"}]},
]

PATIENT_PATTERNS.extend(given_name_patterns + family_name_patterns + general_name_patterns)

# Date of Birth patterns - handled by built-in spacy DATE but also refined here
PATIENT_PATTERNS.extend([
    # words that identify we're talking about death
    {"label": "DEATH_KEYWORD", "pattern": [{"LOWER": "died"}]},
    {"label": "DEATH_KEYWORD", "pattern": [{"LOWER": "deceased"}]},
    {"label": "DEATH_KEYWORD", "pattern": [{"LOWER": "passed"}, {"LOWER": "away"}]},

    # words that identify we're talking about birth
    {"label": "BIRTH_KEYWORD", "pattern": [{"LOWER": "born"}]},
    {"label": "BIRTH_KEYWORD", "pattern": [{"LOWER": "birth"}]},
    {"label": "BIRTH_KEYWORD", "pattern": [{"LOWER": "dob"}]},

    # Ranges: 1990 to 2000
    {"label": "YEAR_RANGE", "pattern": [{"TEXT": {"REGEX": r"\d{4}"}},
                                         {"LOWER": {"IN": ["to", "and", "-"]}},
                                         {"TEXT": {"REGEX": r"\d{4}"}}]},

    # Keywords: after / before
    {"label": "YEAR_AFTER", "pattern": [{"LOWER": {"IN": ["after", "gt", "greater"]}},
                                         {"TEXT": {"REGEX": r"\d{4}"}}]},

    {"label": "YEAR_BEFORE", "pattern": [{"LOWER": {"IN": ["before", "lt", "less"]}},
                                          {"TEXT": {"REGEX": r"\d{4}"}}]},

    # Exact year
    {"label": "ON_YEAR", "pattern": [{"LOWER": {"IN": ["in", "on"]}},
                                        {"TEXT": {"REGEX": r"\d{4}"}}]}
])

# Age patterns
PATIENT_PATTERNS.extend([
    {"label": "AGE_OVER",
        "pattern": [
            {"LOWER": {"IN": ["over", "older", "above", "greater", "more"]}},
            {"LOWER": "than", "OP": "?"},   # optional "than"
            {"TEXT": {"REGEX": r"\d{1,3}"}}
        ]
    },
    {"label": "AGE_UNDER",
        "pattern": [
            {"LOWER": {"IN": ["under", "younger", "below", "less"]}},
            {"LOWER": "than", "OP": "?"},   # optional "than"
            {"TEXT": {"REGEX": r"\d{1,3}"}}
        ]
    },
    {"label": "AGE_EXACT", "pattern": [
        {"LOWER": {"IN": ["age", "aged", "is", "years", "year"]}},
        {"TEXT": {"REGEX": r"\d{1,3}"}}
    ]},
    # a 45-year-old
    {"label": "AGE",
        "pattern": [
            {"LOWER": "a", "OP": "?"},
            {"IS_DIGIT": True},
            {"TEXT": "-"},
            {"LOWER": {"IN": ["year", "years"]}}
        ]
    },
    # 45 years old
    {"label": "AGE",
        "pattern": [
            {"IS_DIGIT": True},
            {"LOWER": {"IN": ["year", "years"]}},
            {"LOWER": "old", "OP": "?"}
        ]
    },
])

# Gender patterns
PATIENT_PATTERNS.extend([
    # Male
    {"label": "GENDER_MALE", "pattern": [{"LOWER": "male"}]},
    {"label": "GENDER_MALE", "pattern": [{"LOWER": "m"}]},
    {"label": "GENDER_MALE", "pattern": [{"LOWER": "man"}]},
    {"label": "GENDER_MALE", "pattern": [{"LOWER": "boy"}]},
    {"label": "GENDER_MALE", "pattern": [{"LOWER": "boys"}]},

    # Female
    {"label": "GENDER_FEMALE", "pattern": [{"LOWER": "female"}]},
    {"label": "GENDER_FEMALE", "pattern": [{"LOWER": "f"}]},
    {"label": "GENDER_FEMALE", "pattern": [{"LOWER": "woman"}]},
    {"label": "GENDER_FEMALE", "pattern": [{"LOWER": "girl"}]},
    {"label": "GENDER_FEMALE", "pattern": [{"LOWER": "girls"}]},

    # Other / non-binary
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "non-binary"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "nb"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "transgender"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "genderqueer"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "agender"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "other"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "unknown"}]},
    {"label": "GENDER_OTHER", "pattern": [{"LOWER": "lgbtq"}]}
])

## Relations patterns

# GP / Primary Care Physician patterns
PATIENT_PATTERNS.extend([
     # Titles / prefixes
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": {"REGEX": r"dr\.?"}}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "doctor"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "physician"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "gp"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "family"}, {"LOWER": "doctor"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "primary"}, {"LOWER": "care"}, {"LOWER": "provider"}]},

    # Care assignment phrases
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "patients"}, {"LOWER": "of"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "under"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "seeing"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "assigned"}, {"LOWER": "to"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "managed"}, {"LOWER": "by"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "supervised"}, {"LOWER": "by"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "attending"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "covering"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "co-managing"}]},

    # IDs / reference numbers
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "npi"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "dea"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "provider"}, {"LOWER": "code"}]},

     # More references to GPs
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "patients"}, {"LOWER": "of"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "patients"}, {"LOWER": "seeing"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "who"}, {"LOWER": "go"}, {"LOWER": "to"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "primary"}, {"LOWER": "care"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "primary"}, {"LOWER": "medical"}, {"LOWER": "provider"}]},
    {"label": "GP_TRIGGER", "pattern": [{"LOWER": "primary"}, {"LOWER": "healthcare"}, {"LOWER": "provider"}]},
 ])

# Organizations already idenified by built-in spacy ORG entity
# Linked patients are not handled in this version.