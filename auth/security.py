import bcrypt


class Security:

    @staticmethod
    def hash_password(password):

        password = password.encode("utf-8")

        hashed = bcrypt.hashpw(
            password,
            bcrypt.gensalt()
        )

        return hashed.decode("utf-8")


    @staticmethod
    def verify_password(password, hashed_password):

        password = password.encode("utf-8")

        hashed_password = hashed_password.encode("utf-8")

        return bcrypt.checkpw(
            password,
            hashed_password
        )