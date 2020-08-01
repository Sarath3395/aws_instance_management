from django.shortcuts import render,redirect
from .models import  instance_creation,ami_creation,check_spot
from aws.models import c4cxlargetable,t2micro
from datetime import datetime, timedelta


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

def get_session(region, usr_aws_access_key_id,usr_aws_secret_access_key):
    session = boto3.Session(
        aws_access_key_id=usr_aws_access_key_id,
        aws_secret_access_key=usr_aws_secret_access_key,
    )
    client = session.client('ec2', region_name=region)
    return client

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

def get_instance_img(in_id, session):
    # clt = session.client('ec2', region_name=region)
    response = session.describe_instances(

        InstanceIds=[
            in_id,
        ],

    )
    print("dddddddddddddddddddddddddddddddddd")
    for r in response['Reservations']:
        for i in r['Instances']:
            print(i['ImageId'])
            img_id=i['ImageId']
    return img_id


def ami_creation_spot(in_id, session):
    # clt = session.client('ec2', region_name=region)
    # client = boto3.client('ec2')

    image = session.create_image(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'VirtualName': 'string',
                'Ebs': {
                    'DeleteOnTermination': True,
                },
            },
        ],
        Description=in_id,
        DryRun=False,
        InstanceId=in_id,
        Name=in_id,
        NoReboot=False
    )
    # image.wait_until_exists()
    print("created ami")
    print(image['ImageId'])
    return image['ImageId']


def check_spot_or_not(ec2_con_re):
    ec2 = ec2_con_re
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','stopped','terminated','shutting-down']}])
    spot_ins = []
    # ami_obj = ami_creation(instance_id=each, ami_id=ami_id)
    # ami_obj.save()
    print("innnnnnnnn chkkkkkkkkkkkkkkkk")
    for instance in instances:
        print(instance)
        if instance.spot_instance_request_id:
            print(instance.instance_id, 'is a SPOT instance')
            # if (check_spot.objects.filter(instance_id=instance.instance_id).exists()) == 0:
            #     chk_obj = check_spot(instance_id=instance.instance_id, spot_indi=1)
            #     chk_obj.save()
            spot_ins.append(instance.instance_id)

        else:
            print(instance.instance_id, 'is a ON-Demand instance')
            # if (check_spot.objects.filter(instance_id=instance.instance_id).exists()) == 0:
            #     chk_obj = check_spot(instance_id=instance.instance_id, spot_indi=0)
            #     chk_obj.save()

    return spot_ins

def get_platform_details( ami, session):
    print()
    # clt = session.client('ec2', region_name=region)

    # client = boto3.client('ec2')

    response = session.describe_images(

        ImageIds=[
            ami,
        ],

        DryRun=False
    )
    ami_det = {}
    for image in response['Images']:

        print(image['PlatformDetails'])
        ami_det['platform'] = image['PlatformDetails']
        ami_det['state'] = image['State']

    return ami_det



