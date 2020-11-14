import psycopg2

def get_database_credentials():
    connection = psycopg2.connect(user = "hkmwrxkewkhzrh",
                                    password = "a8f37ea49b38f2d3d07d853b15ed59e0a7b5edaea657c3450c970dd8b9038a57",
                                    host = "ec2-54-91-178-234.compute-1.amazonaws.com",
                                    port = "5432",
                                    database = "de6eje61ar0ot3")
    return connection