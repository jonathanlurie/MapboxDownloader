'''
Copyright (c) 2015, Jonathan LURIE, All rights reserved.
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library.
'''


'''
SettingFileReader needs tobe used with only two functions: constructor and getter.

Constructor: default is without any argument. In this case the "setting.ini" file
    will be used. You can specify another file using a relative address
    (from the launcher) or absolute.


getSetting : returns the parameter written in "setting.ini" (by default) after casting it
    to float if it's a float, to int if it's an integer or to string in other cases.

    Takes two arguments:
        group : the group of arguments, writen between square brackets
        name : name of the argument


'''



from ConfigParser import *

class SettingFileReader:

    # default file address
    _fileName = 'settings.ini'

    # parser object
    _parser = None


    # constructor
    def __init__(self, fileAdress = None):

        if(fileAdress):
            self._fileName = fileAdress

        self._parser = SafeConfigParser()
        self._parser.read(self._fileName)


    def getSetting(self, group, name):

        try:
            settingValue = self._parser.get(group, name)
        except NoSectionError as e:
            print(e)
            exit()

        # trying to cast to number
        try:
            # cast to float
            settingValue = float(settingValue)

            # if interger, cast to integer
            if(settingValue.is_integer()):
                
                settingValue = int(settingValue)


        except ValueError as e:
            None





        return settingValue
