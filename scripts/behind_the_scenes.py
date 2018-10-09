#!/usr/bin/env python
import rospy
import rosnode
import subprocess, shlex
from colorama import Fore, Style

###### WARNING ######
# You need to comment out the code below the:
# "If not running interactively, don't do anything"
# line in the remote computers' ~/.bashrc in order to run ROS commands

valid_mm_input = ["0", "1", "2", "3", "4", "5", "6", "q"]

def main():
    rospy.init_node("behind_the_scenes")

    rosnodes_to_kill = rospy.get_param("behind_the_scenes/rosnodes_to_kill", [])
    launch_packages = rospy.get_param("behind_the_scenes/launch_packages", [])
    custom_commands = rospy.get_param("behind_the_scenes/custom_commands", [])
    ip_addresses = rospy.get_param("behind_the_scenes/ip_addresses", [])
    launch_files = rospy.get_param("behind_the_scenes/launch_files", [])
    run_packages = rospy.get_param("behind_the_scenes/run_packages", [])
    executables = rospy.get_param("behind_the_scenes/executables", [])
    usernames = rospy.get_param("behind_the_scenes/usernames", [])

    while(not rospy.is_shutdown()):
        print Fore.YELLOW + Style.BRIGHT + " BEHIND THE SCENES " + Style.RESET_ALL
        if len(ip_addresses) > 0:
            if len(ip_addresses) == len(usernames):
                print "-------------------------------"
                print "------AVAILABLE COMPUTERS------"
                print "-------------------------------"
                i = 0
                for i in xrange(len(ip_addresses)):
                    if i % 2 == 0:
                        print Fore.YELLOW
                    else:
                        print Fore.GREEN
                    print str(i+1) + ": [" + ip_addresses[i] + "], username: " + usernames[i]
                    print Style.RESET_ALL
            else:
                print Fore.RED + "Invalid input. ip_addresses and usernames do not have the same size!" + Style.RESET_ALL
                exit()
        print "-------------------"
        print "------M E N U------"
        print "-------------------"
        print Fore.BLUE + Style.BRIGHT + "1: " + Style.RESET_ALL + "Kill a node selected on runtime."
        print Fore.BLUE + Style.BRIGHT + "2: " + Style.RESET_ALL + "Kill a node from a predefined collection."
        print Fore.BLUE + Style.BRIGHT + "3: " + Style.RESET_ALL + "Kill all predefined nodes."
        print Fore.BLUE + Style.BRIGHT + "4: " + Style.RESET_ALL + "Launch one of the launch files."
        print Fore.BLUE + Style.BRIGHT + "5: " + Style.RESET_ALL + "Run one of the executables."
        print Fore.BLUE + Style.BRIGHT + "6: " + Style.RESET_ALL + "Run one of the predefined custom commands."
        print Fore.BLUE + Style.BRIGHT + "0: " + Style.RESET_ALL + "Clear move_base costmaps."
        print Fore.BLUE + Style.BRIGHT + "q: " + Style.RESET_ALL + "Quit the application."
        print Fore.GREEN + Style.DIM + "INFO: Append a selection with \",\" and a number to run the command on one of the available computers" + Style.RESET_ALL
        ans = raw_input().lower().strip()
        remote_ans = ans.split(",")
        remote_command = ""
        if len(remote_ans) > 1:
            if remote_ans[1].isdigit() and int(remote_ans[1]) > 0 and int(remote_ans[1])-1 < len(ip_addresses):
                remote_command = "ssh " + usernames[int(remote_ans[1])-1] + "@" + ip_addresses[int(remote_ans[1])-1] + " '"
            else:
                print Fore.RED + "Remote computer index not found!" + Style.RESET_ALL
                continue
        if remote_ans[0] not in valid_mm_input:
            print Fore.RED + "Wrong input!" + Style.RESET_ALL
        else:
            if ans == "q":
                print Fore.YELLOW + "bb" + Style.RESET_ALL
                exit()
            elif remote_ans[0] == "0":
                x(remote_command, "rosservice call /move_base/clear_costmaps \"{}\"")
            elif remote_ans[0] == "1":
                i = 0
                selected = False
                while(not selected):
                    running_nodes = rosnode.get_node_names()
                    for i in xrange(len(running_nodes)):
                        if i % 2 == 0:
                            print Fore.YELLOW
                        else:
                            print Fore.GREEN
                        print str(i+1) + ": " + running_nodes[i]
                        print Style.RESET_ALL
                    print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                    ans = raw_input().strip()
                    if ans == "0":
                        break
                    else:
                        if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(running_nodes):
                            selected = True
                            x(remote_command, "rosnode kill " + running_nodes[int(ans)-1])
                        else:
                            print Fore.RED + "Wrong input!" + Style.RESET_ALL
            elif remote_ans[0] == "2":
                if len(rosnodes_to_kill) == 0:
                    print Fore.RED + "The list of predefined nodes is empty! Check the rosnodes_to_kill parameter." + Style.RESET_ALL 
                else:
                    i = 0
                    selected = False
                    while(not selected):
                        for i in xrange(len(rosnodes_to_kill)):
                            if i % 2 == 0:
                                print Fore.YELLOW
                            else:
                                print Fore.GREEN
                            print str(i+1) + ": " + rosnodes_to_kill[i]
                            print Style.RESET_ALL
                        print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                        ans = raw_input().strip()
                        if ans == "0":
                            break
                        else:
                            if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(rosnodes_to_kill):
                                selected = True
                                x(remote_command, "rosnode kill " + rosnodes_to_kill[int(ans)-1])
                            else:
                                print Fore.RED + "Wrong input!" + Style.RESET_ALL
            elif remote_ans[0] == "3":
                if len(rosnodes_to_kill) == 0:
                    print Fore.RED + "The list of predefined nodes is empty! Check the rosnodes_to_kill parameter." + Style.RESET_ALL 
                else:
                    c = "rosnode kill "
                    for i in rosnodes_to_kill:
                        c += i + " "
                    x(remote_command, c)
            elif remote_ans[0] == "4":
                if len(launch_packages) == 0:
                    print Fore.RED + "The list of predefined packages is empty! Check the launch_packages parameter." + Style.RESET_ALL 
                else:
                    i = 0
                    selected = False
                    while(not selected):
                        for i in xrange(len(launch_packages)):
                            if i % 2 == 0:
                                print Fore.YELLOW
                            else:
                                print Fore.GREEN
                            print str(i+1) + ": " + launch_packages[i]
                            print Style.RESET_ALL
                        print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                        ans = raw_input().strip()
                        if ans == "0":
                            break
                        else:
                            if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(launch_packages):
                                package = launch_packages[int(ans)-1]
                                if len(launch_files) == 0:
                                    print Fore.RED + "The list of predefined launch files is empty! Check the launch_files parameter." + Style.RESET_ALL 
                                    break
                                else:
                                    i = 0
                                    selected2 = False
                                    while(not selected2):
                                        for i in xrange(len(launch_files)):
                                            if i % 2 == 0:
                                                print Fore.YELLOW
                                            else:
                                                print Fore.GREEN
                                            print str(i+1) + ": " + launch_files[i]
                                            print Style.RESET_ALL
                                        print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                                        ans = raw_input().strip()
                                        if ans == "0":
                                            break
                                        else:
                                            if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(launch_files):
                                                selected = True
                                                selected2 = True
                                                x(remote_command, "roslaunch " + package + " " + launch_files[int(ans)-1])
                                            else:
                                                print Fore.RED + "Wrong input!" + Style.RESET_ALL
                            else:
                                print Fore.RED + "Wrong input!" + Style.RESET_ALL
            elif remote_ans[0] == "5":
                if len(run_packages) == 0:
                    print Fore.RED + "The list of predefined packages is empty! Check the run_packages parameter." + Style.RESET_ALL 
                else:
                    i = 0
                    selected = False
                    while(not selected):
                        for i in xrange(len(run_packages)):
                            if i % 2 == 0:
                                print Fore.YELLOW
                            else:
                                print Fore.GREEN
                            print str(i+1) + ": " + run_packages[i]
                            print Style.RESET_ALL
                        print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                        ans = raw_input().strip()
                        if ans == "0":
                            break
                        else:
                            if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(run_packages):
                                package = run_packages[int(ans)-1]
                                if len(executables) == 0:
                                    print Fore.RED + "The list of predefined executables is empty! Check the executables parameter." + Style.RESET_ALL 
                                    break
                                else:
                                    i = 0
                                    selected2 = False
                                    while(not selected2):
                                        for i in xrange(len(executables)):
                                            if i % 2 == 0:
                                                print Fore.YELLOW
                                            else:
                                                print Fore.GREEN
                                            print str(i+1) + ": " + executables[i]
                                            print Style.RESET_ALL
                                        print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                                        ans = raw_input().strip()
                                        if ans == "0":
                                            break
                                        else:
                                            if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(executables):
                                                selected = True
                                                selected2 = True
                                                x(remote_command, "rosrun " + package + " " + executables[int(ans)-1])
                                            else:
                                                print Fore.RED + "Wrong input!" + Style.RESET_ALL
                            else:
                                print Fore.RED + "Wrong input!" + Style.RESET_ALL
            elif remote_ans[0] == "6":
                if len(custom_commands) == 0:
                    print Fore.RED + "The list of predefined custom commands is empty! Check the custom_commands parameter." + Style.RESET_ALL 
                else:
                    i = 0
                    selected = False
                    while(not selected):
                        for i in xrange(len(custom_commands)):
                            if i % 2 == 0:
                                print Fore.YELLOW
                            else:
                                print Fore.GREEN
                            print str(i+1) + ": " + custom_commands[i]
                            print Style.RESET_ALL
                        print Fore.BLUE + "0: " + Style.RESET_ALL + "Cancel."
                        ans = raw_input().strip()
                        if ans == "0":
                            break
                        else:
                            if ans.isdigit() and int(ans)-1 >= 0 and int(ans)-1 < len(custom_commands):
                                selected = True
                                x(remote_command, rosnodes_to_kill[int(ans)-1])
                            else:
                                print Fore.RED + "Wrong input!" + Style.RESET_ALL

def x(remote_command, c):
    print c
    command = remote_command + c
    if len(remote_command) > 0:
        command += "'"
    command = shlex.split(command)
    subprocess.Popen(command)

main()