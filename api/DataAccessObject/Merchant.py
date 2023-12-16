from flask import abort

class Merchant:

    def __init__(self, driver):
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        """
        self.driver = driver

    def all(self, sort = 'name', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of user.

        Results should be ordered by the `sort` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.
        """
        # Get a list of users from the database
        def getAllMerchants(tx, sort, order, limit, skip):
            cypher = """MATCH (m:Merchant) 
            RETURN m {{ .* }} AS merchant
            ORDER BY m.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("merchant") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllMerchants, sort, order, limit, skip)


    def findByName(self, name):
        """
        Find a Merchant by their name.

        If no Merchant is found, a NotFoundError should be thrown.
        """
         # Find a Merchant by their name
        def getMerchant(tx, name):
            cypher_query = """
                MATCH (m:Merchant {name: $name})
                RETURN m { .* } AS merchant
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, name=name).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("merchant")

        with self.driver.session() as session:
            return session.execute_read(getMerchant, name)

    def addMerchant(self, name, comertial_activity , contact_number , address):
        """
        Add new Merchant with the name of Merchant.
        """
        def createMerchant(tx, name, comertial_activity , contact , address):
            row = tx.run("""
                    MERGE (m:Merchant { name :$name})
                    ON CREATE
                        SET m.created_at = timestamp()
                        SET m.comertial_activity = $comertial_activity 
                        SET m.contact  = $contact
                        SET m.address  = $address
                    RETURN m { .* } AS merchant
                    """,
                     name=name, comertial_activity=comertial_activity, 
                     contact=contact, address=address).single()
            return row.get("merchant")

        with self.driver.session() as session:
            return session.execute_write(createMerchant,  name, comertial_activity , contact_number , address)

    def newCreateMerchant(self, device_id, name, comertial_activity , contact_number , address , date):
        """
        Add new Merchant with the name of Merchant.
        """
        def createMerchant(tx, device_id, name, comertial_activity , contact , address , date):
            row = tx.run("""
                    MATCH (u:User {device_id : $device_id})
                                     
            // EVENT JOURNEY
                    OPTIONAL MATCH (u) -[trig:TRIGGERED]->(pe:Event)
                    WHERE trig.created_at is not null
                    WITh COLLECT(pe) as PE_list, u, trig ORDER BY trig.created_at DESC LIMIT 1

                    CREATE (e:Event)
                    CREATE (u) -[t:TRIGGERED ]->(e)
                        SET t.created_at = $date
                         
                    WITh *, PE_list
                    FOREACH(i in PE_list | CREATE (i)<-[:FOLLOWED] -(e))
                         
            // CREAETE MERCHANT
                    MERGE (m:Merchant { name :$name})
                    ON CREATE
                        SET m.created_at = $date
                        SET m.comertial_activity = $comertial_activity 
                        SET m.contact  = $contact
                        SET m.address  = $address
                    
                    CREATE (u) -[r:CREATED_MERCHANT] -> (m)
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(m)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN m { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                     device_id=device_id, name=name, comertial_activity=comertial_activity, 
                     contact=contact, address=address , date=date).single()
            return row.get("Output")

        with self.driver.session() as session:
            return session.execute_write(createMerchant, device_id, name, comertial_activity , contact_number , address)

    def newContactMerchant(self, device_id, name, comertial_activity , contact_number , address , date ):
        """
        Add new Merchant with the name of Merchant.
        """
        def contactMerchant(tx, device_id, name, comertial_activity , contact , address , date ):
            row = tx.run("""
                    MATCH (u:User {device_id : $device_id})
            
            // EVENT JOURNEY
                    OPTIONAL MATCH (u) -[trig:TRIGGERED]->(pe:Event)
                    WHERE trig.created_at is not null
                    WITh COLLECT(pe) as PE_list, u, trig ORDER BY trig.created_at DESC LIMIT 1

                    CREATE (e:Event)
                    CREATE (u) -[t:TRIGGERED ]->(e)
                        SET t.created_at = date ()
                         
                    WITh *, PE_list
                    FOREACH(i in PE_list | CREATE (i)<-[:FOLLOWED] -(e))
                         
            // CONTANCTED MERCHANT 
                    MERGE (m:Merchant { name :$name})
                    ON CREATE
                        SET m.created_at = date ()
                        SET m.comertial_activity = $comertial_activity 
                        SET m.contact  = $contact
                        SET m.address  = $address
                    
                    CREATE (u) -[r:CONTACTED] -> (m)
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(m)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN m { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                     device_id=device_id, name=name, comertial_activity=comertial_activity, 
                     contact=contact, address=address , date=date).single()
            return row.get("Output")

        with self.driver.session() as session:
            return session.execute_write(contactMerchant, device_id, name, comertial_activity , contact_number , address , date)

    def newViewedMerchantGallery(self, device_id, name, comertial_activity , contact_number , address , date ):
        """
        Add new Merchant with the name of Merchant.
        """
        def viewMerchantGallery(tx, device_id, name, comertial_activity , contact , address , date):
            row = tx.run("""
                    MATCH (u:User {device_id : $device_id})
            
            // EVENT JOURNEY
                    OPTIONAL MATCH (u) -[trig:TRIGGERED]->(pe:Event)
                    WHERE trig.created_at is not null
                    WITh COLLECT(pe) as PE_list, u, trig ORDER BY trig.created_at DESC LIMIT 1

                    CREATE (e:Event)
                    CREATE (u) -[t:TRIGGERED ]->(e)
                        SET t.created_at = $date
                         
                    WITh *, PE_list
                    FOREACH(i in PE_list | CREATE (i)<-[:FOLLOWED] -(e))
                         
            // VIEWED MERCHANT GALLERY
                    MERGE (m:Merchant { name :$name})
                    ON CREATE
                        SET m.created_at = $date
                        SET m.comertial_activity = $comertial_activity 
                        SET m.contact  = $contact
                        SET m.address  = $address
                    
                    CREATE (u) -[r:VIEWED_MERCHANT_GALLERY] -> (m)
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(m)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN m { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                     device_id=device_id, name=name, comertial_activity=comertial_activity, 
                     contact=contact, address=address , date=date).single()
            return row.get("Output")

        with self.driver.session() as session:
            return session.execute_write(viewMerchantGallery, device_id, name, comertial_activity , contact_number , address , date)