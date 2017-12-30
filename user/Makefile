current_dir = $(shell pwd)
config_dir = $(current_dir)/data/config
keystore_path := $(config_dir)/keystore
pwd_path := $(config_dir)/password.txt

new-account:
	@echo "\n🌟 Creating keystore directory at $(keystore_path)\n"
	mkdir -p $(keystore_path)
ifeq ($(wildcard $(pwd_path)),)
	@read -s -p "🌟 Enter a new password to encrypt your account:" pwd; \
	echo "$$pwd" > $(pwd_path)
	@echo "\n🌟 Your password is stored at $(pwd_path)\n"
else
	@echo "\n🌟 Will encrypt your account with $(pwd_path)"
endif

	@echo "\n🌟 Pyethapp container is creating new address for you, might take few seconds:\n"
	docker run -it --rm \
	-v $(config_dir):/root/.config/pyethapp \
	ethresearch/pyethapp-research:alpine \
	pyethapp --password /root/.config/pyethapp/password.txt account new

	@echo "\n🌟 New address created at $(keystore_path)\n"
	ls $(keystore_path)