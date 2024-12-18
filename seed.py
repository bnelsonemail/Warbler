"""Seed database with sample data from CSV files."""

import os
import logging
from csv import DictReader
from app import db
from models import User, Message, Follows

logging.basicConfig(level=logging.INFO)

# Configurable file paths
USERS_CSV = os.getenv('USERS_CSV', 'generator/users.csv')
MESSAGES_CSV = os.getenv('MESSAGES_CSV', 'generator/messages.csv')
FOLLOWS_CSV = os.getenv('FOLLOWS_CSV', 'generator/follows.csv')

def validate_csv(file_path):
    """Check if the CSV file exists and is readable."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    if not file_path.endswith('.csv'):
        raise ValueError(f"{file_path} is not a valid CSV file.")

def seed_users():
    """Seed users table from users.csv."""
    logging.info("Seeding users...")
    validate_csv(USERS_CSV)
    with open(USERS_CSV) as users:
        db.session.bulk_insert_mappings(User, DictReader(users))
    logging.info("Users seeded successfully.")

def seed_messages():
    """Seed messages table from messages.csv."""
    logging.info("Seeding messages...")
    validate_csv(MESSAGES_CSV)
    with open(MESSAGES_CSV) as messages:
        db.session.bulk_insert_mappings(Message, DictReader(messages))
    logging.info("Messages seeded successfully.")

def seed_follows():
    """Seed follows table from follows.csv."""
    logging.info("Seeding follows...")
    validate_csv(FOLLOWS_CSV)
    with open(FOLLOWS_CSV) as follows:
        db.session.bulk_insert_mappings(Follows, DictReader(follows))
    logging.info("Follows seeded successfully.")

if __name__ == "__main__":
    logging.info("Dropping and creating tables...")
    db.drop_all()
    db.create_all()

    try:
        seed_users()
        seed_messages()
        seed_follows()
        db.session.commit()
        logging.info("Database seeding completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during seeding: {e}")
        db.session.rollback()
