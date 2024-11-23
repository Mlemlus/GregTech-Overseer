# GregTech Overseer
### GTOverseer.py
- [ ] Write update work data func
- [ ] GET post to return only overwiev API info = guest info
- [ ] add func to check if power is low and which network is it
- [ ] add func to check only one machine data
- [ ] add the *features* <sub>inc.</sub>

### data_parse.py
- [ ] make the exception actually RETURN usefull error info

### data_processes.py
- [ ] 17. filter differently tha input_eu
- [ ] 31,32. dont include work progress

### database.__init__.py
- [ ] Actually use it

### query.py
- [ ] add update queries

### class_db.py
- [ ] selectMultiple, (updateMultiple?)
- [ ] uncomment exception handling when debugged (never lmao)
- [ ] the init func doesnt do anything with exception, maybe return false or smth (call del xd)

### gto_controller.lua
- [ ] write update function
- [ ] ditch the session_ID, just use oc_address as IDs

# Postgres
### docker-compose.yaml
- [ ] remove pgadmin4 when done
- [ ] add external logging after fixing db-logs privileges

### pg_hba.conf
- [ ] remove pgadmin4 route when done

### postgre_GTOverseer.sql
- [ ] write better default privileges in the "privilege" table

# GTNH server

