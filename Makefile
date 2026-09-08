COMPOSE := COMPOSE_BAKE=true docker compose -f docker-compose.yaml

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

prune: clean
	docker system prune -f -a

re: prune all

matcha:
	$(COMPOSE) exec app sh

postgres:
	$(COMPOSE) exec db sh
# 	$(COMPOSE) exec db psql -U $$(POSTGRES_USER) -d $$(POSTGRES_DB)

nginx:
	$(COMPOSE) exec nginx sh

.PHONY: all up build start restart stop down ps logs images volume clean prune matcha postgres nginx re