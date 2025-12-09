import sqlite3

conn = sqlite3.connect("beauty_salon.db")
cursor = conn.cursor()

# Увімкнути зовнішні ключі
cursor.execute("PRAGMA foreign_keys = ON;")

# ============================
#  РОЛЬ
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Role (
    RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    roleName TEXT NOT NULL UNIQUE
);
""")

# ============================
#  КОРИСТУВАЧ
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    password TEXT NOT NULL,
    createdAt TEXT NOT NULL
);
""")

# ============================
#  UserRole (зв’язок M:N)
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS UserRole (
    UserRoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    RoleID INTEGER NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID) ON DELETE CASCADE
);
""")

# ============================
#  КЛІЄНТ (1:1 з User)
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Client (
    ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL UNIQUE,
    notes TEXT,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);
""")

# ============================
#  МАЙСТЕР (1:1 з User)
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Master (
    MasterID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL UNIQUE,
    specialization TEXT,
    experienceYears INTEGER,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);
""")

# ============================
#  ПОСЛУГА
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Service (
    ServiceID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    basePrice REAL NOT NULL,
    duration INTEGER NOT NULL
);
""")

# ============================
#  MASTER–SERVICE (M:N)
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS MasterService (
    MasterServiceID INTEGER PRIMARY KEY AUTOINCREMENT,
    MasterID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    priceOverride REAL,
    FOREIGN KEY (MasterID) REFERENCES Master(MasterID) ON DELETE CASCADE,
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID) ON DELETE CASCADE
);
""")

# ============================
#  ЗАПИС (APPOINTMENT)
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Appointment (
    AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClientID INTEGER NOT NULL,
    MasterID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    startTime TEXT NOT NULL,
    endTime TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES Client(ClientID),
    FOREIGN KEY (MasterID) REFERENCES Master(MasterID),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
);
""")

# ============================
#  ПЛАТІЖ
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Payment (
    PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    AppointmentID INTEGER NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);
""")

conn.commit()
conn.close()

print("Базу даних успішно створено!")