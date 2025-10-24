import pandas as pd
from models import db, Scheme
from app import app

df = pd.read_csv('indian_gov_schemes.csv')
existing_slugs = set()

with app.app_context():
    for _, row in df.iterrows():
        if row['slug'] in existing_slugs:
            continue  # Skip duplicate slugs
        existing_slugs.add(row['slug'])
        s = Scheme(
            scheme_name=row['scheme_name'],
            slug=row['slug'],
            details=row['details'],
            benefits=row['benefits'],
            eligibility=row['eligibility'],
            application=row['application'],
            documents=row['documents'],
            level=row['level'],
            schemeCategory=row['schemeCategory'],
            tags=row['tags']
        )
        db.session.add(s)
    db.session.commit()
print("Database populated with schemes successfully.")
