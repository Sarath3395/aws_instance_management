from django.shortcuts import render
import boto3
import sys
import os
import time


# Create your views here.

def index(request):

    return render(request, 'index.html')



def get_ec2_con_for_given_region(my_region):
    session = boto3.Session(
            aws_access_key_id="AKIAJBNEB6XPLCWB56WA",
            aws_secret_access_key="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",
        )
    ec2_con_re = session.resource('ec2',region_name=my_region)
    return ec2_con_re

def list_instances_on_my_region(ec2_con_re):
    for each in ec2_con_re.instances.all():
        print(each.id)

def get_instance_state(ec2_con_re,in_id):
    for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
        pr_st=each.state['Name']
    return pr_st

def start_instance(ec2_con_re,in_id):
    pr_st=get_instance_state(ec2_con_re,in_id)
    if pr_st=="running":
        print("instance is already running")
    else:
        for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
            each.start()
            print("please wait it is going to strat, once if it is strated then we will let you know")
            each.wait_until_running()
            print("now it is running")
    return

def Thank_you():
    print("\n\n*************thank you for using this scirpt**************")
    return None

def stop_instance(ec2_con_re,in_id):
    pr_st=get_instance_state(ec2_con_re,in_id)
    if pr_st=="stopped":
        print ("instance is already stopped")
    else:
        for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
            each.stop()
            print ("please wait it is going to stop, once it is stopped then we will let you know")
            each.wait_until_stopped()
            print("now it is stopped")


def welcome():
    print("this script will help you to start or stop ec2 instance based on your required region and instance id")
    print("Enjou it")
    time.sleep(3)

def main():
    welcome()


    #my_region=raw_input("Endter your region name:")
    my_region="us-east-1"
    print("please wait connecting to your aws ec2 console")
    ec2_con_re=get_ec2_con_for_given_region(my_region)
    print("please wait listing all instances ids in your region{}".format(my_region))
    list_instances_on_my_region(ec2_con_re)
    #in_id=raw_input("now choose your instance id to start or stop:")
    in_id="i-093f0b73a2ed67c2d"
    #start_stop=raw_input("enter either start or stop command for youe ec2 instance:")
    start_stop="start"
    while True:
        if start_stop not in ["start","stop"]:
            start_stop=raw_input("enter only start or stop commands:")
            continue
        else:
            break
    if start_stop=="stop":
        start_instance(ec2_con_re,in_id)
    else:
        stop_instance(ec2_con_re,in_id)
    Thank_you()





def stop(request):
    #session = boto3.Session(
    #    aws_access_key_id="AKIAJBNEB6XPLCWB56WA",
    #    aws_secret_access_key="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",
    #)
    #ec2 = session.resource('ec2')
    #instance = ec2.Instance('i-093f0b73a2ed67c2d')
    #instance.stop()
    main()
    return render(request, 'instance.html')

