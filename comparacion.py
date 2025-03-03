import json

def load_plan(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_subjects(plan):
    subjects = []
    for year in plan["Años"]:
        for cuatrimestre in year["Cuatrimestres"]:
            for materia in cuatrimestre["Materias"]:
                subjects.append(materia)
    return subjects

def count_optatives(subjects):
    return sum(1 for subject in subjects if "OPTATIVA" in subject)

def compare_plans(plan1, plan2):
    subjects1 = get_all_subjects(plan1)
    subjects2 = get_all_subjects(plan2)

    included = {}
    optative1 = count_optatives(subjects1)
    optative2 = count_optatives(subjects2)
    different = {}
    missing = {}
    missing_from_second = {}
    subjects_left = len(subjects2)-len(subjects1)

    for subject in subjects1:
        if "OPTATIVA" in subject:
            continue
        if subject in subjects2:
            included[subject] = 1
        else:
            missing[subject] = 1

    for subject in subjects2:
        if "OPTATIVA" in subject:
            continue
        if subject not in subjects1:
            different[subject] = 1
            missing_from_second[subject] = 1


    return included, different, missing, optative1, optative2, missing_from_second, subjects_left

# Load the plans
plan1 = load_plan('./planes/LICENCIATURA_EN_GESTIÓN_DE_TECNOLOGÍA_DE_LA_INFORMACIÓN.json')
plan2 = load_plan('./planes/TECNICATURA_UNIVERSITARIA_EN_DESARROLLO_DE_SOFTWARE.json')
# plan2 = load_plan('./planes/INGENIERÍA_EN_INFORMÁTICA.json')

# Compare the plans
included, different, missing, optative1, optative2, missing_from_second, subjects_left = compare_plans(plan1, plan2)

# Print the results
print("Subjects approved in the previous plan (excluding optatives):", included)
print("Subjects different in the second plan (missing from the first plan):",different)
print("Total optative subjects in both plans:", optative1 + optative2)
print("Subjects approved in the previous plan:", len(included) + optative1)
print("Subjects missing from the second plan to complete it:",missing_from_second)
print("Subjects left in the second plan:", subjects_left)