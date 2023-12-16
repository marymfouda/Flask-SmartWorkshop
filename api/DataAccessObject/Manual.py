from flask import abort

class Manual:

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
        # Get a list of manual from the database
        def getAllManual(tx, sort, order, limit, skip):
            cypher = """MATCH (m:Manual) 
            RETURN m {{ .* }} AS manual
            ORDER BY m.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("manual") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllManual, sort, order, limit, skip)


    def findByName(self, name):
        """
        Find a manual by their name.

        If no manual is found, a NotFoundError should be thrown.
        """
         # Find a Manual by their name
        def getManual(tx, name):
            cypher_query = """
                MATCH (m:Manual{name: $name})
                RETURN m { .* } AS manual
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, name=name).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("manual")

        with self.driver.session() as session:
            return session.execute_read(getManual, name)

    def addManual(self, name, type):
        """
        Add new Manual with the device_id and type of manual.
        """
        def createManual(tx, name, type):
            row = tx.run("""
                    MERGE (m:Manual {name : $name, type: $type})

                    RETURN m { .* } AS manual
                    """,
                    name=name, type=type).single()
            return row.get("manual")

        with self.driver.session() as session:
            return session.execute_write(createManual, name, type)
        
    def newVisit(self, device_id, name, type , date):
        def visitedManual(tx, device_id, name, type , date):
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
                         
            // VISITED MANUAL
                    MERGE (c:Manual {name : $name})
                    ON CREATE 
                        SET c.type = $type
                    
                    CREATE (u) -[r:VISITED_MANUAL] -> (c)
            
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(c)]
                    SET e.rel_keys = [ID(r)]

                         
                    RETURN c { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                    device_id=device_id, name=name, type=type , date=date ).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(visitedManual,device_id, name , type , date)
