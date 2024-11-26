import json

def load_plan(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_subjects(plan):
    subjects = set()
    for year in plan:
        for cuatrimestre in year["Cuatrimestres"]:
            for materia in cuatrimestre["Materias"]:
                subjects.add(materia)
    return subjects

def compare_plans(plan1, plan2):
    subjects1 = get_all_subjects(plan1)
    subjects2 = get_all_subjects(plan2)
    
    included = subjects1.intersection(subjects2)
    different = subjects1.symmetric_difference(subjects2)
    missing = subjects2 - subjects1
    
    return included, different, missing

# Load the plans
plan1 = load_plan('plan_de_estudios_ingenieria_tecnicatura.json')
plan2 = load_plan('plan_de_estudios_ingenieria_licenciatura.json')

# Compare the plans
included, different, missing = compare_plans(plan1, plan2)

print("Included in both plans:", included, "\nCount:", len(included), "\n")
print("Different between plans:", different, "\nCount:", len(different), "\n")
print("Missing in the first plan:", missing, "\nCount:", len(missing), "\n")