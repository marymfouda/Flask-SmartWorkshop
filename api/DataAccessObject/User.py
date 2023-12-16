from flask import abort

class User:
    """
    The Class used to handle User Nodes operations.
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

    def all(self, sort = 'name', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of user.

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
            Contain user informations.
        """

        def getAllUsers(tx, sort, order, limit, skip):
            cypher = """MATCH (u:User) 
            RETURN u {{ .* }} AS user
            ORDER BY u.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("user") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllUsers, sort, order, limit, skip)


    def findById(self, device_id):
        """
        Find a user by their ID.
        If no user is found, abort with 404 status code.

        Parameters
        ----------
        device_id : int or str
            The id used to identify a user.

        Returns
        -------
        dict
            Contain user informations.
        """

        def getUser(tx, device_id):
            cypher_query = """
                MATCH (u:User {device_id: $device_id})
                RETURN u { .* } AS user
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, device_id=device_id).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("user")

        with self.driver.session() as session:
            return session.execute_read(getUser, device_id)

    def addUser(self, device_id, type):
        """
        Add new user with the device_id and type of user.

        Parameters
        ----------
        device_id : int or str
            The id used to identify a user.

        type : str
            Type of the user either Normal, Carpenter or Alumetal technician

        Returns
        -------
        dict
            Contain user informations.
        """

        def createUser(tx, device_id, type):
            row = tx.run("""
                    MERGE (u:User {device_id : $device_id})
                    ON Match 
                        SET u.type = $type
                    ON CREATE
                        SET u.type = $type
                        SET u.created_at = timestamp()
                    RETURN u { .* } AS user
                    """,
                    device_id=device_id, type=type).single()
            return row.get("user")

        with self.driver.session() as session:
            return session.execute_write(createUser, device_id, type)
