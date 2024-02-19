#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import models
import shlex


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }
    prompt = '(hbnb) '


    def parser(self, parsed):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in parsed:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_all(self, arg):
        """ Shows all objects, or all objects of a class"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in self.classes:
            obj_dict = models.storage.all(self.classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")


    def do_create(self, arg):
        """Creates a new instance of a class"""
        parsed = arg.split()
        if len(parsed) == 0:
            print("** class name missing **")
            return False
        if parsed[0] in self.classes:
            new_dict = self.parser(parsed[1:])
            instance = self.classes[parsed[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()


    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, parsed):
        """ Method to show an individual object """
        new = parsed.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing parsed
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, parsed):
        """ Destroys a specified object """
        new = parsed.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")


        if parsed:
            parsed = parsed.split(' ')[0]  # remove possible trailing parsed
            if parsed not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == parsed:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, parsed):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if parsed == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, parsed):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwparsed = ''

        # isolate cls from id/parsed, ex: (<cls>, delim, <id/parsed>)
        parsed = parsed.partition(" ")
        if parsed[0]:
            c_name = parsed[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from parsed
        parsed = parsed[2].partition(" ")
        if parsed[0]:
            c_id = parsed[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwparsed or parsed
        if '{' in parsed[2] and '}' in parsed[2] and type(eval(parsed[2])) is dict:
            kwparsed = eval(parsed[2])
            parsed = []  # reformat kwparsed into list, ex: [<name>, <value>, ...]
            for k, v in kwparsed.items():
                parsed.append(k)
                parsed.append(v)
        else:  # isolate parsed
            parsed = parsed[2]
            if parsed and parsed[0] == '\"':  # check for quoted arg
                second_quote = parsed.find('\"', 1)
                att_name = parsed[1:second_quote]
                parsed = parsed[second_quote + 1:]

            parsed = parsed.partition(' ')

            # if att_name was not quoted arg
            if not att_name and parsed[0] != ' ':
                att_name = parsed[0]
            # check for quoted val arg
            if parsed[2] and parsed[2][0] == '\"':
                att_val = parsed[2][1:parsed[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and parsed[2]:
                att_val = parsed[2].partition(' ')[0]

            parsed = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(parsed):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = parsed[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
