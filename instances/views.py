from django.shortcuts import render,redirect
import boto3
import sys
import os
import time
# Create your views here.
ins =[]
region = ""
aws_access_key_id = ""
aws_secret_access_key = ""



def get_ec2_con_for_given_region(my_regions,my_aws_access_key_id,my_aws_secret_access_key):
    session = boto3.Session(
            aws_access_key_id=my_aws_access_key_id,
                aws_secret_access_key=my_aws_secret_access_key,
        )
    ec2_con_re = session.resource('ec2',region_name=my_regions)
    return ec2_con_re

def list_instances_on_my_region(ec2_con_re):
    ins =[]
    for each in ec2_con_re.instances.all():
        print(each.id)
        ins.append(each.id)
    return ins
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

def main(start_stops,instance_id,region,aws_access_key_id,aws_secret_access_key):
    welcome()


    #my_region=raw_input("Endter your region name:")
    #my_region="us-east-1"
    print("please wait connecting to your aws ec2 console")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&77"+region+aws_access_key_id+aws_secret_access_key)
    ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))
    list_instances_on_my_region(ec2_con_re)
    #in_id=raw_input("now choose your instance id to start or stop:")
    in_id=instance_id
    #start_stop=raw_input("enter either start or stop command for youe ec2 instance:")
    start_stop=start_stops
    while True:
        if start_stop not in ["start","stop"]:
            start_stop=raw_input("enter only start or stop commands:")
            continue
        else:
            break
    if start_stop=="start":
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
    instance_id = request.GET["instance_id"]
    region = request.GET["region"]
    aws_access_key_id=request.session['session_aws_access_key_id']
    aws_secret_access_key=request.session['session_aws_secret_access_key']

    main("stop",instance_id,region,aws_access_key_id,aws_secret_access_key)


    ec2_con_re={}
    ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))
    list=list_instances_on_my_region(ec2_con_re)

    status={}
    for each in list:
        prs=get_instance_state(ec2_con_re,each)
        status[each]=prs

    print(status)

    return render(request, 'instances.html',{'region':region, 'status':status})


    #return render(request, 'instancestopped.html')

def start(request):
    instance_id = request.GET["instance_id"]
    region = request.GET["region"]
    aws_access_key_id=request.session['session_aws_access_key_id']
    aws_secret_access_key=request.session['session_aws_secret_access_key']
    #print("+++++++++++"+instance_id)
    main("start",instance_id,region,aws_access_key_id,aws_secret_access_key)
    #return redirect('regioninstances')



    ec2_con_re={}
    ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))
    list=list_instances_on_my_region(ec2_con_re)

    status={}
    for each in list:
        prs=get_instance_state(ec2_con_re,each)
        status[each]=prs

    print(status)

    return render(request, 'instances.html',{'region':region, 'status':status})
    #return render(request, 'instancestarted.html')
    #return redirect(request.META['HTTP_REFERER'])




def regioninstances(request):

    if request.method == 'POST':
        region= request.POST['region']
        aws_access_key_id= request.POST['aws_access_key']
        request.session['session_aws_access_key_id'] = aws_access_key_id
        aws_secret_access_key= request.POST['aws_secret_access_key']
        request.session['session_aws_secret_access_key'] = aws_secret_access_key

        ec2_con_re={}
        ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
        print("please wait listing all instances ids in your region{}".format(region))
        list=list_instances_on_my_region(ec2_con_re)

        status={}
        for each in list:

            prs=get_instance_state(ec2_con_re,each)
            status[each]=prs

        print(status)

        return render(request, 'instances.html',{'region':region, 'status':status})


    else:
        return render(request, 'index.html')