from CoverLetterExpress import menu
from CoverLetterExpress import utility
from CoverLetterExpress import configurator
from CoverLetterExpress.configurator import get_config as config

continue_msg = False
utility.clear_screen()

print("Initializing setup...")

# attempt to load a previously save config
try:
    configurator.set_config(configurator.Config.load())
except FileNotFoundError:
    print("No config was found, making one...")
    config().save(force=False)
    continue_msg = True

print("\nSetup complete!")

if continue_msg:
    input(config().continue_msg)

menu.hub_navigation()
