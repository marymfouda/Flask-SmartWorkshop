
class PlisseWire:
    """
    The Class used to handle PlisseWire Nodes operations.
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

    def all(self, sort = 'sector_type', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of plisse.

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
            Contain plisse informations.

        """

        def allServices(tx, sort, order, limit, skip):
            cypher = """MATCH (pw:PlisseWire) 
            RETURN pw {{ .* }} AS plisse
            ORDER BY pw.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            print(cypher)           #### TODO: DEBUG
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("plisse") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(allServices, sort, order, limit, skip)


    def addNode(self, type):
        """
        Add new plisse with the sector type.

        Parameters
        ----------
        type : str
            Type of the plisse's sector

        Returns
        -------
        dict
            Contain plisse informations.
        """

        def createService(tx, type):
            row = tx.run("""
                    MERGE (pw:PlisseWire { sector_type: $type})
                    ON CREATE
                        SET pw.created_at = timestamp()
                    RETURN pw { .* } AS plisse
                    """,
                    type=type).single()
            return row.get("plisse")

        with self.driver.session() as session:
            return session.execute_write(createService, type)

    
    def newService(self, device_id, type, height, width, piece_count, two_shutter, open_horizontal, date):
        """
        Add new Plisse Wire service associated with the User

        Parameters
        ----------
        device_id : int or str
            The id used to identify a user.

        type : str
            Type of the plisse's sector.

        height : int
        width : int
        piece_count : int

        two_shutter : bool
            whether it has 2 shutter or not.

        open_horizontal : bool
            wether it opens horizontally or not.

        Returns
        -------
        dict
            Contain plisse informations.

        """

        def createService(tx, device_id, type, height, width, piece_count, two_shutter, open_horizontal,date):
            row = tx.run("""
                    MATCH (u:User {device_id : $device_id})
            // EVENT JOURNEY
                    OPTIONAL MATCH (u) -[trig:TRIGGERED]->(pe:Event)
                    WHERE trig.created_at is not null
                    WITh COLLECT(pe) as PE_list, u, trig ORDER BY trig.created_at DESC LIMIT 1

                    CREATE (e:Event)
                    CREATE (u) -[t:TRIGGERED ]->(e)
                        SET t.created_at = datetime($date)
                         
                    WITh *, PE_list
                    FOREACH(i in PE_list | CREATE (i)<-[:FOLLOWED] -(e))

            // PLISSE WIRE CREATION
                    MERGE (pw:PlisseWire { sector_type: $type})
                    ON CREATE 
                        SET pw.created_at = datetime($date)
                    
                    CREATE (u) -[r:CREATED_SERVICE] -> (pw)
                        SET r.height = $height
                        SET r.width = $width
                        SET r.piece_count = $piece_count
                        SET r.two_shutter = $two_shutter
                        SET r.open_horizontal = $open_horizontal
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(pw)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN r {  User : u.device_id, PlisseWireType : pw.type , .* ,
                        Relationship : type(r), EventTriggeredAt : tostring(t.created_at)}  AS Output 
                    """,
                    device_id=device_id, type=type,
                      height=height, width=width, piece_count=piece_count,
                      two_shutter=two_shutter, open_horizontal=open_horizontal , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(createService, device_id, type, height, width, 
                                            piece_count, two_shutter, open_horizontal , date)