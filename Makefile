COMPOSE := COMPOSE_BAKE=true docker compose -f docker-compose.yml

all: build up

up:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

# launch:
# 	$(COMPOSE) run --rm app java -jar matcha.jar

start:
	$(COMPOSE) start

restart:
	$(COMPOSE) restart

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down --rmi all --volumes --remove-orphans

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

images:
	docker images

volume:
	docker volume ls

clean:
	$(MAKE) down 
	mvn -f ./back-matcha/pom.xml clean

prune: clean
	docker system prune -f -a

re: prune all

mvn:
	mvn -f ./back-matcha/pom.xml clean package

matcha:
	$(COMPOSE) exec app sh

postgres:
	$(COMPOSE) exec db sh

nginx:
	$(COMPOSE) exec nginx sh

.PHONY: all up build start restart stop down ps logs images volume clean prune matcha postgres nginx re