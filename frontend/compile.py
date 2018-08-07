import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROM_DIR = os.path.join(BASE_DIR, "/templates")
TO_DIR = os.path.join(BASE_DIR,"/html")



all_from_files = [f for f in os.listdir(FROM_DIR) if os.path.isfile(os.path.join(FROM_DIR, f))]
print all_from_files
