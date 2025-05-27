CREATE TABLE leituras (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_chuva INTEGER,
    valor_luz INTEGER
);
