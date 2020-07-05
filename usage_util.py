"""Command line options include many subcommand functions, full usage print out full usage help. function usage
print out specific subcommand usage when it's called.
"""

import sys
import getopt

# highlight color of the output
WARN = '\x1b[1;31m'
CHANGED = '\x1b[1;31;42m'
END = '\x1b[0m'

def full_usage(function_usage, valid_options=[]):
    exec_options = ''
    required_options = '< --sid [arrayname] > < --case case_number >'
    mode_options = '[-f] [-i] [-p]'
    exec_options = ['add', 'delete']
    exec_str = ''

    for exec_opt in valid_options:
           exec_str = exec_str + ' < --' + exec_opt + '=' + exec_opt.upper() + '>'
    cli_usage = (sys.argv[0] + " --" + list(set(exec_options) & set(valid_options))[0] + " "
                    + required_options + exec_str + " " + mode_options)

    Usage="""
    Usage:

        {cmd}

        Help:
            -h, --help                 Display usage

        Required Options:
            --sid <array_name>         Specify the Array name
            --case <case number>       Mandatory entry, case # logged so it can be tracked

        Execute Options:
            --add                      Add host execute
            --delete                   Delete host execute

        Mode Options:
            -f, --force                Force execute
            -i, --noprompt             Proceed with the operation without requiring confirmation
            -p, --preview              Run in Preview Mode
    """.format(cmd=cli_usage)
    print(Usage)
    # subcommand specific usage
    function_usage()

def user_argv_input(argv, function_usage, valid_options):
    """process user input argument based on the subcommand input"""

    ret_dict = dict() # store each argument input

    # default value that should be added here
    try:
        opts, args = getopt.getopt(
                argv, ":fiph",
                [
                    "sid=",
                    "case=",
                    "force",
                    "noprompt",
                    "preview",
                    "help",
                    "add",
                    "delete",
                    "host=",
                    "count=",
                    "size=",
                    "os="
                ]
        )
    except getopt.GetoptError as err:
        print(
            "\n",
            WARN,
            "  getopt error",
            str(err),
            END
            )

        full_usage(function_usage, valid_options)
        sys.exit(1)

    if len(args) > 0:
        print("*** Contains invalid options:", args[0])
        full_usage(function_usage, valid_options)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            full_usage(function_usage, valid_options)
            sys.exit(1)
        elif opt in "--sid":
            ret_dict["array"] = arg
        elif opt in "--case":
            ret_dict["case"] = arg
        elif opt in "--add":
            ret_dict["add"] = 1
        elif opt in "--delete":
            ret_dict["delete"] = 1
        elif opt in ("-f", "--force"):
            ret_dict["force"] = 1
        elif opt in ("-i", "--noprompt"):
            ret_dict["noprompt"] = 1
        elif opt in ("-p", "--preview"):
            ret_dict["preview"] = 1
        elif opt in "--host":
            ret_dict["host"] = arg
        elif opt in "--count":
            ret_dict["count"] = arg
        elif opt in "--size":
            ret_dict["size"] = arg
        elif opt in "--os":
            ret_dict["os"] = arg
        elif opt in "--add":
            ret_dict["add"] = 1
        elif opt in "--add":
            ret_dict["delete"] = 1
        else:
            print("unkown", opt)
            full_usage(usage, valid_options)
            sys.exit(1)

    if "array" and "case" not in ret_dict:
        print(
            "\n",
            WARN,
            "  Missing required option: --sid <array> and --case <case_number>",
            END
            )
        full_usage(function_usage, valid_options)
        sys.exit(1)

    if valid_options is not None:
        # pylint: disable=W0612
        for k, v in ret_dict.items():
            if k not in ('array', 'case', 'force', 'preview', 'noprompt'):
                found = False
                for valid_option in valid_options:
                    if valid_option == k:
                        found = True
                        break
                if not found:
                    print("*** Invalid option given:", k)
                    full_usage(function_usage, valid_options)
                    sys.exit(1)
    if not (set(valid_options).issubset(set(list(ret_dict.keys())))):
        print(
            "\n",
            WARN,
            "  required options: " + str(valid_options),
            END)

        function_usage()
        sys.exit(1)

    return ret_dict


# add funciton
#import usage_util

def add_function_usage():
    Usage="""
    function specific options:

        --add --host <host_name>
              --count <#of Luns>
              --size <45|90|135|250|500|1024|2048|4096|8192>
              --os <solaris|aix|linux|windows|vmware>

    """.format()
    print(Usage)

def main_add(argv):
    valid_options = ["add", "host", "count", "size", "os"]
    #inputs = usage_util.user_argv_input(argv, add_function_usage, valid_options)
    inputs = user_argv_input(argv, add_function_usage, valid_options)

    print(inputs)

# delete function
#import usage_util 

def delete_function_usage():
    Usage="""
    function specific options:

        --delete --host <host_name>

    """.format()
    print(Usage)

def main_delete(argv):
    valid_options = ["delete", "host"]
    #inputs = usage_util.user_argv_input(argv, delete_function_usage, valid_options)
    inputs = user_argv_input(argv, delete_function_usage, valid_options)

    print(inputs)

if __name__ == "__main__":
   main_add(sys.argv[1:])
   #main_delete(sys.argv[1:])
