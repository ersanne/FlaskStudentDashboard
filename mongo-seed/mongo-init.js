db.createUser(
        {
            user: "flask-app",
            pwd: "E9T8ydKeCvfc",
            roles: [
                {
                    role: "readWrite",
                    db: "studentportal"
                }
            ]
        }
);