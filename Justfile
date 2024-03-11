requirements:
    pip-compile --strip-extras requirements.in
    pip-compile --strip-extras dev-requirements.in

run:
    uvicorn app:app --reload

test:
    pytest