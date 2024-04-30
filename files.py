import os

def extract_filename_from_desktop(query):
    desktop_path = os.path.expanduser("~/Desktop") 
    files_on_desktop = os.listdir(desktop_path)
    query_words = query.split()
    for word in query_words:
        for file_name in files_on_desktop:
            if word.lower() in file_name.lower():
                return os.path.join(desktop_path, file_name)

    return None

# Example usage
query = ("open CN")
filename = extract_filename_from_desktop(query)
if filename:
    print("Found file:", filename)
    os.system(f"open {filename}")
else:
    print("No matching file found on the desktop.")
