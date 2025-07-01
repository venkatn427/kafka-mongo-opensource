import time
from superset import db, app
from superset.models.core import Database
from superset.models.slice import Slice
from superset.models.dashboard import Dashboard
from superset.connectors.sqla.models import SqlaTable
from sqlalchemy.exc import IntegrityError

def create_database():
    # MongoDB connection URI for Superset via SQLAlchemy
    mongo_uri = "mongodb+srv://username:password@mongodb_host:27017/dbname?retryWrites=true&w=majority"

    db_obj = db.session.query(Database).filter_by(database_name="MongoDB").first()
    if not db_obj:
        db_obj = Database(database_name="MongoDB", sqlalchemy_uri=mongo_uri)
        db.session.add(db_obj)
        db.session.commit()
        print("✅ MongoDB database added")
    else:
        print("ℹ️ MongoDB database already exists")
    return db_obj

def create_dataset(database, table_name):
    dataset = db.session.query(SqlaTable).filter_by(table_name=table_name).first()
    if not dataset:
        dataset = SqlaTable(table_name=table_name, database=database, schema=None, is_featured=True)
        db.session.add(dataset)
        db.session.commit()
        print(f"✅ Dataset for table '{table_name}' created")
    else:
        print(f"ℹ️ Dataset for table '{table_name}' already exists")
    return dataset

def create_chart(dataset, chart_name, viz_type, metrics):
    chart = db.session.query(Slice).filter_by(slice_name=chart_name).first()
    if not chart:
        chart = Slice(
            slice_name=chart_name,
            viz_type=viz_type,
            datasource_id=dataset.id,
            datasource_type='table',
            params=json.dumps(metrics),
        )
        db.session.add(chart)
        db.session.commit()
        print(f"✅ Chart '{chart_name}' created")
    else:
        print(f"ℹ️ Chart '{chart_name}' already exists")
    return chart

def create_dashboard(dashboard_name, charts):
    dashboard = db.session.query(Dashboard).filter_by(dashboard_title=dashboard_name).first()
    if not dashboard:
        dashboard = Dashboard(dashboard_title=dashboard_name, slices=charts)
        db.session.add(dashboard)
        db.session.commit()
        print(f"✅ Dashboard '{dashboard_name}' created")
    else:
        print(f"ℹ️ Dashboard '{dashboard_name}' already exists")
    return dashboard

if __name__ == "__main__":
    import json
    with app.app_context():
        db_obj = create_database()

        # Create datasets
        employees_ds = create_dataset(db_obj, "employees")
        departments_ds = create_dataset(db_obj, "departments")

        # Define chart params (customize based on your dataset & viz type)
        employees_chart_params = {
            "metrics": [{"expressionType": "SIMPLE", "column": {"column_name": "id"}, "aggregate": "COUNT"}],
            "groupby": [],
            "row_limit": 1000,
            "color_scheme": "supersetColors",
        }
        departments_chart_params = {
            "metrics": [{"expressionType": "SIMPLE", "column": {"column_name": "id"}, "aggregate": "COUNT"}],
            "groupby": [],
            "row_limit": 1000,
            "color_scheme": "supersetColors",
        }

        # Create charts
        emp_chart = create_chart(employees_ds, "Number of Employees", "big_number", employees_chart_params)
        dept_chart = create_chart(departments_ds, "Number of Departments", "big_number", departments_chart_params)

        # Create dashboard with these charts
        create_dashboard("Company Overview", [emp_chart, dept_chart])
