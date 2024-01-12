import subprocess
import toml


def get_current_version():
    configuration = toml.load("config.toml")
    return configuration["version"]

def get_current_tag():
    current_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], text=True).strip()
    return current_tag

def create_changelog():
    current_tag = get_current_tag()
    interval = f"{current_tag}..HEAD"
    changelog = subprocess.check_output(["git", "log", interval, "--oneline"], text=True).strip()
    return changelog


next_version = input(f"Current version is {get_current_version()}, please enter the next version: ")

config = toml.load("config.toml")
config["version"] = next_version

with open("config.toml", "w", encoding="utf-8") as f:
    toml.dump(config, f)

print(f"Current version: {get_current_version()}")
print(f"Next version: {next_version}")
print(f"Current tag: {get_current_tag()}")
print(f"Changelog:\n{create_changelog()}")

print("git add .")
print(f"git commit -m 'releasing version v{next_version}'")
print(f"git tag -a v{next_version} -m 'releasing version v{next_version}'")
print("git push origin v{next_version}")
