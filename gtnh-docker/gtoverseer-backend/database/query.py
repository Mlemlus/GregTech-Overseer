from database.class_db import db # idk if needed

################## CREATE ##################
def insMachine(db, kwargs):
    db.insert("""
        INSERT INTO gtoverseer.machine ("oc_computer_ID", "tier_ID", "owner_ID", oc_address, name, amp) 
        VALUES 
            (%(oc_computer_ID)s, 
            %(tier_ID)s, 
            (SELECT "ID" FROM gtoverseer.user WHERE username = %(owner_name)s), 
            %(oc_address)s, 
            %(name)s, 
            %(amp)s)
        ON CONFLICT ("oc_address") DO UPDATE
        SET 
            "oc_computer_ID" = EXCLUDED."oc_computer_ID", 
            "tier_ID" = EXCLUDED."tier_ID", 
            "owner_ID" = EXCLUDED."owner_ID",
            "amp" = EXCLUDED."amp"
    """, kwargs)
    return selComputer(db, kwargs["oc_address"])

def insCoord(db, kwargs):
    db.insert("""
        INSERT INTO gtoverseer.coord ("machine_ID", "x", "y", "z")
        VALUES 
            (%(machine_ID)s, 
            %(coords_x)s, 
            %(coords_y)s, 
            %(coords_z)s)
        ON CONFLICT ("machine_ID") DO UPDATE
        SET 
            "x" = EXCLUDED."x", 
            "y" = EXCLUDED."y",
            "z" = EXCLUDED."z"
    """, kwargs)

def insWork(db, kwargs):
    db.insert("""
        INSERT INTO gtoverseer.work ("machine_ID", work_progress, work_progress_max)
        VALUES 
            (%(machine_ID)s, 
            %(work_progress)s, 
            %(work_progress_max)s)
        ON CONFLICT ("machine_ID") DO UPDATE
        SET 
            "work_progress" = EXCLUDED."work_progress", 
            "work_progress_max" = EXCLUDED."work_progress_max"
    """, kwargs)

def insComputer(db, kwargs):
    # insert computah, if exist do nothing
    if (oc_comp_id := selComputer(db, kwargs["computer_oc_address"])):
        return oc_comp_id     
    else:
        return db.insert('INSERT INTO gtoverseer.oc_computer (oc_address) VALUES (%(computer_oc_address)s) RETURNING "ID"', kwargs)
    
def insPowerSource(db, kwargs):
    db.insert("""
        INSERT INTO gtoverseer.power_source ("machine_ID", "output_amp", "current_capacity", "max_capacity")
        VALUES 
            (%(machine_ID)s, 
            %(output_amp)s, 
            %(eu_capacity_current)s,    
            %(eu_capacity)s)
        ON CONFLICT ("machine_ID") DO UPDATE
        SET 
            "output_amp" = EXCLUDED."output_amp", 
            "current_capacity" = EXCLUDED."current_capacity",
            "max_capacity" = EXCLUDED."max_capacity"
    """, kwargs)

def insUser(db, kwargs):
    return db.insert("""
        INSERT INTO gtoverseer.user ("username", "email", "password_hash")
        VALUES (
            %(username)s,
            %(email)s, 
            gtoverseer.crypt(%(password)s, gtoverseer.gen_salt('bf'))
        )
        ON CONFLICT ("username") DO UPDATE
        SET
            "username" = EXCLUDED."username",
            "email" = EXCLUDED."email",
            "password_hash" = EXCLUDED."password_hash"
        """, kwargs)

# Cable
def insCable(db, kwargs):
    return db.insert("""
        INSERT INTO gtoverseer.cable ("name", "density", "tier_ID", "max_amp", "loss")
        VALUES (
            %(name)s,
            %(density)s,
            (
                SELECT "ID"
                FROM gtoverseer.tier
                WHERE "name" = %(tier_name)s
            ),
            %(max_amp)s,
            %(loss)s
        )
        ON CONFLICT ("name") DO NOTHING
        """, kwargs)

# Power Network
def insPowerNetwork(db, kwargs):
    return db.insert("""
        INSERT INTO gtoverseer."power_network" ("name", "cable_ID", "owner_ID", "avg_amp", "avg_eu")
        VALUES (
            %(name)s,
            (
                SELECT "ID"
                FROM gtoverseer.cable
                WHERE "name" = %(cable_name)s
            ),
            (
                SELECT "ID"
                FROM gtoverseer.user
                WHERE "username" = %(username)s
            ),
            0,
            0
        )
        ON CONFLICT ("name") DO NOTHING
        """, kwargs)

################## READ ##################
# OC Computer
def selComputer(db, oc_address):
    return db.selectSingle('SELECT "ID" FROM gtoverseer.oc_computer WHERE oc_address = %s', oc_address)

# User
def selUserUsername(db, username):
    return db.selectSingle('SELECT ("ID") FROM gtoverseer.user WHERE username = %s', username)

def selUserEmailPassword(db, kwargs):
    return db.selectMultiple("""
        SELECT "username" FROM gtoverseer.user 
        WHERE 
            email = %(email)s
            AND
            password_hash = gtoverseer.crypt(%(password)s, password_hash)
        """, kwargs)

