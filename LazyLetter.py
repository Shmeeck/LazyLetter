from LazyLetter import menu
from LazyLetter import configurator
from LazyLetter.configurator import get_config as config

# attempt to load a previously save config
try:
    configurator.set_config(configurator.Config.load())
except FileNotFoundError:
    print("No config was found, making one...")
    config().save(force=False)
    input(config().continue_msg)

menu.hub()
