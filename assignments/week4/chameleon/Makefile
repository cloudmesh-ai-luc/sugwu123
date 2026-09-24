NAME ?= sugwu-week4-chameleon
FLAVOR ?= reservation:5f64434a-2031-4f72-bc7b-eeff195d54f5
IMAGE ?= CC-Ubuntu24.04
KEY ?= sugwu
NETWORK ?= sharednet1
SECURITY_GROUP ?= sugwu-ssh

help:
	@echo "Chameleon VM commands:"
	@echo "make list"
	@echo "make create"
	@echo "make info"
	@echo "make stop"
	@echo "make start"
	@echo "make delete"
	@echo "make images"
	@echo "make flavors"
	@echo "make networks"
	@echo "make keypairs"

list:
	openstack server list

create:
	openstack server create \
		--flavor $(FLAVOR) \
		--image "$(IMAGE)" \
		--key-name $(KEY) \
		--security-group $(SECURITY_GROUP) \
		--nic net-id=$(NETWORK) \
		--wait \
		$(NAME)

info:
	openstack server show $(NAME)

stop:
	openstack server stop $(NAME)

start:
	openstack server start $(NAME)

delete:
	openstack server delete $(NAME)

images:
	openstack image list

flavors:
	openstack flavor list

networks:
	openstack network list

keypairs:
	openstack keypair list
