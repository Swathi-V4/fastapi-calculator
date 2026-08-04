from app.models import Calculation, User
from app.schemas import CalculationCreate
from app.security import hash_password
from app.services.calculation_factory import CalculationFactory


def test_insert_calculation_record(db_session):
    user = User(
        username="integrationuser",
        email="integrationuser@test.com",
        password_hash=hash_password("Password123!"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    calculation_data = CalculationCreate(
        a=20,
        b=4,
        type="Divide",
    )

    result = CalculationFactory.calculate(
        calculation_data.type,
        calculation_data.a,
        calculation_data.b,
    )

    calculation = Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
        user_id=user.id,
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    saved_calculation = (
        db_session.query(Calculation)
        .filter(
            Calculation.id == calculation.id,
            Calculation.user_id == user.id,
        )
        .first()
    )

    assert saved_calculation is not None
    assert saved_calculation.a == 20
    assert saved_calculation.b == 4
    assert saved_calculation.type == "Divide"
    assert saved_calculation.result == 5
    assert saved_calculation.user_id == user.id