
class Kitchen:
    """
    The Class used to handle Kitchen Nodes operations.
    """
    
    def __init__(self, driver):
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        
        Parameters
        ----------
        driver : neo4j.GraphDatabase.driver
            Instance of the neo4j driver.
        """
        self.driver = driver

    def all(self, sort = 'type', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of Kitchen.

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
            Contain Kitchen informations.

        """

        def allServices(tx, sort, order, limit, skip):
            cypher = """MATCH (k:Kitchen) 
            RETURN k {{ .* }} AS Kitchen
            ORDER BY k.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            print(cypher)           #### TODO: DEBUG
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("Kitchen") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(allServices, sort, order, limit, skip)


    def addNode(self, type):
        """
        Add new Kitchen with its type.

        Parameters
        ----------
        type : str
            Type of the Kitchen either Tipper or Sliding

        Returns
        -------
        dict
            Contain Kitchen informations.

        Raises
        ------
        ConstraintError
            If the attribute's value is already in the graph database,
            abort with 422 status code.
        """

        def createServiceNode(tx, type):
            row = tx.run("""
                    MERGE (k:Kitchen { type: $type})
                    ON CREATE
                        SET k.created_at = timestamp()
                    RETURN k { .* } AS Kitchen
                    """,
                    type=type).single()
            return row.get("Kitchen")
        
        with self.driver.session() as session:
            return session.execute_write(createServiceNode, type)
    
    def newService(self, device_id, type, height, width, depth,
                  shutter_color_type, shelves_number, alumetal_unit_type,
                  assembly, unit_assembly, drawer_assembly, drosal_installation,
                  kitchen_sector, shelf_sector, shutter_sector, depth_sector,
                  kitchen_unit_position, kitchen_unit_name , date ):
        """
        Add new Kitchen with the device_id and type of Kitchen.

        Parameters
        ----------
        device_id : int or str
            The id used to identify a Kitchen.

        type : str
            Type of the Kitchen either Normal, Carpenter or Alumetal technician

        Returns
        -------
        dict
            Contain Kitchen informations.

        Raises
        ------
        ConstraintError
            If the attribute's value is already in the graph database,
            abort with 422 status code.
        """

        def createService(tx, device_id, type, height, width, depth,
                  shutter_color_type, shelves_number, alumetal_unit_type,
                  assembly, unit_assembly, drawer_assembly, drosal_installation,
                  kitchen_sector, shelf_sector, shutter_sector, depth_sector,
                  kitchen_unit_position, kitchen_unit_name , date):
            row = tx.run("""
                    MATCH (u:User {device_id : $device_id})
            
            // EVENT JOURNEY 
                    OPTIONAL MATCH (u) -[trig:TRIGGERED]->(previous_event:Event)
                    WHERE trig.created_at is not null
                    WITh COLLECT(previous_event) as PREVIOUS_EVENT_list, u, trig ORDER BY trig.created_at DESC LIMIT 1

                    CREATE (e:Event)
                    CREATE (u) -[t:TRIGGERED ]->(e)
                        SET t.created_at = $date
                         
                    WITh *, PREVIOUS_EVENT_list
                    FOREACH(i in PREVIOUS_EVENT_list | CREATE (i)<-[:FOLLOWED] -(e))
                    
            // KITCHEN CREATION
                    MERGE (k:Kitchen { type: $type})
                    ON CREATE 
                        SET k.created_at = $date
                         
                    MERGE (ku:KitchenUnit {position : $kitchen_unit_position})
                         
                    CREATE (k) -[hu:HAS_UNIT]->(ku)
                        SET hu.unit_name = $kitchen_unit_name
                    
                // Kitchen Sector
                    MERGE (kitchen_Sector:Sector { key : "kitchen/" + $kitchen_sector})
                        ON CREATE
                            SET kitchen_Sector.type = "kitchen"
                            SET kitchen_Sector.sub_type = $kitchen_sector
                         
                    CREATE (k) -[hs_kitchen:HAS_SECTOR]->(kitchen_Sector)
                    
                // Shelf Sector
                    MERGE (shelf_Sector:Sector { key : "shelf/" + $shelf_sector})
                        ON CREATE
                            SET shelf_Sector.type = "shelf"
                            SET shelf_Sector.sub_type = $shelf_sector
                         
                    CREATE (k) -[hs_shelf:HAS_SECTOR]->(shelf_Sector)
                    
                // Shutter Sector
                    MERGE (shutter_Sector:Sector { key : "shutter/" + $shutter_sector})
                        ON CREATE
                            SET shutter_Sector.type = "shutter"
                            SET shutter_Sector.sub_type = $shutter_sector
                         
                    CREATE (k) -[hs_shutter:HAS_SECTOR]->(shutter_Sector)
                    
                // Depth Sector
                    MERGE (depth_Sector:Sector { key : "depth/" + $depth_sector})
                        ON CREATE
                            SET depth_Sector.type = "depth"
                            SET depth_Sector.sub_type = $depth_sector
                         
                    CREATE (k) -[hs_depth:HAS_SECTOR]->(depth_Sector)

                // CREATED SERVICE
                    CREATE (u) -[r:CREATED_SERVICE] -> (k)
                        SET r.id = randomuuid()
                         
                        SET r.height = $height
                        SET r.width = $width
                        SET r.depth = $depth
                         
                        SET r.shutter_color_type = $shutter_color_type
                        SET r.shelves_number = $shelves_number
                        SET r.alumetal_unit_type = $alumetal_unit_type
                        SET r.assembly = $assembly
                        SET r.unit_assembly = $unit_assembly
                        SET r.drawer_assembly = $drawer_assembly
                        SET r.drosal_installation = $drosal_installation

                        SET r.kitchen_unit_position = $kitchen_unit_position
                        SET r.kitchen_unit_name = $kitchen_unit_name
                         
                // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(k), ID(ku), ID(kitchen_Sector), 
                            ID(shelf_Sector), ID(shutter_Sector), ID(depth_Sector)]
                    SET e.rel_keys = [ID(r), ID(hu), ID(hs_kitchen), 
                            ID(hs_shelf), ID(hs_shutter), ID(hs_depth)]
                         
                    RETURN r {User : u.device_id, KitchenType : k.type, .* , 
                        UnitName : hu.unit_name, UnitPosition : ku.position,
                        Sectors : {
                            kitchen : kitchen_Sector.sub_type,
                            shutter : shutter_Sector.sub_type,
                            shelf : shelf_Sector.sub_type,
                            depth : depth_Sector.sub_type
                        },
                        Relationship : type(r), EventTriggeredAt : t.created_at}  AS Output
                    """,
                    device_id=device_id, type=type,
                    height=height, width=width, depth=depth,
                    shutter_color_type=shutter_color_type, shelves_number=shelves_number, alumetal_unit_type=alumetal_unit_type,
                    assembly=assembly, unit_assembly=unit_assembly, drawer_assembly=drawer_assembly, drosal_installation=drosal_installation,
                    kitchen_sector=kitchen_sector, shelf_sector=shelf_sector, shutter_sector=shutter_sector, depth_sector=depth_sector,
                    kitchen_unit_position=kitchen_unit_position, kitchen_unit_name=kitchen_unit_name , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(createService, 
                device_id, type, height, width, depth,
                shutter_color_type, shelves_number, alumetal_unit_type,
                assembly, unit_assembly, drawer_assembly, drosal_installation,
                kitchen_sector, shelf_sector, shutter_sector, depth_sector,
                kitchen_unit_position, kitchen_unit_name , date)