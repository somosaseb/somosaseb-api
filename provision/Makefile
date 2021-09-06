
setup:
	ansible-playbook -vv --exclude-tags vhost playbooks/setup.py

deploy:
	tar cpf - playbooks | ssh -t apps@54.205.144.51 " \
		tar xpf - -C /tmp && \
		cd /tmp/playbooks && \
		bash /tmp/playbooks/deploy.sh && \
		rm -rf /tmp/playbooks \
	"
restart:
	ssh -t apps@54.205.144.51 'bash -s' < playbooks/restart.sh
