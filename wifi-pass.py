import subprocess, re

def show_profiles():
    try:
        response = subprocess.run(
            'netsh wlan show profiles',
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='cp850'
        )

        return response.stdout
    
    except subprocess.CalledProcessError:
        print("Execution Error")
        return None

def list_profiles(profiles_output):
    if profiles_output:
        regex_list = [
            r"Perfil de todos los usuarios\s+:\s(.+)",
            r"All User Profile\s+:\s(.+)"
        ]

        for regex in regex_list:
            matches = re.findall(regex, profiles_output)
            if matches:
                return matches
            
    return []

def get_password(profile_name):
    try:
        command = f'netsh wlan show profile name="{profile_name}" key=clear'
        response = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='cp850'
        )

        password_regex_list = [
            r"Contenido de la clave\s+:\s(.+)",
            r"Key Content\s+:\s(.+)"
        ]

        for password_regex in password_regex_list:
            password_match = re.search(password_regex, response.stdout)
            if password_match:
                return password_match.group(1).strip()
            
    except subprocess.CalledProcessError:
        return "Password Obtain Error"
    
    return "Password didn't found"

def list_passwords(all_profiles):
    print("\n[--- Wi-Fi Passwords ---]")
    if not all_profiles:
        print("No wlan profiles available")
        return

    for profile in all_profiles:
        password = get_password(profile)
        print(f"Profile: {profile:<30} Password: {password}")

def main():
    profiles_output = show_profiles()
    profiles_list = list_profiles(profiles_output)
    list_passwords(profiles_list)

if __name__ == '__main__':
    main()