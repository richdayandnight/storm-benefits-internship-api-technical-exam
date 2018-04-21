from companyAPI.models import Company
from companyAPI.database import db_session

# Insert 2 records in the company table under the Company database
def populate():
    company_temp = Company(1, 'Jollibee Foods Corporation', 9999, 'Philippines', 'feedback@jollibee.com', 'Food')
    company_temp2 = Company(2, 'Google', 73992, 'USA', 'sample@gmail.com', 'Software')
    db_session.add(company_temp)
    db_session.add(company_temp2)
    db_session.commit()
