from flask import abort

class RollingShutter:
    """
    The Class used to handle RollingShutter Nodes operations.
    """
    
    def __init__(self, driver):
        self.driver = driver
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        
        Parameters
        ----------
        driver : neo4j.GraphDatabase.driver
            Instance of the neo4j driver.
        """

    def all(self, sort = 'type', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of rolling.

        Results should be ordered by the `sort` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.

        Parameters
        ----------
        sort : str
            The name of parameter to order with.
        order : str
            Discribe ASC or DES ordering.
        limit : int
            Limit the number of returned users.
        skip : int
            Skip certain number of rows.

        Returns
        -------
        list
            Contain rolling informations.

        """

        def allServices(tx, sort, order, limit, skip):
            cypher = """MATCH (rs:RollingShutter) 
            RETURN rs {{ .* }} AS rolling
            ORDER BY rs.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            print(cypher)           #### TODO: DEBUG
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("rolling") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(allServices, sort, order, limit, skip)


    def addNode(self, type):
        """
        Add new rolling with the device_id and type of rolling.

        Parameters
        ----------
        device_id : int or str
            The id used to identify a rolling.

        type : str
            Type of the rolling either Normal, Carpenter or Alumetal technician

        Returns
        -------
        dict
            Contain rolling informations.
        """

        def createService(tx, type):
            row = tx.run("""
                    MERGE (rs:RollingShutter { type: $type})
                    ON CREATE
                        SET rs.created_at = timestamp()
                    RETURN rs { .* } AS rolling
                    """,
                    type=type).single()
            return row.get("rolling")

        with self.driver.session() as session:
            return session.execute_write(createService, type)

    
    def newService(self, device_id, type, height, width, piece_count , date):
        """
        Add new Rolling service associated with the User

        Parameters
        ----------
        device_id : int or str
            The id used to identify a user.

        type : str
            Type of the rolling either Normal, Carpenter or Alumetal technician

        height : int
        width : int
        piece_count : int

        Returns
        -------
        dict
            Contain rolling informations.

        """

        def createService(tx, device_id, type, height, width, piece_count , date ):
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
                         
            // ROLLING SHUTTER CREATION
                    MERGE (rs:RollingShutter { type: $type})
                    ON CREATE 
                        SET rs.created_at = $date
                    
                    CREATE (u) -[r:CREATED_SERVICE] -> (rs)
                        SET r.height = $height
                        SET r.width = $width
                        SET r.piece_count = $piece_count
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(rs)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN r {  User : u.device_id, RollingShutterType : rs.type , .* ,
                        Relationship : type(r), EventTriggeredAt : t.created_at}  AS Output 
                    """,
                    device_id=device_id, type=type,
                      height=height, width=width, piece_count=piece_count , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(createService, device_id, type,
                                            height, width, piece_count , date)