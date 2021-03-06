from app import app, db, Area, Unit, Module, Keyword, File, Link, Source, load_areas, load_keywords
from datetime import date, datetime
from faker import Faker
from sqlalchemy import null
import json
import os

fake = Faker()
Faker.seed(0)


def fill_with_fake(fake_auk=True):
    if fake_auk:
        random_areas(14)
        random_keywords(400)
    else:
        areas = Area.query.all()
        keywords = Keyword.query.all()
        if not len(areas):
            load_areas()
        if not len(keywords):
            load_keywords()
    random_files(300)
    random_urls(120)
    random_modules(100)


def random_modules(n):
    areas = Area.query.all()
    keywords = Keyword.query.all()
    files = set(File.query.all())
    links = Link.query.all()
    for i in range(n):
        new_module = Module(name=fake.catch_phrase(), author=fake.name(), description=fake.paragraph(nb_sentences=4), date_added=fake.date_between_dates(date.fromisoformat('2018-01-01'), date.fromisoformat('2019-12-31')), date_updated=fake.date_between_dates(date.fromisoformat('2020-01-01'), date.today()) if fake.random_int(min=0, max=1) else null())
        db.session.add(new_module)
        db.session.commit()
    modules = Module.query.all()
    for module in modules:
        chosen_area = fake.random_element(areas)
        chosen_units = list(set([fake.random_element(chosen_area.units) for _ in range(fake.random_int(min=1, max=2))]))
        chosen_keywords = list(set([fake.random_element(keywords) for _ in range(fake.random_int(min=2, max=4))]))
        chosen_files = list(set([fake.random_element(files) for _ in range(fake.random_int(min=1, max=3))]))
        chosen_links = list(set([fake.random_element(links) for _ in range(fake.random_int(min=2, max=5))]))
        module.units = chosen_units
        module.keywords = chosen_keywords
        module.files = chosen_files
        module.links = chosen_links
        for file in chosen_files:
            files.remove(file)
        db.session.commit()


def random_areas(n):
    for i in range(n):
        units = [unit.name for unit in Unit.query.all()]
        new_area = Area(name=fake.word(), units=[Unit(name=word) for word in fake.words(nb=fake.random_int(min=3, max=4)) if word not in units])
        db.session.add(new_area)
    db.session.commit()


def random_files(n):
    for i in range(n):
        new_file = File(name=fake.file_name())
        db.session.add(new_file)
    db.session.commit()
    files = File.query.all()
    for file in files:
        with open(os.path.join(app.config["UPLOAD_PATH"], str(file.id)), "wb") as file_out:
            file_out.write(os.urandom(1024))


def random_keywords(n):
    for i in range(n):
        keywords = [keyword.name for keyword in Keyword.query.all()]
        name = fake.word()
        if name not in keywords:
            new_keyword = Keyword(name=name, acronym=''.join(fake.random_letters(length=3)).upper() if fake.random_int(min=0, max=1) else '')
            db.session.add(new_keyword)
    db.session.commit()


def random_urls(n):
    for i in range(n):
        links = [link.url for link in Link.query.all()]
        url = fake.domain_name()
        if url not in links:
            new_url = Link(url=url)
            db.session.add(new_url)
    db.session.commit()


def clear_database():
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    clear_database()
    fill_with_fake(fake_auk=False)
