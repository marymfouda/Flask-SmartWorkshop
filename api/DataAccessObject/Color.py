from flask import abort
from neo4j.exceptions import ConstraintError

class Color:

    def __init__(self, driver):
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        """
        self.driver = driver

    def all(self, code = 'code', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a list of color.

        Results should be ordered by the `code` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.
        """
        # Get a list of users from the database
        def getAllColor(tx, sort, order, limit, skip):
            cypher = """MATCH (c:Color) 
            RETURN c {{ .* }} AS color
            ORDER BY c.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order,limit , skip )

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, code = code , order = order , limit = limit , skip = skip )

            return [ row.get("color") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllColor, code , order , limit , skip)


    def findByCode(self, code):
        """
        Find a color by their code.

        If no color is found, a NotFoundError should be thrown.
        """
         # Find a color by code
        def getColor(tx, code):
            cypher_query = """
                MATCH (c:Color {code: $code})
                RETURN c { .* } AS color
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, code = code).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("color")

        with self.driver.session() as session:
            return session.execute_read(getColor, code)

    def addColor(self, code, type):
        """
        Add new color with the code and type of color.
        """
        def createColor(tx, code, type):
            row = tx.run("""
                    MERGE (c:Color {code :$code, type: $type})

                    RETURN c { .* } AS color
                    """,
                    code = code , type=type).single()
            return row.get("color")

        with self.driver.session() as session:
            return session.execute_write(createColor, code, type)
        

    def NewSelectedColor(self,device_id, code , type , date):
        """
        Add new color node .

        Parameters
        ----------
        device_id :  str
            The id used to identify the User.
        
        code : str
        type : str
        
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

        def SelectedColor(tx,device_id ,code , type , date):    
            row = tx.run("""
                    MATCH (u:User {device_id : $device_id})
            
            // EVENT JOURNEY
                    OPTIONAL MATCH (u) -[trig:TRIGGERED]->(pe:Event)
                    WHERE trig.created_at is not null
                    WITh COLLECT(pe) as PE_list, u, trig ORDER BY trig.created_at DESC LIMIT 1

                    CREATE (e:Event)
                    CREATE (u) -[t:TRIGGERED ]->(e)
                        SET t.created_at = $date
                        SET t.id =randomuuid()
                         
                    WITh *, PE_list
                    FOREACH(i in PE_list | CREATE (i)<-[:FOLLOWED] -(e))
                         
            // COLOR SELECTION
                    MERGE (c:Color {code : $code})
                    ON CREATE 
                        SET c.type = $type
                        SET c.id =randomuuid()
                    
                    CREATE (u) -[r:SELECTED_COLOR] -> (c)
                         
            // CONNECT EVENT WITH ItS KEYS
                    SET e.node_keys = [c.id]
                    SET e.rel_keys =  [r.id]

                         
                    RETURN c { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                    device_id=device_id,code = code, type = type , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        try:
            with self.driver.session() as session:
                return session.execute_write(SelectedColor,device_id, code , type , date)
            
        except ConstraintError as err:
            abort(422, err.message)