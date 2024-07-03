-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Zoneat
-- -----------------------------------------------------
-- BD Zoneat
DROP SCHEMA IF EXISTS `Zoneat` ;

-- -----------------------------------------------------
-- Schema Zoneat
--
-- BD Zoneat
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Zoneat` DEFAULT CHARACTER SET utf8 ;
USE `Zoneat` ;

-- -----------------------------------------------------
-- Table `Zoneat`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `fecha_nacim` DATE NULL,
  `direccion` VARCHAR(150) NULL,
  `telefono` VARCHAR(12) NULL,
  `email` VARCHAR(45) NULL,
  `contrasena` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`categorias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_categ` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`suscripciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`suscripciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `valor` DECIMAL NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`propietarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`propietarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `fecha_nacim` DATE NULL,
  `direccion` VARCHAR(150) NULL,
  `telefono` VARCHAR(12) NULL,
  `email` VARCHAR(45) NULL,
  `contrasena` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`locales_comida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`locales_comida` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `telefono` VARCHAR(10) NULL,
  `direccion` VARCHAR(150) NULL,
  `email` VARCHAR(45) NULL,
  `sitio_web` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `suscripcion_id` INT NOT NULL,
  `categoria_id` INT NOT NULL,
  `propietario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_restaurantes_suscripciones_idx` (`suscripcion_id` ASC) VISIBLE,
  INDEX `fk_locales_comida_categorias1_idx` (`categoria_id` ASC) VISIBLE,
  INDEX `fk_locales_comida_propietarios1_idx` (`propietario_id` ASC) VISIBLE,
  CONSTRAINT `fk_restaurantes_suscripciones`
    FOREIGN KEY (`suscripcion_id`)
    REFERENCES `Zoneat`.`suscripciones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_locales_comida_categorias1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `Zoneat`.`categorias` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_locales_comida_propietarios1`
    FOREIGN KEY (`propietario_id`)
    REFERENCES `Zoneat`.`propietarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`calificaciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`calificaciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comentario` TEXT NULL,
  `cant_estrellas` TINYINT(5) NULL,
  `cod_verificacion` VARCHAR(5) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  `local_comida_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_calificaciones_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_calificaciones_restaurantes1_idx` (`local_comida_id` ASC) VISIBLE,
  CONSTRAINT `fk_calificaciones_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `Zoneat`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_calificaciones_restaurantes1`
    FOREIGN KEY (`local_comida_id`)
    REFERENCES `Zoneat`.`locales_comida` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`medios_pago`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`medios_pago` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`pagos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`pagos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `total` DECIMAL NULL,
  `num_cuota` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `suscripcion_id` INT NOT NULL,
  `medio_pago_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pagos_suscripciones1_idx` (`suscripcion_id` ASC) VISIBLE,
  INDEX `fk_pagos_medios_pago1_idx` (`medio_pago_id` ASC) VISIBLE,
  CONSTRAINT `fk_pagos_suscripciones1`
    FOREIGN KEY (`suscripcion_id`)
    REFERENCES `Zoneat`.`suscripciones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pagos_medios_pago1`
    FOREIGN KEY (`medio_pago_id`)
    REFERENCES `Zoneat`.`medios_pago` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Zoneat`.`preguntas_frecuentes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Zoneat`.`preguntas_frecuentes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(45) NULL,
  `respuesta` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
