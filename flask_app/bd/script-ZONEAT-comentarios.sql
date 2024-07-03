-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema esquema_zoneat
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_zoneat` ;

-- -----------------------------------------------------
-- Schema esquema_zoneat
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_zoneat` DEFAULT CHARACTER SET utf8 ;
USE `esquema_zoneat` ;

-- -----------------------------------------------------
-- Table `esquema_zoneat`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_zoneat`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `tipo_usuario` CHAR(1) NOT NULL,
  `email` VARCHAR(45) NULL,
  `contrasena` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_zoneat`.`locales_comida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_zoneat`.`locales_comida` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `direccion` VARCHAR(150) NULL,
  `telefono` VARCHAR(12) NULL,
  `email` VARCHAR(45) NULL,
  `sitio_web` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_peliculas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_peliculas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_zoneat`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_zoneat`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_zoneat`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comentario` TEXT NULL,
  `cant_estrellas` TINYINT(5) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  `local_comida_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentarios_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_comentarios_peliculas1_idx` (`local_comida_id` ASC) VISIBLE,
  CONSTRAINT `fk_comentarios_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_zoneat`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comentarios_peliculas1`
    FOREIGN KEY (`local_comida_id`)
    REFERENCES `esquema_zoneat`.`locales_comida` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
