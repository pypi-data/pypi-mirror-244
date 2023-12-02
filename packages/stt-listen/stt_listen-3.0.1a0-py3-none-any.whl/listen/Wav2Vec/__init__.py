import os

from listen import HOME

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/user/listen.service"):
        print("No listen service present.")
        print("To download it type:")
        print("    wget https://gitlab.com/waser-technologies/technologies/listen/-/raw/main/listen.service.example")
        print("    mv listen.service.example /usr/lib/systemd/user/listen.service")
        sys.exit(1)
    if not os.path.exists(f"{HOME}/.config/systemd/user/default.target.wants/assistant.listen.service"):
        print("Listen STT service is disabled.")
        print("To enable it type:")
        print(f"systemctl --user enable --now listen")
        sys.exit(1)
