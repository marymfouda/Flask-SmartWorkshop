
class FoldingSecurit:
    """
    The Class used to handle FoldingSecurit Nodes operations.
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
    
    def newService(self, device_id, height, width, piece_count, sink , date ):
        """
        Add new Folding Securit service associated with the User.

        Parameters
        ----------
        device_id : int or str
            The id used to identify the User.
        
        height : int
        width : int
        piece_count : int

        sink : bool
            whether the service use sink path or not.

        Returns
        -------
        dict
            Contain Folding Securit informations.

        """

        def createService(tx, device_id, height, width, piece_count, sink , date):
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

            // FOLDING SECURIT CERATION
                    MERGE (fs:FoldingSecurit)
                    ON CREATE 
                        SET fs.created_at = $date
                    
                    CREATE (u) -[r:CREATED_SERVICE] -> (fs)
                        SET r.height = $height
                        SET r.width = $width
                        SET r.piece_count = $piece_count
                        SET r.sink_path = $sink
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(fs)]
                    SET e.rel_keys = [ID(r)]

                         
                    RETURN r {  User : u.device_id, FoldingSecurit : "base" , .* ,
                        Relationship : type(r), EventTriggeredAt : t.created_at}  AS Output 
                    """,
                    device_id=device_id, height=height, width=width, 
                    piece_count=piece_count, sink=sink , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(createService, device_id,
                                              height, width, piece_count, sink , date)