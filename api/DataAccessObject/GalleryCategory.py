from flask import abort

class GalleryCategory:

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
        # Get a list of GalleryCatgory from the database
        def getAllGalleryCategory(tx, sort, order, limit, skip):
            cypher = """MATCH (g:GalleryCatgory) 
            RETURN g {{ .* }} AS galleryCatgory
            ORDER BY g.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("galleryCatgory") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllGalleryCategory, sort, order, limit, skip)


    def findByName(self, name):
        """
        Find a gallarycatgory by their name.

        If no GalleryCatgory is found, a NotFoundError should be thrown.
        """
         # Find a GalleryCatgory by their name
        def getGalleryCategory(tx, name):
            cypher_query = """
                MATCH (g:GalleryCatgory {name: $name})
                RETURN g { .* } AS galleryCatgory
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, name=name).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("galleryCatgory")

        with self.driver.session() as session:
            return session.execute_read(getGalleryCategory, name)

    def addGalleryCategory(self, name):
        """
        Add new GalleryCatgory with the device_id and type of GalleryCatgory.
        """
        def createGalleryCategory(tx, name):
            row = tx.run("""
                    MERGE (g:GalleryCatgory {name: $name})
                    ON CREATE
                        SET g.created_at = timestamp()
                    RETURN g { .* } AS galleryCatgory
                    """,
                    name=name).single()
            return row.get("galleryCatgory")

        with self.driver.session() as session:
            return session.execute_write(createGalleryCategory , name)