def get_az( ins_id, session):
    print()
    # clt = session.client('ec2', region_name=region)

    # client = boto3.client('ec2')
    response = session.describe_instances(

        InstanceIds=[
            ins_id,
        ],

    )
    az=""
    print("azzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    for r in response['Reservations']:
        for i in r['Instances']:
            print(i['Placement']['AvailabilityZone'])
            az=i['Placement']['AvailabilityZone']

    return az


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

def get_curnt_sp(ins_type,platform_det,az, session):
    # clt = session.client('ec2', region_name=region)

    prices = session.describe_spot_price_history(InstanceTypes=[ins_type], MaxResults=1,
                                                ProductDescriptions=[platform_det], AvailabilityZone=az)
    print("sssssssssssssspppppppppppottttttttttttttttttttt")
    print(prices['SpotPriceHistory'][0])
    cr_sp = prices['SpotPriceHistory'][0]['SpotPrice']
    print(cr_sp)

    return cr_sp

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

def instance_termination(ins_id,ec2_con_re):
    # ec2 = boto3.resource('ec2')
    ids = [ins_id]
    ec2_con_re.instances.filter(InstanceIds=ids).terminate()
    # res.wait_until_terminated()

def get_spot_ins_id(req_id, session):
    # client = boto3.client('ec2')

    response = session.describe_spot_instance_requests(
        Filters=[
            {

            },
        ],
        DryRun=False,
        SpotInstanceRequestIds=[
            req_id,
        ],

    )
    print(response)
    for instance in response['SpotInstanceRequests']:
        ins_id = instance['InstanceId']
        print(ins_id)

    return ins_id

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
    c4 = t2micro.objects.all()

    if request.method == 'POST':

        region= request.POST['region']
        request.session['region'] = region

        aws_access_key_id= request.POST['aws_access_key']
        request.session['session_aws_access_key_id'] = aws_access_key_id

        aws_secret_access_key= request.POST['aws_secret_access_key']
        request.session['session_aws_secret_access_key'] = aws_secret_access_key

        bid_price= request.POST['bid_price']
        request.session['bid_price'] = bid_price


        ec2_con_re={}
        ec2_con_re=get_ec2_con_for_given_region(region,aws_access_key_id,aws_secret_access_key)
        print("please wait listing all instances ids in your region{}".format(region))

        session = get_session(region,aws_access_key_id,aws_secret_access_key)

        time = datetime.now().replace(microsecond=0, second=0, minute=0)

        now = time.strftime("%H:%M:%S")

        forcst_prc = t2micro.objects.filter(time = now)
        # forcst_prc = forcst_prc.price
        print("ffffffffffffffffffffffffffffffffffffffff")
        for person in forcst_prc:
            print(person.price)
            forcst_prc = person.price


        list=list_instances_on_my_region(ec2_con_re)

        statuss = {}
        spot_ins = check_spot_or_not(ec2_con_re)

        for each in list:

            prs=get_instance_state(ec2_con_re,each)
            type = get_instance_type(ec2_con_re, each)

            ami = get_instance_img(each, session)

            ami_det = get_platform_details( ami,session)

            platform = ami_det['platform']
            az = get_az( each,session)
            cr_sp = get_curnt_sp( type, platform, az,session)
            sp_in = 0

            if each in spot_ins:
                sp_in = 1

            # sp_in = check_spot.objects.filter(instance_id=each)
            # for prp in sp_in:
            #     print(prp.spot_indi)
            #     sp_in = prp.spot_indi


            statuss[each] = {}
            statuss[each]['type'] = type
            statuss[each]['status'] = prs
            statuss[each]['cr_sp'] = cr_sp
            statuss[each]['spot_indi'] = sp_in

            if((sp_in == 1) & (float(bid_price) < float(forcst_prc)) & (prs == 'running')):
                print("amiiiiiii creation for spot iinnnnnnnnnnnnnnnssssssssssssss")
                ami_id = ami_creation_spot(each, session)
                ami_obj = ami_creation(instance_id=each, ami_id=ami_id)
                ami_obj.save()
            print("ttttttttttttttttttttttttttttttttt")
            print(bid_price)
            print(cr_sp)
            print(sp_in)
            print(prs)
            if ((sp_in == 0) & (float(bid_price) == float(cr_sp)) & (prs == 'running')):
                print("amiiiiiii creation for spot iinnnnnnnnnnnnnnnssssssssssssss")
                ami_id = ami_creation_spot(each,session)
                ami_obj = ami_creation(instance_id=each, ami_id=ami_id)
                ami_obj.save()
            # status[each]['type']=type

        print("finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        print(statuss)


        return render(request, 'instances.html',{'region':region, 'status':statuss, 'c4': c4})


    else:
        # c4 = c4cxlargetable.objects.all()

        return render(request, 'index.html',{'c4': c4})


def ondemandinstancecreate(session,ins_type,ter_id,img):
    print("ondemand_creation")
    # session = boto3.Session(
    #     aws_access_key_id=my_aws_access_key_id,
    #     aws_secret_access_key=my_aws_secret_access_key,
    # )
    # client = session.client('ec2')
    created_ins = session.run_instances(ImageId=img,
                                InstanceType=ins_type,
                                MinCount=1,
                                MaxCount=1)
    print("createdddddddddddddddddddddddddd")
    for instance in created_ins['Instances']:
        cr_id =instance['InstanceId']
        print(cr_id)
        ins_cr = instance_creation(terminated_id=ter_id,creation_id=cr_id)
        ins_cr.save()


def spot_ins_creation(ami,_ins_type,az, session):
    # client = boto3.client('ec2')

    response = session.request_spot_instances(
        DryRun=False,
        SpotPrice='0.10',
        InstanceCount=1,
        Type='one-time',
        LaunchSpecification={
            'ImageId': ami,
            'InstanceType': _ins_type,
            'Placement': {
                'AvailabilityZone': az,
            },
            'BlockDeviceMappings': [
                {

                },
            ],

            'EbsOptimized': False,
            'Monitoring': {
                'Enabled': False
            },
            'SecurityGroupIds': [
            ]
        }
    )
    # response.wait_until_exists()
    for instance in response['SpotInstanceRequests']:
        req_id =instance['SpotInstanceRequestId']
        print("sssssssspppppppppppppppppppppppppppppppppp")
        print(req_id)
    return req_id


def get_more_tables(request):

    print("uu--------------------------------------------")
    increment = int(request.GET['append_increment'])
    increment_to = increment + 10

    region = request.session['region']
    aws_access_key_id = request.session['session_aws_access_key_id']
    aws_secret_access_key = request.session['session_aws_secret_access_key']

    ec2_con_re = {}
    ec2_con_re = get_ec2_con_for_given_region(region, aws_access_key_id, aws_secret_access_key)
    print("please wait listing all instances ids in your region{}".format(region))

    session = get_session(region, aws_access_key_id, aws_secret_access_key)
    list = list_instances_on_my_region(ec2_con_re)

    status = {}
    spot_ins = check_spot_or_not(ec2_con_re)

    bid_price = request.session['bid_price']


    for each in list:

        prs = get_instance_state(ec2_con_re, each)
        type = get_instance_type(ec2_con_re, each)


        ami = get_instance_img( each,session)


        ami_det = get_platform_details( ami,session)

        platform = ami_det['platform']
        # platform = get_platform_details(ami)
        az = get_az( each,session)
        cr_sp = get_curnt_sp(type,platform,az,session)


        spot_in = 0

        if each in spot_ins:
            spot_in = 1

        # sp_in = check_spot.objects.filter(instance_id=each)
        # for prp in sp_in:
        #     print(prp.spot_indi)
        #     sp_in = prp.spot_indi


        status[each] = {}
        status[each]['type'] = type
        status[each]['status'] = prs
        status[each]['cr_sp'] = cr_sp
        status[each]['sp_in'] = spot_in




        if ((prs == "terminated") & (spot_in == 1)):
            # if(each not in created_ins):



            if (instance_creation.objects.filter(terminated_id=each).exists()) == 0:
                print("onnnnnnnnnnn-dddddddddddddddd creation init")

                new_img = ami_creation.objects.filter(instance_id=each)

                for person in new_img:
                    print(person.ami_id)
                    new_img = person.ami_id

                new_ami_det = get_platform_details( new_img,session)
                # new_ami = new_ami_det['state']

                if((ami_creation.objects.filter(instance_id=each).exists() == 1) & (new_ami_det['state'] == 'available')):
                    print("spottttttttttammmmmmmmmmmmmmmmmmmmmmiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                    print(new_img)
                    ondemandinstancecreate(aws_access_key_id, aws_secret_access_key, type, each, new_img)
                else:

                     img = get_instance_img( each,session)
                     ondemandinstancecreate(aws_access_key_id, aws_secret_access_key, type, each, img)


            else:
                print("already instance is created")
        print("bid and crnt spot")
        print(float(bid_price))
        print(float(cr_sp))


        if ( (spot_in == 0) & (prs == "running") & (float(bid_price) == float(cr_sp))  ):
            print("terrrrrrrrrrrrrrrrrrrrrrrrrr on ")
            new_img = ami_creation.objects.filter(instance_id=each)

            for person in new_img:
                print(person.ami_id)
                new_img = person.ami_id

            new_ami_det = get_platform_details( new_img,session)
            if((new_ami_det['state'] == 'available')):
                instance_termination(each,ec2_con_re)


                # instance_termination(each)
        if ((spot_in == 0) & (prs == "terminated")):
            print("spot creation intiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            if (instance_creation.objects.filter(terminated_id=each).exists()) == 0:

                new_img = ami_creation.objects.filter(instance_id=each)

                for person in new_img:
                    print(person.ami_id)
                    new_img = person.ami_id

                new_ami_det = get_platform_details( new_img,session)

                if ((ami_creation.objects.filter(instance_id=each).exists() == 1) & (new_ami_det['state'] == 'available')):



                    print("ammmmmmmmmmmmmmmmmmmmmmiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                    print(new_img)
                    # instance_termination(each)
                    req_id = spot_ins_creation(new_img, type, az, session)

                    ins_cr = instance_creation(terminated_id=each, creation_id=req_id)
                    ins_cr.save()

                else:

                    img = get_instance_img( each,session)
                    # instance_termination(each)
                    req_id = spot_ins_creation(img, type, az, session)

                    ins_cr = instance_creation(terminated_id=each, creation_id=req_id)
                    ins_cr.save()





        # status[each]['type']=type

    print("finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    print(status)

    order = status
    print('u++++++++++++++++++++++++++++++++++++')
    c4 = t2micro.objects.all()
    return render(request, 'get_more_tables.html', {'status': order ,'c4': c4})





