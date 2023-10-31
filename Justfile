requirements:
    pip-compile --strip-extras requirements.in
    pip-compile --strip-extras test-requirements.in

run:
    uvicorn app:app --reload

test:
    pytest