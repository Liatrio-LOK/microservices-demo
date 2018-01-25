#!/usr/bin/python

import os
import time
import subprocess

dn = open(os.devnull, 'w')

commands = [
  ["oc login https://$(minishift ip):8443 -u system:admin", ""],
  ["oc delete user developer", "deleting default users and projects..."],
  ["oc delete project myproject", ""],
  ["oc create user admin", "creating users..."],
  ["oc create user shipping-dev", ""],
  ["oc create user front-end-dev", ""],
  ["oc adm groups new shipping", "creating groups..."],
  ["oc adm groups new front-end", ""],
  ["oc adm groups add-users shipping admin shipping-dev", "adding users to groups..."],
  ["oc adm groups add-users front-end admin front-end-dev", ""],
  ["oc new-project sock-shop", "creating sock-shop project..."],
  ["oc adm policy add-role-to-user admin admin", "setting sock-shop project permissions..."],
  ["oc adm policy add-role-to-user view shipping-dev", ""],
  ["oc adm policy add-role-to-user view front-end-dev", ""],
  ["oc project default", ""],
  ["WAIT-FOR-REGISTRY", "waiting for openshift registry to be ready..."],
  ["oc login https://$(minishift ip):8443 -u admin -p admin", ""],
  ["oc project sock-shop", "creating build configurations and image streams in sock-shop project..."],
  ["oc create -f builds/shipping.yaml", ""],
  ["oc create -f builds/front-end.yaml", ""],
  ["oc create -f resources/image_streams.yaml", ""],
  ["python setup_images.py", "pushing default images to the sock-shop project..."],
  ["oc login https://$(minishift ip):8443 -u system:admin", ""],
  ["oc new-project ci", "creating ci project..."],
  ["oc adm policy add-role-to-user admin admin", "setting ci project permissions..."],
  ["oc adm policy add-role-to-user view shipping-dev", ""],
  ["oc adm policy add-role-to-user view front-end-dev", ""],
  ["oc process -f jenkins/jenkins.json | oc create -f -", "adding a persistent jenkins deployment to ci project..."],
  ["oc adm policy add-role-to-user admin system:serviceaccount:ci:jenkins", "setting ci project and cluster permissions for jenkins service account..."],
  ["oc adm policy add-cluster-role-to-user view system:serviceaccount:ci:jenkins", ""],
  ["oc adm policy add-cluster-role-to-user self-provisioner system:serviceaccount:ci:jenkins", ""],
  ["oc adm policy add-scc-to-group anyuid system:authenticated", "setting scc to allow pod containers to be run as root..."],
  ["oc adm policy add-cluster-role-to-group system:image-puller system:authenticated --namespace=sock-shop", "setting permissions to allow everyone to pull images from sock-shop project..."],
]

print("""
 ______     __         __  __     ______     ______   ______     ______    
/\  ___\   /\ \       /\ \/\ \   /\  ___\   /\__  _\ /\  ___\   /\  == \   
\ \ \____  \ \ \____  \ \ \_\ \  \ \___  \  \/_/\ \/ \ \  __\   \ \  __<   
 \ \_____\  \ \_____\  \ \_____\  \/\_____\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_____/   \/_____/     \/_/   \/_____/   \/_/ /_/ 
                                                                           
                 ______     ______     ______   __  __     ______           
                /\  ___\   /\  ___\   /\__  _\ /\ \/\ \   /\  == \          
                \ \___  \  \ \  __\   \/_/\ \/ \ \ \_\ \  \ \  _-/          
                 \/\_____\  \ \_____\    \ \_\  \ \_____\  \ \_\            
                  \/_____/   \/_____/     \/_/   \/_____/   \/_/            

""")

for command in commands:
  if (command[1] != ""):
    print(command[1])
  
  if (command[0] == "WAIT-FOR-REGISTRY"):
    for i in range(0, 180):
      output = subprocess.check_output("oc get pods | grep 'docker-registry' | awk '{print $3}'", shell=True)
      
      if ((output == "Running\n") | (output == "Running\nRunning")):
        print("openshift registry is ready!")
        break
      elif (i == 179):
        print("openshift registry failed to start!")
        quit()
      
      time.sleep(5)
  else:
    subprocess.check_call(command[0], stdout=dn, stderr=dn, shell=True)
