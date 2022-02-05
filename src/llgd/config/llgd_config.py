import configparser
from os import environ, path, makedirs
from re import T


class LlgdConfig:
    """This class allows the state of the light along with custom profiles
    to be persisted into a user config file
    """

    CURRENT_PROFILE_NAME = "current"
    BRIGHT = "brightness"
    TEMP = "temperature"

    def __init__(self):
        """Constructor initializes the configuration file
        """
        self.config = configparser.ConfigParser()
        self.config_file = None
        xdg_config = environ.get('XDG_CONFIG_HOME')
        if xdg_config != None:
            dir = path.join(xdg_config, "llgd")
            if not path.exists(dir):
                makedirs(dir)
            self.config_file = path.join(dir, "config")
        else:
            self.config_file = path.join(path.expanduser('~'), ".llgd_config")
        self.config.read(self.config_file)

    def delete_profile(self, profile_name):
        """Delete a profile if it exists

        Args:
            profile_name (string): The name of the profile to delete
        """
        if self.config.has_section(profile_name):
            self.config.remove_section(profile_name)
            self.write_config()

    def update_current_state(self, brightness=None, temp=None):
        """Updates the current state of the light

        Args:
            brightness (int, optional): The current brightness level to persist. Defaults to None.
            temp (int, optional): The current temperature level to persist. Defaults to None.
        """
        self.add_or_update_profile(
            self.CURRENT_PROFILE_NAME, brightness=brightness, temp=temp)

    def add_or_update_profile(self, profile_name, brightness=None, temp=None):
        """Adds or updates a profile with the specified parameters

        Args:
            profile_name (string): Name of the profile to add or update.
            brightness (int, optional): Brightness level. Defaults to None.
            temp (int, optional): Temperature level. Defaults to None.
        """
        write_result = False

        if not self.config.has_section(profile_name):
            self.config.add_section(profile_name)
            write_result = True

        if brightness != None:
            self.config.set(profile_name, self.BRIGHT, str(brightness))
            write_result = True

        if temp != None:
            self.config.set(profile_name, self.TEMP, str(temp))
            write_result = True

        if write_result:
            self.write_config()

    def read_profile(self, profile_name):
        """Returns the attributes of the specified profile

        Args:
            profile_name (string): The name of the profile to read

        Returns:
            dictionary: Contains the brightness and temperature values
            indexed by LlgdConfig.BRIGHT and LlgdConfig.TEMP
        """
        brightness = self.config.get(profile_name, self.BRIGHT, fallback=None)
        temperature = self.config.get(profile_name, self.TEMP, fallback=None)

        if brightness != None:
            brightness = int(brightness)
        if temperature != None:
            temperature = int(temperature)

        return {self.BRIGHT: brightness, self.TEMP: temperature}

    def read_current_state(self):
        """Returns the attributes of the current state of the light

        Returns:
            dictionary: Contains the brightness and temperature values
            indexed by LlgdConfig.BRIGHT and LlgdConfig.TEMP
        """
        return self.read_profile(self.CURRENT_PROFILE_NAME)

    def write_config(self):
        """Writes the configuration information to disk
        """
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
