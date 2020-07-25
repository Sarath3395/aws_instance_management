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


class CreateDict:
    def __init__(self):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    def new_dict(self, dictname):
        setattr(self, dictname, {})

    def add_node(self, parent, nodename):
        node = parent[nodename] = {}
        return node

    def add_cell(self, nodename, cellname, value):
        cell = nodename[cellname] = value
        return cell

    def display_dict(self, dictname, level=0):
        indent = " " * (4 * level)
        for key, value in dictname.items():
            if isinstance(value, dict):
                print(f'\n{indent}{key}')
                level += 1
                self.display_dict(value, level)
            else:
                print(f'{indent}{key}: {value}')
            if level > 0:
                level -= 1





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

def get_instance_type(ec2_con_re,in_id):
    for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
        response = each.describe_attribute(
            Attribute='instanceType')
        ty=response['InstanceType']['Value']

    return ty


def start_instance(ec2_con_re,in_id):
    pr_st=get_instance_state(ec2_con_re,in_id)
    if pr_st=="running":
        print("instance is already running")
    else:
        for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
            each.start()
            print("please wait it is going to strat, once if it is strated then we will let you know")
            # each.wait_until_running()
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
            # each.wait_until_stopped()
            print("now it is stopped")


def welcome():
    print("this script will help you to start or stop ec2 instance based on your required region and instance id")
    print("Enjou it")
    time.sleep(3)

def main(start_stops,instance_id,region,aws_access_key_id,aws_secret_access_key):
    welcome()


    #my_region=raw_input("Endter your region name:")
    #my_region="us-east-1"

    ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
    #in_id=raw_input("now choose your instance id to start or stop:")
    in_id=instance_id
    #start_stop=raw_input("enter either start or stop command for youe ec2 instance:")
    start_stop=start_stops

    if start_stop=="start":
        start_instance(ec2_con_re,in_id)
    else:
        stop_instance(ec2_con_re,in_id)
    Thank_you()




def stop(request):

    instance_id = request.GET["instance_id"]
    region = request.session['region']
    aws_access_key_id=request.session['session_aws_access_key_id']
    aws_secret_access_key=request.session['session_aws_secret_access_key']

    main("stop",instance_id,region,aws_access_key_id,aws_secret_access_key)
    ec2_con_re={}
    ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))
    list=list_instances_on_my_region(ec2_con_re)

    status = {}
    for each in list:

        prs = get_instance_state(ec2_con_re, each)
        type = get_instance_type(ec2_con_re, each)


        status[each] = {}
        status[each]['type'] = type
        status[each]['status'] = prs

        # status[each]['type']=type

    print("finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    print(status)

    return render(request, 'instances.html',{'region':region, 'status':status})


def start(request):
    instance_id = request.GET["instance_id"]
    region = request.session['region']
    aws_access_key_id=request.session['session_aws_access_key_id']
    aws_secret_access_key=request.session['session_aws_secret_access_key']
    #print("+++++++++++"+instance_id)
    main("start",instance_id,region,aws_access_key_id,aws_secret_access_key)
    #return redirect('regioninstances')

    ec2_con_re={}
    ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))
    list=list_instances_on_my_region(ec2_con_re)

    status = {}
    for each in list:

        prs = get_instance_state(ec2_con_re, each)
        type = get_instance_type(ec2_con_re, each)
        

        status[each] = {}
        status[each]['type'] = type
        status[each]['status'] = prs

        # status[each]['type']=type

    print("finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    print(status)

    return render(request, 'instances.html',{'region':region, 'status':status})





def regioninstances(request):

    if request.method == 'POST':

        region= request.POST['region']
        request.session['region'] = region

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
            type = get_instance_type(ec2_con_re, each)
            if(prs=="terminated"):
                ondemandinstancecreate(aws_access_key_id,aws_secret_access_key)

            status[each]={}
            status[each]['type']=type
            status[each]['status'] = prs

            # status[each]['type']=type

        print("finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        print(status)



        return render(request, 'instances.html',{'region':region, 'status':status})


    else:
        return render(request, 'index.html')


def ondemandinstancecreate(my_aws_access_key_id,my_aws_secret_access_key):
    print("ondemand_creation")
    # session = boto3.Session(
    #     aws_access_key_id=my_aws_access_key_id,
    #     aws_secret_access_key=my_aws_secret_access_key,
    # )
    # client = session.client('ec2')
    # client.run_instances(ImageId='ami-08f3d892de259504d',
    #                             InstanceType='t2.micro',
    #                             MinCount=1,
    #                             MaxCount=1)

def get_more_tables(request):
    increment = int(request.GET['append_increment'])
    increment_to = increment + 10

    region = request.session['region']
    aws_access_key_id = request.session['session_aws_access_key_id']
    aws_secret_access_key = request.session['session_aws_secret_access_key']

    ec2_con_re = {}
    ec2_con_re = get_ec2_con_for_given_region(region, aws_access_key_id, aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))
    list = list_instances_on_my_region(ec2_con_re)

    status = {}
    for each in list:

        prs = get_instance_state(ec2_con_re, each)
        type = get_instance_type(ec2_con_re, each)
        if (prs == "terminated"):
            ondemandinstancecreate(aws_access_key_id, aws_secret_access_key)

        status[each] = {}
        status[each]['type'] = type
        status[each]['status'] = prs

        # status[each]['type']=type

    print("finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    print(status)


    order = status
    return render(request, 'get_more_tables.html', {'status': order})





