import subprocess

subprocess.check_output("eval $(minishift docker-env)", shell=True)

subprocess.check_output("docker login -u developer -p $(oc whoami -t) 172.30.1.1:5000", shell=True)


pull_list = [
	'mongo:latest'
	'weaveworksdemos/catalogue:0.3.5'
	'weaveworksdemos/user:0.4.4'
	'weaveworksdemos/payment:0.4.3'
	'weaveworksdemos/front-end:0.3.12'
	'weaveworksdemos/shipping:0.4.8'
	'weaveworksdemos/carts:0.4.8'
	'weaveworksdemos/orders:0.4.7'
	'weaveworksdemos/queue-master:0.3.1'
	'weaveworksdemos/catalogue-db:0.3.0'
	'weaveworksdemos/user-db:0.4.0']

for image in pull_list:
	command = "docker pull {}".format(image)
	subprocess.check_output(command1, shell=True)

images = {  "mongo" : "mongo",
						"weaveworksdemos/catalogue" : "catalogue",
						"rabbitmq" : "rabbitmq",
						"weaveworksdemos/user" : "user",
						"weaveworksdemos/payment" : "payment",
						"weaveworksdemos/front-end" : "front-end",
						"weaveworksdemos/shipping" : "shipping",
						"weaveworksdemos/carts" : "carts",
						"weaveworksdemos/orders" : "orders",
						"weaveworksdemos/queue-master" : "queue-master",
						"weaveworksdemos/catalogue-db" : "catalogue-db",
						"weaveworksdemos/user-db" : "user-db"
						}

images_manifest = subprocess.check_output("docker images | awk '{print $1 \" \" $2 \" \" $3}'", shell=True)

for line in images_manifest.split("\n"):
	splitline = line.split(" ")
	if splitline[0] in images:
		command1 = "docker tag {} 172.30.1.1:5000/sock-shop/{}:latest".format(splitline[2], images[splitline[0]])
		command2 = "docker push 172.30.1.1:5000/sock-shop/{}:latest".format(images[splitline[0]])
		print(subprocess.check_output(command1, shell=True))
		print(subprocess.check_output(command2, shell=True))

subprocess.check_output("docker tag mongo:latest 172.30.1.1:5000/sock-shop/carts-db:latest", shell=True)
subprocess.check_output("docker push 172.30.1.1:5000/sock-shop/carts-db:latest", shell=True)
subprocess.check_output("docker tag mongo:latest 172.30.1.1:5000/sock-shop/orders-db:latest", shell=True)
subprocess.check_output("docker push 172.30.1.1:5000/sock-shop/orders-db:latest", shell=True)