import re
import datetime


def now():
    return datetime.datetime.now().strftime("%H:%M:%S")


def print_info(text):
    if text:
        print(f"{now()} Info: " + text)


def print_error(text):
    if text:
        print(f"{now()} Error: " + text)


def clean_skill(x):
    skill = x[:x.index("(")] if "(" in x else x

    skill = skill.lower()

    temp_d = {"ms ":"microsoft ", "sw ":"software ", "aws ":"amazon web services ", "azure":"microsoft azure"}
    for key, value in temp_d.items():
        if skill.startswith(key):
            skill = skill.replace(key, value)

    skill += " "
    temp_d = {"mgt":" management ", "sw":" software ", "-":" ", "and":" ", "/ iec":" ", "js":" javascript ", "javabeans":" java beans "}
    for key, value in temp_d.items():
        skill = skill.replace(f" {key} ", value)

    return skill.strip()


def transform_label_4(x):
    labels = ["scientist", "analyst", "engineer"]
    lower = x.lower()
    for label in labels:
        if label in lower:
            return label
    return "misc"


def check(x, label, item_list):
    for item in item_list:
        if item in x:
            return label
    return None


def transform_label_2(x):
    lower = x.lower()
    if check(lower, "analyst", ["analytics", "analyst", "analysis"]):
        return "analyst"
    if check(lower, "engineer", ["engineer"]):
        return "engineer"
    return "misc"


def transform_scalar_2(x):
    lower = x.lower()
    if check(lower, "analyst", ["analytics", "analyst", "analysis"]):
        return 0
    if check(lower, "engineer", ["engineer"]):
        return 1
    return 0.5


def transform_label_12(x):
    lower = x.lower()
    lower = re.sub(r"[^a-zA-Z0-9]", " ", lower)
    lower = f" {lower} "
    if check(lower, "ops", ["devops", "operations", "ops"]):
        if "operations research" not in lower:
            return "ops"
    if check(lower, "director", ["director", "manager", "mgr", "mgmt", "management"]):
        return "director"
    if check(lower, "architect", ["architect"]):
        return "architect"
    if check(lower, "security", ["cyber", "security", "cybersecurity"]):
        return "security"
    if check(lower, "cv", ["computer vision"]):
        return "cv"
    if check(lower, "ml", ["machine learning", " ml ", "machine-learning", " m l ", "deep learning"]):
        return "ml"
    if check(lower, "nlp", ["natural language", " nlp "]):
        return "nlp"
    if check(lower, "analyst", ["analytics", "analyst", "analysis", "analytic"]):
        return "analyst"
    if check(lower, "backend", ["back end", "backend"]):
            return "backend"
    if check(lower, "developer", ["developer", "software developer"]):
            return "developer"
    if check(lower, "engineer", ["engineer", "engineering"]):
        return "engineer"
    if check(lower, "scientist", ["science", "scientist"]):
        return "scientist"
    return "misc"


