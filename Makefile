LOG_LINES = 100
FG = FALSE
UPDATE = FALSE
DATE_PREFIX = `date +'%Y_%m_%d-%Hh'`
 DOCKER_UP := docker-compose up
DOCKER_LOGS := docker-compose logs --tail=$(LOG_LINES)
DOCKER_START := docker-compose start
DOCKER_STOP := docker-compose stop
 ifeq ($(FG), TRUE)
	DOCKER_UP += -d
endif
 ifdef FOLLOW
	DOCKER_LOGS += -f
endif
 ifdef SERVICES
	DOCKER_UP += $(SERVICES)
	DOCKER_LOGS += $(SERVICES)
	DOCKER_STOP += $(SERVICES)
	DOCKER_START += $(SERVICES)
	DOCKER_RECREATE := docker-compose rm -s $(SERVICES); docker-compose up -d $(SERVICES)
endif
 .DEFAULT_GOAL : help
 help:
	@echo "Welcome to Agorapi make file."
	@echo "This file is intended to ease your life regarding docker-compose commands."
	@echo "Bellow you will find the options you have with this makefile."
	@echo "You just need to run 'make <command> <arguments..>'."
	@echo "    "
	@echo "    help - Print this help message"
	@echo "    "
	@echo "    run [FG=FALSE] [SERVICES=ALL]"
	@echo "        Run the project in Background mode by default."
	@echo "        FG: Define as TRUE to run in foreground."
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "    "
	@echo "    logs [LOG_LINES=100] [SERVICES=ALL] [FOLLOW=TRUE]"
	@echo "        See services logs."
	@echo "        LOG_LINES: The number of log lines for each service"
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "        FOLLOW: keep tracking the logs. E.g.: FOLLOW=TRUE"
	@echo "    "
	@echo "    stop [SERVICES=ALL]"
	@echo "        Stop one or more services."
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "    "
	@echo "    start [SERVICES=ALL]"
	@echo "        Start one or more stopped services."
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "    "
	@echo "    recreate SERVICES='<service_a> <service_b> ...'"
	@echo "        Remove and recreate the given services/containers, but not their volumes."
	@echo "    "
	@echo "    clean"
	@echo "        stop and remove all service containers and images."
	@echo "    "
	@echo "    clean-containers"
	@echo "        remove all containers, keeping images and volumes"
	@echo "    "
	@echo "    clean-volumes"
	@echo "        remove all volumes. It also remove containers"
	@echo "    "
	@echo "    clean-repo"
	@echo "        Clean the current repo by undoing all uncommited changes and remove untracked git files"
	@echo "    "
	@echo "    makemigrations"
	@echo "    "
	@echo "    migrate"
	@echo "    "
	@echo "    import"
	@echo "       Import csv files in data and write on DB"
	@echo "    "
	@echo "    import-csv-remote"
	@echo "        This command will download all csvs from the remote server"
	@echo "    "
	@echo "    shell"
	@echo "        This command will open a psql terminal to manage the DB"
	@echo "    "
	@echo "    test"
	@echo "        This command will run the tests for the repository"
	@echo "    "
	@echo "    get-heroku-api-key"
	@echo "        This command will run the heroku cli to get API KEY"
	@echo "    "
	@echo "    download-remote-db-heroku"
	@echo "        This command will download the heroku remote Database"  sync-db-with-heroku
	@echo "    "
	@echo "    import-dump-to-db"
	@echo "        This command will restore the dump to the local db"
	@echo "    "
	@echo "    sync-db-with-heroku"
	@echo "        This command will synchronize the local db with the remote db on heroku. Careful! Some of your local data could be lost."
	@echo "    "
	@echo "    update migrate=true data=remote"
	@echo "        This command will clean the DB and get the data from the remote server."
	@echo "    "
	@echo "    update-data [model=model_name]"
	@echo "        This command will clean a specific table and import its data"
.PHONY: help
 run:
	@$(DOCKER_UP)
.PHONY: run
 logs:
	$(DOCKER_LOGS)
.PHONY: logs
 stop:
	@$(DOCKER_STOP)
.PHONY: stop
 start:
	@$(DOCKER_START)
.PHONY: start
 recreate:
ifndef DOCKER_RECREATE
	@echo "You need to pass the services you want to recreate with SERVICE='service_a_name service_b_name'"
	@exit 1
else
	@$(DOCKER_RECREATE)
endif
.PHONY: recreate
 clean:
	docker-compose down --rmi all
.PHONY: clean
 clean-containers:
	docker-compose down
.PHONY: clean-containers
 clean-volumes:
	docker-compose down --rmi local -v
.PHONY: clean-containers
 clean-repo:
	git reset --hard HEAD
	git clean -di -e '.env'
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
.PHONY: clean-pyc
 makemigrations:
	docker exec -it "agorapi" sh -c './manage.py makemigrations'
.PHONY: makemigrations
 migrate:
	docker exec -it "agorapi" sh -c './manage.py migrate'
.PHONY: migrate
 import:
	docker exec -it "agorapi" sh -c './manage.py flush --no-input; ./manage.py import_all_data'
.PHONY: reset
 import-csv-remote:
	docker exec -it "agorapi" sh -c './manage.py import_csvs_from_remote'
.PHONY: import-csv-remote
 shell:
	docker exec -it "dbapi" psql -U postgres
.PHONY: shell
 test:
	docker exec -it agorapi sh -c './manage.py test_all'
.PHONY: test
 get-heroku-api-key:
	docker-compose run --rm heroku-cli sh login_heroku_cli.sh
.PHONY: get-heroku-api-key
 download-remote-db-heroku:
	docker-compose run --rm heroku-cli sh download_remote_db.sh
.PHONY: download-remote-db-heroku
 import-dump-to-db:
	docker exec -it dbapi sh -c 'pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d postgres /backup_data/latest.dump'
.PHONY: import-dump-to-db
 sync-db-with-heroku: download-remote-db-heroku import-dump-to-db
.PHONY: sync-db-with-heroku
 update:
ifeq ($(migrate), true)
	docker exec -it "agorapi" sh -c './manage.py makemigrations'
	docker exec -it "agorapi" sh -c './manage.py migrate'
endif
	docker exec -it "agorapi" sh -c './manage.py flush --no-input'
ifeq ($(data), remote)
	docker exec -it "agorapi" sh -c './manage.py import_all_data_from_remote'
else
	docker exec -it "agorapi" sh -c './manage.py import_all_data'
endif
.PHONY: update
 update-data:
	docker exec -it agorapi sh -c './manage.py update_data --model $(model)'
.PHONY: update-data

