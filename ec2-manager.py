### Description: This is the EC2 Manager, a boto3 script that is designed to change the state of the existing EC2 instances.
### Author: Nicholas Doropoulos
### Version: 1

import boto3
import sys

# Defining the user's named profile so that a custom session is used instead of the default one
profile = input("What is the profile name of your IAM entity? ")

# Configuring a custom session using the resource object
custom_session = boto3.session.Session(profile_name=profile)
ec2_con_re = custom_session.resource(service_name="ec2", region_name="eu-west-1")

# Displaying the menu of available actions
while True:
    print("""
        1. Describe my instances
        2. Start an instance
        3. Stop an instance
        4. Reboot an instance
        5. Terminate an instance
        6. Exit
        """
        )
    # Getting the option supplied by the user and storing it inside a variable    
    option = int(input("What is your option?  "))
    if option == 1:
        print("")
        print("Describing all instances...")
        print("")
        existing_instances = ec2_con_re.instances.all()
        # Looping through all existing instances and print their IDs along with their status
        for instance in existing_instances:
            print("InstanceID: " + instance.id + " " + "State: " + str(instance.state['Name']))
    elif option == 2:
        supplied_id_for_starting = input("What is the ID of the instance you wish to start? ")
        # Starting the instance specified on the condition that it's currently stopped
        for i in existing_instances:
            if i.state['Name'] == "stopped" and i.id == supplied_id_for_starting:
                i.start() # Start the instance
                print("Starting an instance...")
                i.wait_until_running() # A waiter that has the user wait until the specified instance is running again
                print("Your instance has started!")
            else:
                break          
    elif option == 3:
        supplied_id_for_stopping = input("What is the ID of the instance you wish to stop? ")
        # Stopping the instance specified on the condition that it's currently running
        for i in existing_instances:
            if i.state['Name'] == "running" and i.id == supplied_id_for_stopping:
                i.stop() # Stop the instance 
                print("Stopping the instance...")
                i.wait_until_stopped() # A waiter that has the user wait until the specified instance has stopped
                print("Your instance has stopped.")
            else:
                break
    elif option == 4:
        supplied_id_for_rebooting = input("What is the ID of the instance you wish to reboot? ")
        # Rebooting the instance specified on the condition that it's currently running
        for i in existing_instances:
            if i.state['Name'] == "running" and i.id == supplied_id_for_rebooting:
                i.reboot() # Reboot the instance
                print("Rebooting the instance")
    elif option == 5:
        supplied_id_for_terminating = input("What is the ID of the instance you wish to terminate? ")
        # Terminating the instance specified on the condition that it's not already terminated
        for i in existing_instances:
            if i.state['Name'] != "terminated" and i.id == supplied_id_for_terminating:
                i.terminate() # Terminate the instance
                print("Terminating the instance...")
                i.wait_until_terminated() # A waiter that has the user wait until the specified instance has been terminated
                print("Your instance has been terminated.")
            else:
                break 
    elif option == 6:
        sys.exit()
    else:
        print("Your option is not valid. Try again...")
    
   
