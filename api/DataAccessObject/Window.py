
class Window:
    """
    The Class used to handle Window Nodes operations.
    """
    
    def __init__(self, driver):
        self.driver = driver
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        
        Parametew
        ----------
        driver : neo4j.GraphDatabase.driver
            Instance of the neo4j driver.
        """

    def all(self, sort = 'type', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of window.

        Results should be ordered by the `sort` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.

        Parametew
        ----------
        sort : str
            The name of parameter to order with.
        order : str
            Discribe ASC or DES ordering.
        limit : int
            Limit the number of returned usew.
        skip : int
            Skip certain number of rows.

        Returns
        -------
        list
            Contain window informations.

        """

        def allServices(tx, sort, order, limit, skip):
            cypher = """MATCH (w:Window) 
            RETURN w {{ .* }} AS window
            ORDER BY w.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            print(cypher)           #### TODO: DEBUG
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("window") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(allServices, sort, order, limit, skip)


    def addNode(self, type):
        """
        Add new Window Node.

        Parametew
        ----------
        device_id : int or str
            The id used to identify a window.

        type : str
            Type of the window 

        Returns
        -------
        dict
            Contain window informations.
        """

        def createService(tx, type):
            row = tx.run("""
                    MERGE (w:Window { type: $type})
                    ON CREATE
                        SET w.created_at = timestamp()
                    RETURN w { .* } AS window
                    """,
                    type=type).single()
            return row.get("window")

        with self.driver.session() as session:
            return session.execute_write(createService, type)

    
    def newService(self, device_id, Wtype, height, width, piece_count, horizontal, 
                    Gstyle, Gsingle, Gthick,
                    Stype, Ssub_type, Sbar_type, Sbar_value, Ssouas,
                    SHtype, SHshutter_count, SHtrack_count, SHshape,
                    FSHposition, FSHdimension , date):
        """
        Add new Window service associated with the User.

        Parameters
        ----------
        device_id : int or str
            The id used to identify a user.

        Wtype : str
            Type of the window.

        height : int
        width : int
        piece_count : int
        
        horizontal : bool
            wether the window is horizontal or vertical.

        Gstyle : str
            style of glass.
        Gsingle : bool
            single or double
        Gthick : float
            glass thickness
        
        Stype : str
            sector main type
        Ssub_type : str
            sector sub type
        Sbar_type : str
            Sector bar type
        Sbar_value : float
            measurements of the bar
        Ssouas : string
            Sector souas

        SHtype : str
            Shutter type
        SHshutter_count: int
            Shutter count
        SHtrack_count : int
            Shutter track count
        SHshape : str
            Shutter shape

        FSHposition : str
            Fixed Shutter position
        FSHdimension : float
            Fixed Shutter dimensions
        Returns
        -------
        dict
            Contain window informations.

        """

        Ssector_key = Stype + '/' + Ssub_type
        def createService(tx, device_id, Wtype, height, width, piece_count, 
                          horizontal, Gstyle, Gsingle, Gthick,
                          Stype, Ssub_type, Sbar_type, Ssector_key, Sbar_value, Ssouas,
                          SHtype, SHshutter_count, SHtrack_count, SHshape,
                          FSHposition, FSHdimension, date 
                          ):

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
                         
            // WINDOW CRERATION
                    MERGE (w:Window { type: $Wtype})
                    ON CREATE 
                        SET w.created_at = $date
                    
                    CREATE (u) -[cs:CREATED_SERVICE] -> (w)
                        SET cs.height = $height
                        SET cs.width = $width
                        SET cs.piece_count = $piece_count
                        SET cs.horizontal = $horizontal

                    MERGE (g:Glass { style : $Gstyle})
                    CREATE (w) -[hg:HAS_GLASS] -> (g)
                        SET hg.single = $Gsingle
                        SET hg.thickness = $Gthick

                    MERGE (s:Sector { key : $Ssector_key })
                        ON CREATE
                            SET s.type = $Stype
                            SET s.sub_type = $Ssub_type
                         
                    CREATE (w) -[hs:HAS_Sector] -> (s)
                        SET hs.bar_type = $Sbar_type
                        SET hs.bar_value = $Sbar_value
                        SET hs.souas = $Ssouas

                    MERGE (sh:Shutter { type : $SHtype })
                        ON CREATE
                            SET sh.shutter_count = $SHshutter_count
                            SET sh.track_count = $SHtrack_count 
                         
                    CREATE (w) -[hsh:HAS_SHUTTER] -> (sh)
                        SET hsh.shutter_shape = $SHshape

                    MERGE (fsh:FixedShutter { position : $FSHposition})
                    CREATE (sh) -[hfsh:HAS_FIXED] -> (fsh)
                        SET hfsh.dimension = $FSHdimension

            // CONNECT EVENT WITH ItS KEYS      
                    SET e.node_keys = [ID(w), ID(g), ID(s), ID(sh), ID(fsh)] 
                    SET e.rel_keys = [ID(cs), ID(hg), ID(hs), ID(hsh), ID(hfsh)]
                         
                    RETURN cs {  User : u.device_id, WindowType : w.type , .* ,
                        Relationship : type(cs), EventTriggeredAt : t.created_at}  AS Output 
                    """,
                    device_id=device_id, Wtype=Wtype,
                    height=height, width=width, piece_count=piece_count,
                    horizontal=horizontal, Gstyle=Gstyle, Gsingle=Gsingle, Gthick=Gthick,
                    Stype=Stype, Ssub_type=Ssub_type, Ssector_key=Ssector_key, 
                        Sbar_type=Sbar_type, Sbar_value=Sbar_value, Ssouas=Ssouas,
                    SHtype=SHtype, SHshutter_count=SHshutter_count, SHtrack_count=SHtrack_count, SHshape=SHshape,
                    FSHposition=FSHposition, FSHdimension=FSHdimension , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')


        with self.driver.session() as session:
            return session.execute_write(createService, device_id, Wtype,
                            height, width, piece_count,
                            horizontal, Gstyle, Gsingle, Gthick,
                            Stype, Ssub_type, Ssector_key, Sbar_type, Sbar_value, Ssouas,
                            SHtype, SHshutter_count, SHtrack_count, SHshape,
                            FSHposition, FSHdimension , date)