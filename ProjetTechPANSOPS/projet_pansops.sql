-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 23 mars 2025 à 22:46
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
  `statut_admin_agent` enum('Administrateur','Agent') DEFAULT 'Agent'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `agents`
--

INSERT INTO `agents` (`id_agents`, `statut_agent`, `nom_agent`, `prenom_agent`, `date_naissance_agent`, `tel_agent`, `fin_formation_theorique_agent`, `debut_activite_enac`, `fin_activite_enac`, `motPasse`, `statut_admin_agent`) VALUES
(18, 'Actif', 'agent', 'agent', '2000-01-01', '123456789', '2020-01-01', '2023-01-01', NULL, 'd4f0bc5a29de06b510f9aa428f1eedba926012b591fef7a518e776a7c9bd1824', 'Administrateur');

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
  `commentaires` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  MODIFY `id_agents` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT pour la table `maintien_competences`
--
ALTER TABLE `maintien_competences`
  MODIFY `id_maintien_competences` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `participation_agent`
--
ALTER TABLE `participation_agent`
  MODIFY `id_participation_agent` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

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
