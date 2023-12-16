from flask import abort

class Image:

    def __init__(self, driver):
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        """
        self.driver = driver

    def all(self, sort = 'url', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of user.

        Results should be ordered by the `sort` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.
        """
        # Get a list of users from the database
        def getAllImages(tx, sort, order, limit, skip):
            cypher = """MATCH (i:Image) 
            RETURN i {{ .* }} AS image
            ORDER BY i.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("image") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllImages, sort, order, limit, skip)


    def findByURL(self, url):
        """
        Find a image by their url.

        If no image is found, a NotFoundError should be thrown.
        """
         # Find a user by their ID
        def get_image(tx, device_id):
            cypher_query = """
                MATCH (i:Image {url: $url})
                RETURN i { .* } AS image
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, url=url).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("image")

        with self.driver.session() as session:
            return session.execute_read(get_image, url)

    def addImage(self, url):
        """
        Add new user with the device_id and type of image.
        """
        def createImage(tx, url):
            row = tx.run("""
                    MERGE (i:Image {url : $url})
                    ON CREATE
                        SET i.created_at = $date
                    RETURN i { .* } AS image
                    """,
                    url=url).single()
            return row.get("image")

        with self.driver.session() as session:
            return session.execute_write(createImage, url)
        
    def newClick(self, device_id, url , date):
        def userClick(tx, device_id, url):
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

            // IMAGE CLICKED    
                    MERGE (c:Image {url : $url})
                    
                    CREATE (u) -[r:CLICKED] -> (c)

            // CONNECT EVENT WITH ItS KEYS  
                    SET e.node_keys = [ID(c)]
                    SET e.rel_keys = [ID(r)]
                         
                    RETURN c { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                    device_id=device_id, url=url , date = date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')

        with self.driver.session() as session:
            return session.execute_write(userClick, device_id, url , date)
