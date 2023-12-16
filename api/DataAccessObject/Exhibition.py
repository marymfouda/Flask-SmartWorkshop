from flask import abort
from neo4j.exceptions import ConstraintError


class Exhibition:

    def __init__(self, driver):
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        """
        self.driver = driver

    def all(self, sort = 'name', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of Exhibition.

        Results should be ordered by the `sort` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.
        """
        # Get a list of event from the database
        def getAllExhibition(tx, sort, order, limit, skip):
            cypher = """MATCH (ex:Exhibition) 
            RETURN ex {{ .* }} AS Exhibition
            ORDER BY ex.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("Exhibition") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllExhibition, sort, order, limit, skip)

    def findByName(self, name):
        """
        Find a Exhibition by their name.

        If no Exhibition is found, a NotFoundError should be thrown.
        """
         # Find a Exhibition by their ID
        def getExhibition(tx, name ):
            row = tx.run("""
                    MATCH (ex:Exhibition {name: $name})
                    RETURN ex { .* } AS Exhibition
                    """, 
                    name=name).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("Exhibition")

        with self.driver.session() as session:
            return session.execute_read(getExhibition, name)

        
    def addExhibition(self, name, description, 
                          contact, address, social, rate , date ):
        def create_Exhibition(tx, name, description, 
                          contact, address, social, rate ):
            row = tx.run("""
                    MERGE (ex:Exhibition {name : $name})
                    ON CREATE
                        SET ex.created_at = timestamp()
                        SET ex.description = $description
                        SET ex.address = $address
                        SET ex.contact = $contact
                        SET ex.social = $social
                        SET ex.rate = $rate
                         
                    RETURN ex { .* } AS Exhibition
                    """,
                    name=name, description=description, contact=contact, 
                    address=address, social=social, rate=rate , date=date) .single()
            return row.get("Exhibition")

        with self.driver.session() as session:
            return session.execute_write(create_Exhibition, name, description, 
                          contact, address, social, rate , date)

    def NewViewedGallery(self,device_id, name, description=None, contact=None, 
                         address=None, social=None, rate=None , date=None):
        """
        Add new Viewed Gallery Relationship.

        Parameters
        ----------
        device_id :  str
            The id used to identify the User.
        
        Exhibition_id :int
        
        Returns
        -------
        dict
            Contain Node informations.


        Raises
        ------
        ConstraintError
            If the attribute's value is already in the graph database,
            abort with 422 status code.
        """

        def ViewedGallery(tx,device_id, name, description, 
                          contact, address, social, rate , date ):    
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

            // VIEWED GALLERY 
                    MERGE (ex: Exhibition { name : $name})
                    ON CREATE                    
                        SET ex.created_at = $date
                        SET ex.description = $description
                        SET ex.address = $address
                        SET ex.contact = $contact
                        SET ex.social = $social
                        SET ex.rate = $rate
                         
                    CREATE (u) -[r:VIEWED_GALLERY] -> (ex)             
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [ID(ex)]
                    SET e.rel_keys = [ID(r)]

                    RETURN ex { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                    device_id=device_id, name=name, description=description, 
                    contact=contact, address=address, social=social, rate=rate , date=date ).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        try:
            with self.driver.session() as session:
                return session.execute_write(ViewedGallery,device_id, name, 
                                             description, contact, address, social, rate , date)
            
        except ConstraintError as err:
            abort(422, err.message)