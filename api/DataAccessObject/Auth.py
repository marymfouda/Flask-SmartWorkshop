import bcrypt
from flask import  abort
from flask_jwt_extended import create_access_token

from neo4j.exceptions import ConstraintError

class Auth:
    """
    The Class used to handle Adimn authorization and authontication.
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

    def register(self, userName, plain_password):
        """
        This method should create a new Admin node in the database with the userName
        provided, along with an encrypted version of the password.

        The properties also be used to generate a JWT `token` which should be included
        with the returned admin.

        Parameters
        ----------
        userName : str
            The new admin userName.
        plain_password : str
            Plain text password to be encrypted.

        Returns
        -------
        userName : str
            The new admin userName.
        token : str
            Encoded JWT token with a set of 'claims'.

        Raises
        ------
        ConstraintError
            If the attribute's value is already in the graph database.
        """
        encrypted = bcrypt.hashpw(plain_password.encode("utf8"), bcrypt.gensalt()).decode('utf8')

        def createAdmin(tx, userName, encrypted):
            return tx.run("""
                CREATE (admin:Admin {
                    userName: $userName,
                    password: $encrypted
                })
                RETURN admin
            """,
            userName=userName, encrypted=encrypted
            ).single()

        try:
            with self.driver.session() as session:
                result = session.execute_write(createAdmin, userName, encrypted)

                admin = result['admin']

                payload = {
                    "userName":  admin["userName"]
                }

                access_token = create_access_token(identity=admin["userName"])
                payload['token'] = access_token

                return payload
        except ConstraintError as err:
            abort(422, err.message)


    def authenticate(self, userName, plain_password):
        """
        This method should attempt to find a admin by the userName provided
        and attempt to verify the password.

        If a admin is not found or the passwords do not match, a `false` value should
        be returned.  Otherwise, the users properties should be returned along with
        an encoded JWT token with a set of 'claims'.

        {
        userName: 'Adel,
        token: '...'
        }

        Parameters
        ----------
        userName : str
            Admin userName to search with.
        plain_password : str
            Plain text password used to verify the admin.

        Returns
        -------
        token : str
            Encoded JWT token with a set of 'claims'.
        """
        def getAdmin(tx, userName):
            result = tx.run("MATCH (admin:Admin {userName: $userName}) RETURN admin",
                userName=userName)

            first = result.single()

            if first is None:
                return None

            admin = first.get("admin")

            return admin

        with self.driver.session() as session:
            admin = session.execute_read(getAdmin, userName=userName)

            if admin is None:
                return False

            if bcrypt.checkpw(plain_password.encode('utf-8'), admin["password"].encode('utf-8')) is False:
                return False

            access_token = create_access_token(identity=admin["userName"])

            return {"token":access_token}
 