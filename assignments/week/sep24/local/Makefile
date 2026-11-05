NAME ?= week4-local
IMAGE ?= 24.04

help:
	@echo "Available commands:"
	@echo "make launch"
	@echo "make list"
	@echo "make info"
	@echo "make shell"
	@echo "make start"
	@echo "make stop"
	@echo "make restart"
	@echo "make test"
	@echo "make delete"
	@echo "make purge"

launch:
	multipass launch $(IMAGE) --name $(NAME) --cpus 2 --memory 2G --disk 10G

list:
	multipass list

info:
	multipass info $(NAME)

shell:
	multipass shell $(NAME)

start:
	multipass start $(NAME)

stop:
	multipass stop $(NAME)

restart:
	multipass restart $(NAME)

test:
	multipass exec $(NAME) -- uname -a
	multipass exec $(NAME) -- ls -la

delete:
	multipass delete $(NAME)

purge:
	multipass purge
