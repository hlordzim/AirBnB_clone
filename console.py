#!/usr/bin/python3
"""HBnB Console - Simple Command Line Interface"""

import cmd
import re
from models.base_model import BaseModel
from models import storage

class HBNBCommand(cmd.Cmd):
    """Contains the functionality for th HBNB console"""

    prompt = "(hbnb) "

    supported_classes = {
        "BaseModel": BaseModel,
    }

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def default(self, line):
        """Handle unknown commands"""
        print("*** Unknown syntax: {}".format(line))

    def do_quit(self, line):
        """Exit the console"""
        return True

    def do_EOF(self, line):
        """Handle EOF"""
        print("")
        return True

    def do_create(self, line):
        """Create a new instance of a class"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.supported_classes:
            print("** class doesn't exist **")
            return
        new_instance = self.supported_classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """Show details of an object"""
        args = line.split()
        if len(args) < 2:
            print("** Usage: show <class> <id>")
            return
        class_name = args[0]
        object_id = args[1]
        key = "{}.{}".format(class_name, object_id)
        obj_dict = storage.all()
        if key in obj_dict:
            print(obj_dict[key])
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """Delete an object"""
        args = line.split()
        if len(args) < 2:
            print("** Usage: destroy <class> <id>")
            return
        class_name = args[0]
        object_id = args[1]
        key = "{}.{}".format(class_name, object_id)
        obj_dict = storage.all()
        if key in obj_dict:
            del obj_dict[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """List all objects or objects of a specific class"""
        args = line.split()
        obj_dict = storage.all()
        if args and args[0] not in self.supported_classes:
            print("** class doesn't exist **")
            return
        print([str(obj) for obj in obj_dict.values()])

    def do_count(self, line):
        """Count instances of a class"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        obj_dict = storage.all()
        count = sum(1 for key in obj_dict if key.startswith(class_name + "."))
        print(count)

    def do_update(self, line):
        """Update an object with new information"""
        args = re.split(r'[()]', line)
        if len(args) < 3:
            print("** Usage: update <class> <id> <attribute_name> <attribute_value>")
            return
        class_name, obj_id = args[0].split()
        obj_id = obj_id.strip()
        attribute_name, attribute_value = args[1].split(',')
        attribute_name = attribute_name.strip()
        attribute_value = attribute_value.strip()
        key = "{}.{}".format(class_name, obj_id)
        obj_dict = storage.all()
        if key not in obj_dict:
            print("** no instance found **")
            return
        obj = obj_dict[key]
        setattr(obj, attribute_name, attribute_value)
        obj.save()

    def do_help(self, line):
        """Show help information"""
        cmd.Cmd.do_help(self, line)

if __name__ == "__main__":
    HBNBCommand().cmdloop()