def selAllUsers(db):
    return db.select(
        """
        SELECT "username", "email"
        FROM gtoverseer.user
        ORDER BY "username"
        """)

def searchUsers(db, kwargs):
    return db.selectMultiple(
        """
        SELECT "ID", "username", "email"
        FROM gtoverseer.user
        WHERE username = %(search)s OR email = %(search)s
        """, kwargs)

# Machine
def selMachine(db, oc_address):
    return db.selectSingle('SELECT "ID" FROM gtoverseer.machine WHERE oc_address = %s', oc_address)

def machineReport(db):
    return db.select(
        """
        SELECT * 
        FROM gtoverseer.machine_report
        """)

# Power network
def selAllNetowrksNames(db):
    return db.select(
        """
        SELECT "name"
        FROM gtoverseer.power_network
        """)

def selAllPowerNetworks(db):
    return db.select(
        """
        SELECT pn."name", c."name", pn."created_at", u."username"
        FROM gtoverseer."power_network" pn
        LEFT JOIN gtoverseer.cable c ON pn."cable_ID" = c."ID"
        LEFT JOIN gtoverseer.user u ON pn."owner_ID" = u."ID"
        ORDER BY pn."name"
        """)

# Cable
def selAllCables(db):
    return db.select(
        """
        SELECT c."name", t."name", c."density", c."max_amp", c."loss"
        FROM gtoverseer.cable c
        LEFT JOIN gtoverseer.tier t ON c."tier_ID" = t."ID"
        ORDER BY c."name"
        """)

def selAllCablesNames(db):
    return db.select(
        """
        SELECT "name"
        FROM gtoverseer.cable
        ORDER BY "name"
        """)

# Tier
def selTier(db, voltage):
    return db.selectSingle('SELECT ("ID") FROM gtoverseer.tier WHERE eu = %s', voltage)

def selTiers(db):
    return db.select('SELECT "ID", "name", "eu" FROM gtoverseer.tier')

def selAllTierNames(db):
    return db.select(
        """
        SELECT "name"
        FROM gtoverseer.tier
        """)

################## UPDATE ##################
def updWork(db, kwargs):
    db.insert("""
        INSERT INTO gtoverseer.work ("machine_ID", work_progress, work_progress_max)
        SELECT
            m."ID" AS "machine_ID",
            %(work_progress)s AS work_progress,
            %(work_progress_max)s AS work_progress_max
        FROM gtoverseer.machine m
        WHERE m.oc_address = %(oc_address)s
        ON CONFLICT ("machine_ID") DO UPDATE
        SET
            "work_progress" = EXCLUDED."work_progress", 
            "work_progress_max" = EXCLUDED."work_progress_max",
            "last_worked_at" = CURRENT_TIMESTAMP
    """, kwargs)

# User
def updateUser(db, kwargs): # sometimes, my genius scares me
    return db.update(
        """
        UPDATE gtoverseer.user
        SET
            "username" = %(username)s,
            "email" = %(email)s
        WHERE "username" = %(old_username)s
        AND(
            %(username)s = %(old_username)s 
            OR
            NOT EXISTS(
                SELECT 1 
                FROM gtoverseer.user
                WHERE "username" = %(username)s
            )
        )
        """, kwargs)

# Machine
def updateMachine(db, kwargs):
    return db.update(
        """
        UPDATE gtoverseer.machine
        SET
            "custom_name" = %(name)s,
            "note" = %(note)s,
            "power_network_ID" = (
                SELECT "ID"
                FROM gtoverseer."power_network"
                WHERE "name" = %(pnname)s
            )
        WHERE "ID" = %(ID)s;
        UPDATE gtoverseer."coord"
        SET
            "is_chunk_loaded" = %(chunkloaded)s
        WHERE "machine_ID" = %(ID)s
        """, kwargs)

# Cable
def updateCable(db, kwargs):
    return db.update(
        """
        UPDATE gtoverseer.cable
        SET
            "name" = %(name)s,
            "density" = %(density)s,
            "tier_ID" = (
                SELECT "ID"
                FROM gtoverseer.tier
                WHERE "name" = %(tier_name)s
            ),
            "max_amp" = %(max_amp)s,
            "loss" = %(loss)s
        WHERE "name" = %(old_name)s
        """, kwargs)

# Power Network
def updatePowerNetwork(db, kwargs):
    return db.update(
        """
        UPDATE gtoverseer."power_network"
        SET
            "name" = %(name)s,
            "cable_ID" =(
                SELECT "ID"
                FROM gtoverseer.cable
                WHERE "name" = %(cable_name)s
            )
        WHERE "name" = %(old_name)s
        """, kwargs)

################## DELETE ##################
def deleteUser(db, kwargs):
    return db.delete(
        """
        DELETE FROM gtoverseer.user
        WHERE "username" = %(username)s
        """, kwargs)

def deleteCable(db, kwargs):
    return db.delete(
    """
    DELETE FROM gtoverseer.cable
    WHERE "name" = %(name)s
    """, kwargs)

def deletePowerNetwork(db, kwargs):
    return db.delete(
    """
    DELETE FROM gtoverseer."power_network"
    WHERE "name" = %(name)s
    """, kwargs)