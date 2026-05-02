


-- daily_activity определение

CREATE TABLE IF NOT EXISTS "daily_activity" (
	"day_id"	INTEGER,
	"user_id"	INTEGER,
	"date"	DATE,
	"total_sessions"	INTEGER DEFAULT 0,
	"total_time"	INTEGER DEFAULT 0,
	"avg_cpm"	REAL DEFAULT 0,
	"best_cpm"	REAL DEFAULT 0,
	"avg_accuracy"	REAL DEFAULT 0,
	PRIMARY KEY("day_id" AUTOINCREMENT),
	UNIQUE("user_id","date"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS "idx_daily_uid_date" ON "daily_activity" (
	"user_id",
	"date"
);


-- sessions определение

CREATE TABLE IF NOT EXISTS "sessions" (
	"session_id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"test_type"	TEXT,
	"text_id"	TEXT,
	"gen_text"	TEXT,
	"start_time"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"duration_seconds"	INTEGER,
	"total_chars"	INTEGER,
	"avg_cpm"	REAL,
	"max_cpm"	REAL,
	"accuracy"	REAL,
	"date"	DATE NOT NULL DEFAULT CURRENT_DATE,
	"total_errors"	INTEGER,
	PRIMARY KEY("session_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE
);

-- texts определение

CREATE TABLE IF NOT EXISTS texts  (
    id INTEGER PRIMARY KEY,
    language TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    length TEXT NOT NULL,
    content TEXT NOT NULL,
    size INTEGER,
    source TEXT
);

CREATE INDEX IF NOT EXISTS idx_language ON texts(language);
CREATE INDEX IF NOT EXISTS idx_difficulty ON texts(difficulty);
CREATE INDEX IF NOT EXISTS idx_length ON texts(length);


-- time_points определение

CREATE TABLE IF NOT EXISTS "time_points" (
	"point_id"	INTEGER,
	"session_id"	INTEGER NOT NULL,
	"second"	INTEGER DEFAULT 0,
	"chars"	INTEGER DEFAULT 0,
	"cpm"	REAL DEFAULT 0,
	"errors"	INTEGER DEFAULT 0,
	PRIMARY KEY("point_id" AUTOINCREMENT),
	FOREIGN KEY("session_id") REFERENCES "sessions"("session_id") ON DELETE CASCADE
);


-- users определение

CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"avatar"	TEXT,
	"password_hash"	TEXT,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"sync_token"	TEXT NOT NULL,
	"settings"	TEXT,
	"total_sessions"	INTEGER DEFAULT 0,
	"total_time"	INTEGER DEFAULT 0,
	"total_chars"	INTEGER DEFAULT 0,
	"best_cpm"	INTEGER DEFAULT 0,
	"avg_cpm"	INTEGER DEFAULT 0,
	"avg_accuracy"	INTEGER DEFAULT 0,
	"max_streak"	INTEGER DEFAULT 0,
	"current_streak"	INTEGER DEFAULT 0,
	"total_days"	INTEGER DEFAULT 0,
	"recovery_hash"	TEXT,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);



-- words определение

CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    language TEXT NOT NULL,
    word TEXT NOT NULL
);