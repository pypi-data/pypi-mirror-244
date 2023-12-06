# crud.py

from sqlalchemy.orm import Session

def read(db: Session, model, condition):
    """
    Read an object from the database using a condition.

    Parameters
    ----------
    db: Session : Database session
    model : The model class to query
    condition : The condition to filter by

    Returns
    -------
    The first object that matches the condition or None if not found.
    """
    return db.query(model).filter(condition).first()

def create(db: Session, model, obj_data: dict):
    """
    Create a new object in the database.

    Parameters
    ----------
    db: Session : Database session
    model : The model class to create
    obj_data: dict : The data to create the new object with

    Returns
    -------
    The newly created object.
    """
    obj = model(**obj_data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, model, condition, obj_data: dict):
    """
    Update an object in the database that matches a condition.

    Parameters
    ----------
    db: Session : Database session
    model : The model class to update
    condition : The condition to filter by
    obj_data: dict : The data to update the object with

    Returns
    -------
    The updated object or None if not found.
    """
    obj = db.query(model).filter(condition).first()
    if obj:
        for key, value in obj_data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj
    return None

def delete(db: Session, model, condition):
    """
    Delete an object from the database that matches a condition.

    Parameters
    ----------
    db: Session : Database session
    model : The model class to delete from
    condition : The condition to filter by

    Returns
    -------
    True if the object was deleted, False otherwise.
    """
    obj = db.query(model).filter(condition).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False