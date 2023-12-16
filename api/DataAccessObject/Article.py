from flask import abort
from neo4j.exceptions import ConstraintError

class Article:

    def __init__(self, driver):
        """
        The constructor expects an instance of the Neo4j Driver, which will be
        used to interact with Neo4j.
        """
        self.driver = driver

    def all(self, sort = 'title', order = 'ASC', limit = 6, skip = 0):
        """
        This method should return a paginated list of article.

        Results should be ordered by the `sort` parameter and limited to the
        number passed as `limit`.  The `skip` variable should be used to skip a
        certain number of rows.
        """
        # Get a list of users from the database
        def getAllArticle(tx, sort, order, limit, skip):
            cypher = """MATCH (a:Article) 
            RETURN a {{ .* }} AS article
            ORDER BY a.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            #### TODO: DEBUG
            print(cypher)
            result = tx.run(cypher, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("article") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(getAllArticle, sort, order, limit, skip)


    def findByTitle(self, title):
        """
        Find a article by their title .

        If no article is found, a NotFoundError should be thrown.
        """
         # Find an article by their title
        def get_article(tx, title):
            cypher_query = """
                MATCH (a:Article {title: $title})
                RETURN a { .* } AS Article
            """

            print(cypher_query)      #### TODO: DEBUG
            row = tx.run(cypher_query, title = title).single()

            if row == None:
                abort(404, 'Resource not found')

            return row.get("Article")

        with self.driver.session() as session:
            return session.execute_read(get_article, title)

    def addArticle(self, title , text):
        """
        Add new article with the title and type of article.
        """
        def createArticle(tx, title , text):
            row = tx.run("""
                    MERGE (a:Article {title : $title, text: $text})
                    ON CREATE
                        SET a.created_at = timestamp()
                    RETURN a { .* } AS Article
                    """,
                    title=title, text = text).single()
            return row.get("Article")

        with self.driver.session() as session:
            return session.execute_write(createArticle, title , text)
        
    def NewViewedArticle(self,device_id, title , text , date):
        """
        Add new Article node .

        Parameters
        ----------
        title :  str
            The id used to identify the User.
        
        text : str
        
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

        def ViewedArticle(tx,device_id ,title , text , date):
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
                         
            // ARTICLE CREATION
                    MERGE (a:Article {title : $title})
                    ON CREATE 
                        SET a.text = $text
                        SET a.created_at = $date
                    
                    CREATE (u) -[r:VIEWED_ARTICLE] -> (a)
                                              
            // CONNECT EVENT WITH ItS KEYS   
                    SET e.node_keys = [ID(a)]
                    SET e.rel_keys = [ID(r)]

                         
                    return a { .* , user : u.device_id,
                        relationship : type(r), event_triggered_at : t.created_at}  AS Output 
                    """,
                    device_id=device_id,title=title, text=text , date=date).single()
            
            print(row)      #### TODO: DEBUG
            if not row:
                return {"message" : "User doesn't exist"}
            return row.get('Output')
            # return dict(row) #### TODO: DEBUG

        try:
            with self.driver.session() as session:
                return session.execute_write(ViewedArticle,device_id, title , text , date )
            
        except ConstraintError as err:
            abort(422, err.message)