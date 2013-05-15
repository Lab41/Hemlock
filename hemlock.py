#!/usr/bin/python

import sys, time
import texttable as tt

HELP_COUNTER = 0

def user_create(args, var_d):
    # !! TODO need to flesh out the rest of the options
    arg_d = [
        '--name',
        '--email',
    ]
    return check_args(args, arg_d, var_d) 

def user_delete(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def user_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def user_get(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_create(args, var_d):
    # !! TODO need to flesh out the rest of the options
    arg_d = [
        '--name'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_delete(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def tenant_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def tenant_get(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def system_list(args, var_d):
    arg_d = [
    ]
    return check_args(args, arg_d, var_d) 

def system_get(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def register_remote_system(args, var_d):
    # !! TODO add map of operation vocabulary
    arg_d = [
        '--name',
        '--data_type',
        '--description',
        '--tenant',
        '--hostname',
        '--port',
        '--remote_uri',
        '--poc_name',
        '--poc_email'
    ]
    return check_args(args, arg_d, var_d) 

def deregister_remote_system(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def register_local_system(args, var_d):
    arg_d = [
        '--name'
        '--data_type',
        '--description',
        '--tenant',
        '--hostname',
        '--endpoint',
        '--poc_name',
        '--poc_email'
    ]
    return check_args(args, arg_d, var_d) 

def deregister_local_system(args, var_d):
    arg_d = [
        '--uuid'
    ]
    return check_args(args, arg_d, var_d) 

def check_args(args, arg_d, var_d):
    global HELP_COUNTER
    i = 0
    while i < len(args):
        try:
            if args[i] in arg_d:
                var_d[args[i]] = args[i+1]
            arg_d.remove(args[i])
            i += 2
        except:
            HELP_COUNTER += 1
            print_help()
    if arg_d:
        HELP_COUNTER += 1
        print_help()
    return var_d

def print_help():
    global HELP_COUNTER
    if HELP_COUNTER == 1:
        print "--name \tname of system"
        print "--help \thelp\n"
    sys.exit()

def process_args(args):
    global HELP_COUNTER
    var_d = {}

    # !! TODO add load data actions
    arg_actions = {
        'user-create' : user_create,
        'user-delete' : user_delete,
        'user-list' : user_list,
        'user-get' : user_get,
        'tenant-create' : tenant_create,
        'tenant-delete' : tenant_delete,
        'tenant-list' : tenant_list,
        'tenant-get' : tenant_get,
        'system-list' : system_list,
        'system-get' : system_get,
        'register-remote-system' : register_remote_system,
        'deregister-remote-system' : deregister_remote_system,
        'register-local-system' : register_local_system,
        'deregister-local-system' : deregister_local_system
    }

    # get action
    try:
        action = args[0]
        arg_actions[action](args[1:], var_d)
    except:
        HELP_COUNTER += 1
        print_help()

    return var_d, args[0]

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

def process_action(action, var_d):
    print action, var_d
    # !! TODO save stuff to a db
    # !! TODO do calls to and from couch
    # !! TODO tie in with frontend stuff

    # !! TODO testing pretty printing tables
    tab = tt.Texttable()

    x = [[]] # The empty row will have the header

    for key in var_d:
        x.append([key[2:],var_d[key]])

    tab.add_rows(x)
    tab.set_cols_align(['c','c'])
    tab.set_deco(tab.HEADER | tab.VLINES | tab.BORDER)
    tab.set_chars(['-','|','+','-'])
    tab.header(['Property', 'Value'])
    print tab.draw()

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    var_d, action = process_args(args)
    process_action(action, var_d)
    print "Took",time.time() - start_time,"seconds to complete."
