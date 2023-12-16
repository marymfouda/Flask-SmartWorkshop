from flask import abort

class Material:

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
        def getAllMaterials(tx, sort, order, limit, skip):
            cypher = """MATCH (m:Material) 
            RETURN m {{ .* }} AS material
            ORDER BY m.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("material") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllMaterials, sort, order, limit, skip)


    def findByName(self, name):
        """
        Find a Material by their name.

        If no Material is found, a NotFoundError should be thrown.
        """
         # Find a Material by their ID
        def getMaterial(tx, name):
            cypher_query = """
                MATCH (m:Material {name: $name})
                RETURN m { .* } AS material
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, name=name).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("material")

        with self.driver.session() as session:
            return session.execute_read(getMaterial, name)

    def addMaterial(self, name):
        """
        Add new Material with the device_name and type of Material.
        """
        def createMaterial(tx, name):
            row = tx.run("""
                    MERGE (m:Material {name : $name})

                    RETURN m { .* } AS material
                    """,
                    name=name).single()
            return row.get("material")

        with self.driver.session() as session:
            return session.execute_write(createMaterial, name)
        
    def newSelection(self, device_id, name , date):
        def newSelectMaterial(tx, device_id, name ):
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

            // SELECTED MATERIAL
                    MERGE (c:Material {name : $name})
                    
                    CREATE (u) -[r:SELECTED_MATERIAL] -> (c)

            // CONNECT EVENT WITH ItS KEYS  
                    SET e.node_keys = [ID(c)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN c { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                    device_id=device_id, name=name).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(newSelectMaterial, device_id, name , date)