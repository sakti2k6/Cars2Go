from app import carsDb

def reset_db():
#Delete all tables and create again
    try:
        print("[INFO] Resetting postgreSQL database")
        carsDb.drop_all()
        carsDb.create_all()
    except Exception as e:
        print("[ERROR] Resetting database failed")
        print(str(e))

if __name__ == "__main__":
    reset_db()
