import subprocess


def is_firefox_installed_as_snap():
    try:
        result = subprocess.run(
            ["snap", "list", "firefox"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0  # Return code 0 means Firefox is installed as a snap
    except FileNotFoundError:
        return False
