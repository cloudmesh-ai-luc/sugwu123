CLOUD ?= openstack
NAME ?= sugwu-week4-js2
FLAVOR ?= m3.tiny
IMAGE ?= Featured-Minimal-Ubuntu24
KEY ?= sugwu
NETWORK ?= auto_allocated_network
SECURITY_GROUP ?= remotelogin

OS = openstack --os-cloud $(CLOUD)

help:
	@echo "Jetstream 2 VM commands:"
	@echo "make list"
	@echo "make create"
	@echo "make info"
	@echo "make stop"
	@echo "make start"
	@echo "make delete"
	@echo "make images"
	@echo "make flavors"
	@echo "make floating-ips"
	@echo "make create-ip"
	@echo "make attach-ip FLOATING_IP=x.x.x.x"

list:
	$(OS) server list

create:
	$(OS) server create \
		--flavor $(FLAVOR) \
		--image "$(IMAGE)" \
		--key-name $(KEY) \
		--security-group $(SECURITY_GROUP) \
		--network $(NETWORK) \
		--wait \
		$(NAME)

info:
	$(OS) server show $(NAME)

stop:
	$(OS) server stop $(NAME)

start:
	$(OS) server start $(NAME)

delete:
	$(OS) server delete $(NAME)

images:
	$(OS) image list

flavors:
	$(OS) flavor list

floating-ips:
	$(OS) floating ip list

create-ip:
	$(OS) floating ip create public

attach-ip:
	$(OS) server add floating ip $(NAME) $(FLOATING_IP)
