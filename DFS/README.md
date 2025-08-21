# [DFS] 
### Dockerized FHIR-server with resources imported from a simple FHIR-repository

#### Start-Up

`docker compose up`

#### Check patient resources

`https://localhost:9090/fhir/Patient`

#### Shut-Down

`docker compose down`

`docker volume prune`

#### TODO:
* use https://pypi.org/project/fhir.resources/ to create resources instead of simply copying data
