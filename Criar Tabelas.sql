CREATE DATABASE AV3;
use AV3;

CREATE TABLE Produto (
	id 				INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nome			VARCHAR(100),
	preco_venda		DECIMAL(10,2) NOT NULL
);

CREATE TABLE Cliente (
	id 				INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nome			VARCHAR(100) NOT NULL,
	nascimento		DATE NOT NULL,
	tipo_de_cliente	INT NOT NULL
);

CREATE TABLE Fornecedor (
	id 			INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nome		VARCHAR(100),
	endereco	VARCHAR(200)
);

CREATE TABLE Historico_Preco_Venda (
	id 				INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	preco_venda		DECIMAL(10,2) NOT NULL,
	data_hora		DATETIME
);

CREATE TABLE Venda(
	id 					INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_cliente			INT NOT NULL,
	data_hora			DATETIME NOT NULL,
	forma_de_pagamento	INT NOT NULL,
	endereco_de_envio	VARCHAR(200),	
	CONSTRAINT fk_cliente_venda FOREIGN KEY (id_cliente) REFERENCES Cliente (id)
);

CREATE TABLE Venda_Produto (
	id 			INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_venda 	INT NOT NULL,
	id_produto	INT NOT NULL,
	quantidade	INT NOT NULL,
	CONSTRAINT fk_venda_venda_produto FOREIGN KEY (id_venda) REFERENCES Venda (id),
	CONSTRAINT fk_produto_venda_produto FOREIGN KEY (id_produto) REFERENCES Produto (id)
);

CREATE TABLE Estoque (
	id 				INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_produto		INT NOT NULL,
	quantidade		INT NOT NULL,
	CONSTRAINT fk_produto_estoque FOREIGN KEY (id_produto) REFERENCES Produto (id)
);


CREATE TABLE Compra (
	id 					INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_fornecedor		INT NOT NULL,
	data_hora			DATETIME,
	forma_de_pagamento	INT NOT NULL,
	CONSTRAINT fk_fornecedor_compra FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor (id)
);


CREATE TABLE Compra_Produto (
	id 				INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_produto		INT NOT NULL,
	id_compra		INT NOT NULL,
	quantidade		INT NOT NULL,
	preco_unidade	DECIMAL(10,2) NOT NULL,
	CONSTRAINT fk_produto_compra_produto FOREIGN KEY (id_produto) REFERENCES Produto (id),
	CONSTRAINT fk_compra_compra_produto FOREIGN KEY (id_compra) REFERENCES Compra (id)
);
