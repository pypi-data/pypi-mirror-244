import logging

from package.IO_module import validate_filename, file_exists
from package.supabase_module import uploadFile, insertJob

# logging.getLogger("httpx").setLevel(logging.CRITICAL)

# Example usage:
filename = validate_filename(input("Enter a filename: "))
print(f"Valid filename: {filename}")

# Insert Job
if file_exists(filename, "tmp/"):
    id = insertJob()
    uploadFile(filename, id, 'Job/')
else:
    print(f"The file 'tmp/" + filename + "' does not exist.")