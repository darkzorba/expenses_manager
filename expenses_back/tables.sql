CREATE TABLE income_type (
    id SERIAL PRIMARY KEY,  -- Usando SERIAL para auto incremento
    name VARCHAR(200) NULL
);

CREATE TABLE expense_type (
    id SERIAL PRIMARY KEY,  -- Usando SERIAL para auto incremento
    name VARCHAR(200) NULL
);

CREATE TABLE incomes (
    id SERIAL PRIMARY KEY,  -- Usando SERIAL para auto incremento
    value NUMERIC(16,2) NULL,
    description VARCHAR(200) NULL,
    type_id BIGINT NULL,  -- FK pode ser NULL
    date_income DATE NULL,
    status BOOLEAN NULL,
    CONSTRAINT fk_incomes_type FOREIGN KEY (type_id) REFERENCES income_type(id) ON DELETE no action
);

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,  -- Usando SERIAL para auto incremento
    value NUMERIC(16,2) NULL,
    description VARCHAR(200) NULL,
    type_id BIGINT NULL,  -- FK pode ser NULL
    date_expense DATE NULL,
    status BOOLEAN NULL,
    CONSTRAINT fk_expenses_type FOREIGN KEY (type_id) REFERENCES expense_type(id) ON DELETE no action
);
