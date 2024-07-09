-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-02-2022 a las 13:22:47
-- Versión del servidor: 10.4.21-MariaDB
-- Versión de PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tfg_xatbot_v5`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `assignatura`
--

CREATE TABLE `assignatura` (
  `codi` int(11) NOT NULL,
  `curs` int(11) NOT NULL,
  `semestre` int(11) NOT NULL,
  `nom_grau` varchar(65) NOT NULL,
  `nom` varchar(65) NOT NULL,
  `password` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `assignatura`
--

INSERT INTO `assignatura` (`codi`, `curs`, `semestre`, `nom_grau`, `nom`, `password`) VALUES
(100137, 1, 1, 'Física', 'Mecànica i Relativitat', 'MR_F_TFG_XATBOT'),
(102760, 4, 1, 'Enginyeria Informàtica', 'Gestió de Projectes', 'GP_ENG_TFG_XATBOT'),
(106542, 4, 0, 'Enginyeria Informàtica', 'Treball de Final de Grau', 'TFG_ENG_TFG_XATBOT');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consulta`
--

CREATE TABLE `consulta` (
  `titol_faq` varchar(65) NOT NULL,
  `niu_estudiant` int(11) NOT NULL,
  `data` datetime NOT NULL,
  `valoracio` int(11) NOT NULL,
  `codi_assignatura` int(11) DEFAULT NULL,
  `nom_grau` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `consulta`
--

INSERT INTO `consulta` (`titol_faq`, `niu_estudiant`, `data`, `valoracio`, `codi_assignatura`, `nom_grau`) VALUES
('Horaris de l\'assignatura.', 1111111, '2022-01-31 16:18:20', 0, 102760, 'Enginyeria Informàtica'),
('Horaris de l\'assignatura.', 1456958, '2022-02-01 17:20:26', 0, 102760, 'Enginyeria Informàtica'),
('Informació general sobre el grau.', 1456958, '2022-02-03 12:15:50', 0, NULL, 'Enginyeria Informàtica'),
('Informació general sobre el grau.', 1456958, '2022-02-03 12:20:00', 0, NULL, 'Enginyeria Informàtica'),
('PREGUNTA B sobre el tema Introducció Gestió de Projectes.', 1456958, '2022-02-03 12:37:11', 0, 102760, 'Enginyeria Informàtica'),
('PREGUNTA B sobre el tema Selecció de projectes.', 1456958, '2022-02-03 12:08:50', 0, 102760, 'Enginyeria Informàtica'),
('PREGUNTA J sobre el tema Cicle de Vida del Projecte.', 1456958, '2022-02-03 12:21:06', 0, 102760, 'Enginyeria Informàtica'),
('PREGUNTA K sobre el tema Cicle de Vida del Projecte.', 1111111, '2022-01-31 16:18:45', 0, 102760, 'Enginyeria Informàtica'),
('Quines mencions té aquest grau?', 1456958, '2022-02-03 12:21:51', 0, NULL, 'Enginyeria Informàtica'),
('Quines són les assignatures optatives  d\'aquest grau?', 1456958, '2022-02-03 12:20:05', 0, NULL, 'Enginyeria Informàtica'),
('Quines són les assignatures optatives  d\'aquest grau?', 1456958, '2022-02-03 12:36:58', 0, NULL, 'Enginyeria Informàtica'),
('Sobre l\'avaluació.', 1111111, '2022-01-31 16:18:05', 0, 102760, 'Enginyeria Informàtica'),
('Sobre l\'avaluació.', 1456958, '2022-02-01 17:20:16', 0, 102760, 'Enginyeria Informàtica'),
('Sobre l\'avaluació.', 1456958, '2022-02-03 12:08:19', 0, 102760, 'Enginyeria Informàtica'),
('Sobre l\'avaluació.', 1456958, '2022-02-03 12:20:41', 0, 102760, 'Enginyeria Informàtica'),
('Sobre l\'avaluació.', 1456958, '2022-02-03 12:37:16', 0, 102760, 'Enginyeria Informàtica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiant`
--

CREATE TABLE `estudiant` (
  `codi_assignatura` int(11) NOT NULL,
  `niu_usuari` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `estudiant`
--

INSERT INTO `estudiant` (`codi_assignatura`, `niu_usuari`) VALUES
(102760, 1456958);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `faqs`
--

CREATE TABLE `faqs` (
  `titol` varchar(65) NOT NULL,
  `resposta` text NOT NULL,
  `categoria` varchar(65) NOT NULL,
  `codi_assignatura` int(11) DEFAULT NULL,
  `nom_grau` varchar(65) NOT NULL,
  `titol_tema` varchar(65) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `faqs`
--

INSERT INTO `faqs` (`titol`, `resposta`, `categoria`, `codi_assignatura`, `nom_grau`, `titol_tema`, `id`) VALUES
('Sobre l\'avaluació.', '<b>Càlcul de la nota final:</b>\r\n\r\n- <b>Teoria</b> (mínim 5 de 10), que correspon al 50% de la nota base final. La nota de teoria serà la mitjana ponderada de les parts avaluades:\r\n\r\n<b>Exàmens d’avaluació del coneixement teòric i tècniques de l’assignatura (90%):</b>\r\n\r\n--- 50% - 1er EXAMEN (Octubre): Estudi de Viabilitat del Projecte\r\n--- 50% - 2on EXAMEN (Gener, data prevista pel centre): Implementació i seguiment del Projecte\r\n--- En cas de suspendre una de les parts amb menys de 4, o voler pujar nota: 100% Examen Recuperació (data prevista pel centre). Caldrà fer un examen de les dues parts, independentment de si heu suspès un dels parcials o tots dos.\r\n\r\nNOTA MÍNIMA DELS PARCIALS PER FER MITJANA: 4\r\n\r\n<b>Exercicis de tècniques</b> (10%): Exercicis proposats a classe, que s’hauran d’entregar el dia indicat pel professor. Els exercicis no són obligatoris, però sí molt recomanables i necessaris per optar a matrícula d\'honor. No es poden recuperar.\r\n\r\n<b>Assistència a conferències</b> 0,1 punts a sumar a la nota final de teoria per assistència a cada una de les conferències o activitats proposades.\r\n\r\n- <b>Pràctiques</b> (mínim 5 de 10), que correspon al 50% de la nota base final.\r\n\r\n\r\nPer més info. consultar:\r\nhttps://guies.uab.cat/guies_docents/public/portal/html/2021/assignatura/102760/ca', 'dades', 102760, 'Enginyeria Informàtica', NULL, 1),
('Horaris de l\'assignatura.', 'Els horaris de l\'assignatura es poden trobar en el següent enllaç:\r\nhttps://www.uab.cat/doc/Horari_GEI_Curs4_Sem1', 'dades', 102760, 'Enginyeria Informàtica', NULL, 2),
('PREGUNTA A sobre el tema Introducció Gestió de Projectes.', 'RESPOSTA A Introducció Gestió de Projectes.', 'dades', 102760, 'Enginyeria Informàtica', 'Introducció Gestió de Projectes', 3),
('PREGUNTA B sobre el tema Introducció Gestió de Projectes.', 'RESPOSTA B Introducció Gestió de Projectes.', 'dades', 102760, 'Enginyeria Informàtica', 'Introducció Gestió de Projectes', 4),
('PREGUNTA C sobre el tema Introducció Gestió de Projectes.', 'RESPOSTA C Introducció Gestió de Projectes.', 'dades', 102760, 'Enginyeria Informàtica', 'Introducció Gestió de Projectes', 5),
('PREGUNTA A sobre el tema Selecció de projectes.', 'RESPOSTA A Selecció de projectes.', 'dades', 102760, 'Enginyeria Informàtica', 'Selecció de Projectes', 6),
('PREGUNTA B sobre el tema Selecció de projectes.', 'RESPOSTA B Selecció de projectes.', 'dades', 102760, 'Enginyeria Informàtica', 'Selecció de Projectes', 7),
('PREGUNTA C sobre el tema Selecció de projectes.', 'RESPOSTA C Selecció de projectes.', 'dades', 102760, 'Enginyeria Informàtica', 'Selecció de Projectes', 8),
('PREGUNTA A sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA A Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 9),
('PREGUNTA B sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA B Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 10),
('PREGUNTA C sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA C Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 11),
('PREGUNTA D sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA D Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 12),
('PREGUNTA E sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA E Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 13),
('PREGUNTA H sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA H Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 14),
('PREGUNTA I sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA I Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 15),
('PREGUNTA J sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA J Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 16),
('PREGUNTA K sobre el tema Cicle de Vida del Projecte.', 'RESPOSTA K Cicle de Vida del Projecte.', 'dades', 102760, 'Enginyeria Informàtica', 'Cicle de Vida del Projecte', 17),
('Informació general sobre el grau.', 'Pots trobar informació general sobre el grau a la següent pàgina.\r\n\r\nhttps://www.uab.cat/web/estudiar/llistat-de-graus/informacio-general/enginyeria-informatica-1216708251447.html?param1=1263367146646', 'grau', NULL, 'Enginyeria Informàtica', NULL, 18),
('Quines mencions té aquest grau?', 'Menció en Enginyeria del Software\r\nMenció en Enginyeria de Computadors\r\nMenció en Computació\r\nMenció en Tecnologies de la Informació\r\nMenció en Sistemes d\'Informació (aquesta menció, actualment, no es programa)\r\n\r\nhttps://www.uab.cat/web/estudiar/llistat-de-graus/pla-d-estudis/pla-d-estudis-i-horaris/enginyeria-informatica-1345467811493.html?param1=1263367146646', 'grau', NULL, 'Enginyeria Informàtica', NULL, 19),
('Quines són les assignatures optatives  d\'aquest grau?', '- Pràctiques Externes\r\n- Anglès Professional I\r\n- Anglès Professional II\r\n- Tendències Actuals\r\n- Aplicacions de la Teoria de Codis (1)\r\n- Internet de les Coses\r\n- Tecnologia Blockchain i Criptomonedes (1)\r\n- Tecnologies de Compressió de la Informació (1)(1) Aquestes assignatures optatives s\'ofereixen només als alumnes que cursen la menció en Tecnologies de la Informació.\r\n\r\nL\'estudiant també pot cursar, com a optativa, qualsevol assignatura dels blocs de tecnologia específica que no hagi cursat com a obligatòria.\r\n\r\n\r\nPer més info. consultar:\r\nhttps://www.uab.cat/web/estudiar/llistat-de-graus/pla-d-estudis/pla-d-estudis-i-horaris/enginyeria-informatica-1345467811493.html?param1=1263367146646', 'grau', NULL, 'Enginyeria Informàtica', NULL, 20),
('Què és el TFG?', 'És un <b>exercici original a realitzar individualment i presentar i defensar davant un tribunal universitari</b>, consistent en un projecte en l\'àmbit de les tecnologies específiques de l\'Enginyeria en Informàtica de caire professional en el que es sintetitzin i integrin les competències adquirides en els ensenyaments. Aquest treball suposa una càrrega de treball personal de l\'estudiant de 300 hores.\r\n\r\n\r\nPer més info. consultar:\r\nhttps://guies.uab.cat/guies_docents/public/portal/html/2021/assignatura/106542/ca', 'dades', 106542, 'Enginyeria Informàtica', NULL, 21),
('Qui pot oferir treballs?', 'a) <b>Professorat/departaments.<7b> Seguint el calendari aprovat per l\'Escola hauran de proposar temes/projectes utilitzant l\'aplicació informàtica corresponent. Si es considera convenient, el responsable de l\'assignatura i/o la Comissió de TFG supervisarà si els treballs proposats són adequats.\r\n\r\nb) <b>Empreses o Institucions externes.</b> El treball es pot realitzar en el marc d\'un conveni de col·laboració amb una empresa o institució externa. L\'entitat haurà de fer arribar la proposta per escrit (seguint el model establert a tal efecte, en les dates especificades) al responsable de l\'assignatura. El responsable i/o la Comissió de TFG supervisarà que el projecte proposat sigui adequat (es valorarà que es puguin avaluar les competències previstes al grau -i a la menció corresponent- i que la durada i càrrega de treball sigui adient). Si s\'accepta la proposta, s\'assignarà un professor tutor de la menció que correspongui i s\'introduiran les dades a l\'aplicació. Aquests projectes estan supervisats pel tutor acadèmic de l\'escola i per un tutor de l\'empresa.\r\n\r\nc) <b>Estudiants.</b> L\'estudiant proposarà per escrit (seguint el model establert a tal efecte, en les dates especificades) un tema o projecte concret al responsable de la menció que està cursant. L\'acceptació no serà immediata, ja que caldrà  valorar que es puguin avaluar les competències previstes al grau (i a la menció) i que la durada i càrrega de treball sigui adient. El responsable de la menció haurà d\'acceptar o declinar la proposta i, en cas de ser acceptada, comunicar a l\'estudiant que es pot buscar tutor. Si l\'estudiant no troba tutor, se n\'hi assignarà un al final del procés d\'assignació..\r\n\r\n\r\nPer més info. consultar:\r\nhttps://guies.uab.cat/guies_docents/public/portal/html/2021/assignatura/106542/ca', 'dades', 106542, 'Enginyeria Informàtica', NULL, 22),
('Sobre les sessions de seguiment.', '<b>- 1a sessió de seguiment (setmana 4):</b> l’estudiant lliura un Informe Inicial\r\n<b>- 2a sessió de seguiment (setmana 9):</b> l’estudiant lliura un Informe de progrés (I)\r\n<b>- 3a sessió de seguiment (setmana 14):</b> l’estudiant lliura un Informe de progrés (II)\r\n<b>- 4a sessió de seguiment (setmana 17):</b> l\'estudiant lliura la proposta d\'Informe final i es fa el tancament del projecte (permís per lliurar).\r\n<b>- 5a sessió de seguiment (setmana 18-19):</b> l\'estudiant lliura la proposta de presentació.\r\n\r\n\r\nPer més info. consultar:\r\nhttps://guies.uab.cat/guies_docents/public/portal/html/2021/assignatura/106542/ca', 'dades', 106542, 'Enginyeria Informàtica', NULL, 23),
('Sobre l\'informe inicial.', '<b>Informe inicial.</b> L\'objectiu principal de l\'informe és el de consignar una <b>proposta detallada del TFG</b>, en què es proposen els objectius a assolir i la <b>metodologia a utilitzar</b> per assolir els fins proposats. Així mateix, s\'han de <b>planificar detalladament</b> els diferents passos a seguir en el desenvolupament del mateix,  tant pel que fa a tasques a realitzar com de forma temporal. Aquesta proposta requereix, per tant, d\'una reflexió prèvia per part de l\'estudiant, que haurà de consultar les fonts d\'informació pertinents, de manera que li sigui possible justificar les seves eleccions i programade treball. Haurà d’incloure, <b>com a mínim:</b> ...\r\n\r\nPer més info. consultar:\r\nhttps://guies.uab.cat/guies_docents/public/portal/html/2021/assignatura/106542/ca', 'dades', 106542, 'Enginyeria Informàtica', NULL, 24);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grau`
--

CREATE TABLE `grau` (
  `nom` varchar(65) NOT NULL,
  `codi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `grau`
--

INSERT INTO `grau` (`nom`, `codi`) VALUES
('Enginyeria Informàtica', 2502441),
('Física', 2500097);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificacio`
--

CREATE TABLE `notificacio` (
  `codi_assignatura` int(11) NOT NULL,
  `descripcio` text NOT NULL,
  `titol` text DEFAULT NULL,
  `data` datetime NOT NULL,
  `id` int(11) NOT NULL,
  `niu_professor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `notificacio`
--

INSERT INTO `notificacio` (`codi_assignatura`, `descripcio`, `titol`, `data`, `id`, `niu_professor`) VALUES
(102760, ' Hello', 'NULL', '2022-02-03 12:57:04', 1, 1456958),
(102760, ' Hello', 'NULL', '2022-02-03 13:00:03', 2, 0),
(102760, ' Hello2', 'NULL', '2022-02-03 13:01:18', 3, 1456958);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `professor`
--

CREATE TABLE `professor` (
  `admin` tinyint(1) NOT NULL,
  `niu_usuari` int(11) NOT NULL,
  `codi_assignatura` int(11) NOT NULL,
  `usuari_telegram` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `professor`
--

INSERT INTO `professor` (`admin`, `niu_usuari`, `codi_assignatura`, `usuari_telegram`) VALUES
(1, 1456958, 102760, 'JoseMiguelRodriguezR_UAB');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seqüencia temari`
--

CREATE TABLE `seqüencia temari` (
  `codi_assignatura` int(11) NOT NULL,
  `titol_tema` varchar(65) NOT NULL,
  `ordre` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `seqüencia temari`
--

INSERT INTO `seqüencia temari` (`codi_assignatura`, `titol_tema`, `ordre`) VALUES
(102760, 'Cicle de Vida del Projecte', 3),
(102760, 'Gestió de la Integració', 8),
(102760, 'Gestió de les Comunicacions', 6),
(102760, 'Gestió de Qualitat', 11),
(102760, 'Gestió del Temps', 4),
(102760, 'Gestió dels Costos i Sostenibilitat', 5),
(102760, 'Gestió dels Recursos Humans i de Gènere', 10),
(102760, 'Gestió dels Riscos', 9),
(102760, 'Gestió d’Abast del Projecte', 7),
(102760, 'Introducció Gestió de Projectes', 1),
(102760, 'La figura del Project Manager', 12),
(102760, 'Selecció de Projectes', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tema`
--

CREATE TABLE `tema` (
  `codi_assignatura` int(11) NOT NULL,
  `titol` varchar(65) NOT NULL,
  `descripcio` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tema`
--

INSERT INTO `tema` (`codi_assignatura`, `titol`, `descripcio`) VALUES
(102760, 'Cicle de Vida del Projecte', NULL),
(102760, 'Gestió de la Integració', NULL),
(102760, 'Gestió de les Comunicacions', NULL),
(102760, 'Gestió de Qualitat', NULL),
(102760, 'Gestió del Temps', NULL),
(102760, 'Gestió dels Costos i Sostenibilitat', NULL),
(102760, 'Gestió dels Recursos Humans i de Gènere', NULL),
(102760, 'Gestió dels Riscos', NULL),
(102760, 'Gestió d’Abast del Projecte', NULL),
(102760, 'Introducció Gestió de Projectes', NULL),
(102760, 'La figura del Project Manager', NULL),
(102760, 'Selecció de Projectes', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuari`
--

CREATE TABLE `usuari` (
  `niu` int(11) NOT NULL,
  `nom` varchar(65) NOT NULL,
  `cognoms` varchar(65) NOT NULL,
  `email` varchar(65) NOT NULL,
  `idioma` varchar(65) NOT NULL DEFAULT 'Català',
  `chat_id` bigint(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuari`
--

INSERT INTO `usuari` (`niu`, `nom`, `cognoms`, `email`, `idioma`, `chat_id`) VALUES
(1111111, 'Test', 'Professor 1', 'Test1@uab.cat', 'Català', 1),
(1456958, 'José Miguel', 'Rodríguez', '1456958@uab.cat', 'Català', 1960663127);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `assignatura`
--
ALTER TABLE `assignatura`
  ADD PRIMARY KEY (`codi`),
  ADD KEY `nom_grau` (`nom_grau`);

--
-- Indices de la tabla `consulta`
--
ALTER TABLE `consulta`
  ADD PRIMARY KEY (`titol_faq`,`niu_estudiant`,`data`),
  ADD KEY `codi_assignatura` (`codi_assignatura`),
  ADD KEY `nom_grau` (`nom_grau`);

--
-- Indices de la tabla `estudiant`
--
ALTER TABLE `estudiant`
  ADD PRIMARY KEY (`codi_assignatura`,`niu_usuari`),
  ADD KEY `niu_usuari` (`niu_usuari`);

--
-- Indices de la tabla `faqs`
--
ALTER TABLE `faqs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `codi_assignatura` (`codi_assignatura`),
  ADD KEY `nom_grau` (`nom_grau`),
  ADD KEY `titol_tema` (`titol_tema`),
  ADD KEY `titol` (`titol`);

--
-- Indices de la tabla `grau`
--
ALTER TABLE `grau`
  ADD PRIMARY KEY (`nom`);

--
-- Indices de la tabla `notificacio`
--
ALTER TABLE `notificacio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `codi_assignatura` (`codi_assignatura`);

--
-- Indices de la tabla `professor`
--
ALTER TABLE `professor`
  ADD PRIMARY KEY (`niu_usuari`,`codi_assignatura`),
  ADD KEY `codi_assignatura` (`codi_assignatura`);

--
-- Indices de la tabla `seqüencia temari`
--
ALTER TABLE `seqüencia temari`
  ADD PRIMARY KEY (`titol_tema`,`ordre`),
  ADD KEY `codi_assignatura` (`codi_assignatura`);

--
-- Indices de la tabla `tema`
--
ALTER TABLE `tema`
  ADD PRIMARY KEY (`titol`),
  ADD KEY `codi_assignatura` (`codi_assignatura`);

--
-- Indices de la tabla `usuari`
--
ALTER TABLE `usuari`
  ADD PRIMARY KEY (`niu`,`chat_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `faqs`
--
ALTER TABLE `faqs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `notificacio`
--
ALTER TABLE `notificacio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `assignatura`
--
ALTER TABLE `assignatura`
  ADD CONSTRAINT `assignatura_ibfk_1` FOREIGN KEY (`nom_grau`) REFERENCES `grau` (`nom`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `consulta`
--
ALTER TABLE `consulta`
  ADD CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`titol_faq`) REFERENCES `faqs` (`titol`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_3` FOREIGN KEY (`codi_assignatura`) REFERENCES `faqs` (`codi_assignatura`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_4` FOREIGN KEY (`nom_grau`) REFERENCES `faqs` (`nom_grau`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `estudiant`
--
ALTER TABLE `estudiant`
  ADD CONSTRAINT `estudiant_ibfk_1` FOREIGN KEY (`niu_usuari`) REFERENCES `usuari` (`niu`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `estudiant_ibfk_2` FOREIGN KEY (`codi_assignatura`) REFERENCES `assignatura` (`codi`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `faqs`
--
ALTER TABLE `faqs`
  ADD CONSTRAINT `faqs_ibfk_1` FOREIGN KEY (`codi_assignatura`) REFERENCES `assignatura` (`codi`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `faqs_ibfk_2` FOREIGN KEY (`nom_grau`) REFERENCES `grau` (`nom`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `faqs_ibfk_3` FOREIGN KEY (`titol_tema`) REFERENCES `tema` (`titol`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `notificacio`
--
ALTER TABLE `notificacio`
  ADD CONSTRAINT `notificacio_ibfk_1` FOREIGN KEY (`codi_assignatura`) REFERENCES `assignatura` (`codi`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `professor`
--
ALTER TABLE `professor`
  ADD CONSTRAINT `professor_ibfk_1` FOREIGN KEY (`niu_usuari`) REFERENCES `usuari` (`niu`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `professor_ibfk_2` FOREIGN KEY (`codi_assignatura`) REFERENCES `assignatura` (`codi`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `seqüencia temari`
--
ALTER TABLE `seqüencia temari`
  ADD CONSTRAINT `seqüencia temari_ibfk_1` FOREIGN KEY (`codi_assignatura`) REFERENCES `assignatura` (`codi`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `seqüencia temari_ibfk_2` FOREIGN KEY (`titol_tema`) REFERENCES `tema` (`titol`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `tema`
--
ALTER TABLE `tema`
  ADD CONSTRAINT `tema_ibfk_1` FOREIGN KEY (`codi_assignatura`) REFERENCES `assignatura` (`codi`) ON DELETE NO ACTION ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
