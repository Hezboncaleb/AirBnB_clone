#!/usr/bin/python3

""" Defines the HBnB comand line interpreter """

import cmd
import re
import models
from shlex import split
from models import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [n.strip(",") for n in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [n.strip(",") for n in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [n.strip(",") for n in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """ Defines the command line interpreter """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """ Do nothing upon receiving a command of an empty line """
        pass

    def default(self, arg):
        """ Default behavior """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """ Command to exit the program """
        return True

    def do_EOF(self, arg):
        """ EOF signal to exit the program """
        print("")
        return True

    def do_create(self, arg):
        """ Creates a new class instance and print its id """

        arg_list = parse(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            models.storage.save()

    def do_show(self, arg):
        """ Displays the string representation of a class id """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, arg):
        """ Delete a class of a given id """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            models.storage.save()

    def do_all(self, arg):
        """ Display string representations of all instances """
        arg_list = parse(arg)
        if len(arg_list) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_list) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """ Counts the number of instances of a class """

        arg_list = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """ Update a class instance of a given id """

        arg_list = parse(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) < 2:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) < 3:
            print("** attribute name missing **")
            return False
        if len(arg_list) < 4:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            obj = objdict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = valtype(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for n, v in eval(arg_list[2]).items():
                if (n in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[n]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[n])
                    obj.__dict__[n] = valtype(v)
                else:
                    obj.__dict__[n] = v
        models.storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
