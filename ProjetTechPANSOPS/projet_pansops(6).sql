-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 18 fév. 2025 à 14:51
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `projet_pansops`
--

-- --------------------------------------------------------

--
-- Structure de la table `agents`
--

CREATE TABLE `agents` (
  `id_agents` int(11) NOT NULL,
  `statut_agent` enum('Actif','Inactif') NOT NULL DEFAULT 'Actif',
  `nom_agent` text NOT NULL,
  `prenom_agent` text NOT NULL,
  `date_naissance_agent` date NOT NULL,
  `tel_agent` text NOT NULL,
  `fin_formation_theorique_agent` date NOT NULL,
  `debut_activite_enac` date DEFAULT NULL,
  `fin_activite_enac` date DEFAULT NULL,
  `motPasse` text NOT NULL,
  `staut_admin_agent` enum('Administrateur','Agent') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `agents`
--

INSERT INTO `agents` (`id_agents`, `statut_agent`, `nom_agent`, `prenom_agent`, `date_naissance_agent`, `tel_agent`, `fin_formation_theorique_agent`, `debut_activite_enac`, `fin_activite_enac`, `motPasse`, `staut_admin_agent`) VALUES
(2, 'Actif', 'Mensoif', 'Gérard', '1999-11-25', '066482233', '2024-11-03', NULL, NULL, '', NULL),
(4, 'Actif', 'Dupont', 'Martin', '2006-11-02', '0123456789', '2024-11-06', NULL, NULL, '', NULL),
(5, 'Actif', 'Labrosse', 'Adam', '2004-11-10', '0244489238', '2024-11-13', NULL, NULL, '', NULL),
(6, 'Actif', 'Strueux', 'Simon', '2005-11-09', '093454534', '2024-11-01', NULL, NULL, '', NULL),
(11, 'Actif', 'Test', 'Teste', '2025-02-13', '23544332232', '2025-02-05', NULL, NULL, '', NULL),
(12, 'Actif', 'Pierre', 'Paul', '2004-01-30', '0666356978', '2021-02-01', NULL, NULL, '', NULL),
(13, 'Actif', 'Martin', 'Titouan', '2002-09-12', '23434231', '2020-02-12', '2024-09-12', NULL, '', NULL),
(14, 'Actif', 'Bla', 'Bla', '2002-02-24', '0664000000', '2009-03-25', '2025-01-01', NULL, '6ff0ccf44d37b9eaa30da126d71ae2dbb02e82eed50756ad20b77a7294c95748', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `maintien_competences`
--

CREATE TABLE `maintien_competences` (
  `id_maintien_competences` int(11) NOT NULL,
  `titre_maintien_competences` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `maintien_competences`
--

INSERT INTO `maintien_competences` (`id_maintien_competences`, `titre_maintien_competences`) VALUES
(1, 'Concevoir ou modifier tout ou partie d\'une procédure'),
(2, 'Assister un concepteur en formation pour la conception d\'une procédure'),
(3, 'Vérifier une procédure conçue par un autre\r\n'),
(4, 'Participer en temps que formateur à une formation de concepteurs'),
(5, 'Participer à l\'examen périodique d\'une procédure\r\n'),
(6, 'Formation continue');

-- --------------------------------------------------------

--
-- Structure de la table `participation_agent`
--

CREATE TABLE `participation_agent` (
  `id_participation_agent` int(11) NOT NULL,
  `id_agent` int(11) NOT NULL,
  `id_maintien_competences` int(11) NOT NULL,
  `date_participation_agent` date NOT NULL,
  `date_debut_formation` date DEFAULT NULL,
  `commentaires` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `participation_agent`
--

INSERT INTO `participation_agent` (`id_participation_agent`, `id_agent`, `id_maintien_competences`, `date_participation_agent`, `date_debut_formation`, `commentaires`) VALUES
(2, 2, 4, '2024-11-12', NULL, ''),
(9, 2, 1, '2025-01-02', NULL, ''),
(10, 2, 1, '2025-01-01', NULL, ''),
(11, 2, 5, '2025-01-14', NULL, ''),
(12, 2, 6, '2025-01-21', NULL, ''),
(13, 2, 6, '2025-01-21', NULL, ''),
(14, 4, 6, '2025-01-08', NULL, ''),
(16, 4, 6, '2025-01-01', NULL, ''),
(17, 5, 6, '2025-01-08', NULL, ''),
(18, 2, 6, '2025-01-01', NULL, ''),
(19, 2, 1, '2023-02-01', NULL, ''),
(20, 6, 3, '2025-01-08', NULL, ''),
(21, 5, 4, '2025-01-01', NULL, ''),
(22, 4, 2, '2025-02-03', NULL, ''),
(23, 4, 4, '2025-02-01', NULL, ''),
(24, 11, 2, '2025-01-31', NULL, ''),
(25, 11, 3, '2024-12-27', NULL, ''),
(26, 11, 5, '2025-01-26', NULL, ''),
(27, 11, 2, '2025-02-03', NULL, ''),
(28, 11, 6, '2025-02-04', NULL, ''),
(29, 12, 4, '2022-02-01', NULL, ''),
(30, 12, 6, '2023-02-01', NULL, ''),
(31, 12, 3, '2023-03-23', NULL, ''),
(32, 12, 2, '2024-03-02', NULL, ''),
(33, 12, 3, '2024-03-02', NULL, ''),
(34, 12, 6, '2025-02-05', NULL, ''),
(36, 13, 1, '2025-01-01', NULL, 'OK'),
(37, 13, 6, '2022-03-02', NULL, 'OK'),
(38, 13, 6, '2024-05-02', NULL, 'OK'),
(39, 13, 3, '2023-04-02', NULL, 'OK'),
(40, 13, 4, '2024-04-06', NULL, 'OK');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`id_agents`);

--
-- Index pour la table `maintien_competences`
--
ALTER TABLE `maintien_competences`
  ADD PRIMARY KEY (`id_maintien_competences`);

--
-- Index pour la table `participation_agent`
--
ALTER TABLE `participation_agent`
  ADD PRIMARY KEY (`id_participation_agent`),
  ADD KEY `participation_agent_ibfk_1` (`id_maintien_competences`),
  ADD KEY `id_agent` (`id_agent`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `agents`
--
ALTER TABLE `agents`
  MODIFY `id_agents` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT pour la table `maintien_competences`
--
ALTER TABLE `maintien_competences`
  MODIFY `id_maintien_competences` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `participation_agent`
--
ALTER TABLE `participation_agent`
  MODIFY `id_participation_agent` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `participation_agent`
--
ALTER TABLE `participation_agent`
  ADD CONSTRAINT `participation_agent_ibfk_1` FOREIGN KEY (`id_maintien_competences`) REFERENCES `maintien_competences` (`id_maintien_competences`),
  ADD CONSTRAINT `participation_agent_ibfk_2` FOREIGN KEY (`id_agent`) REFERENCES `agents` (`id_agents`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
