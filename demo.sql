-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Июн 09 2023 г., 02:26
-- Версия сервера: 8.0.19
-- Версия PHP: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `demo`
--

-- --------------------------------------------------------

--
-- Структура таблицы `administrators`
--

CREATE TABLE `administrators` (
  `admin_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `administrators`
--

INSERT INTO `administrators` (`admin_id`, `name`, `surname`, `lastname`, `email`, `password`) VALUES
(1, 'Никит', 'Макаров', 'Сергеевич', 'nik@mail.ru', '1');

-- --------------------------------------------------------

--
-- Структура таблицы `customers`
--

CREATE TABLE `customers` (
  `customer_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(30) NOT NULL,
  `lastname` varchar(30) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `customers`
--

INSERT INTO `customers` (`customer_id`, `name`, `surname`, `lastname`, `email`, `password`) VALUES
(1, '1', '1', '1', '1', '1'),
(2, 'Никита', 'Макаров', 'Сергеевич', 'nik@mail.ru', '1');

-- --------------------------------------------------------

--
-- Структура таблицы `deliverypoints`
--

CREATE TABLE `deliverypoints` (
  `point_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `deliverypoints`
--

INSERT INTO `deliverypoints` (`point_id`, `name`, `address`) VALUES
(1, 'Озон', 'ясенево'),
(2, 'газон', 'газон');

-- --------------------------------------------------------

--
-- Структура таблицы `managers`
--

CREATE TABLE `managers` (
  `manager_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `managers`
--

INSERT INTO `managers` (`manager_id`, `name`, `surname`, `lastname`, `email`, `password`) VALUES
(1, '1', '1', '1', '1', '1');

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `order_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `cust_id` int DEFAULT NULL,
  `prod_id` int DEFAULT NULL,
  `status_id` int DEFAULT NULL,
  `delivery_point_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`order_id`, `order_date`, `cust_id`, `prod_id`, `status_id`, `delivery_point_id`) VALUES
(10, '2023-06-08 20:12:55', 1, 2, 2, 1),
(11, '2023-06-08 20:12:55', 1, 2, 2, 1),
(13, '2023-06-08 22:54:11', 1, 1, 1, NULL),
(14, '2023-06-08 22:54:11', 1, 2, 1, NULL),
(15, '2023-06-08 23:12:28', 2, 1, 1, NULL),
(16, '2023-06-08 23:12:28', 2, 2, 1, NULL),
(17, '2023-06-08 23:14:13', 2, 2, 2, NULL),
(18, '2023-06-08 23:14:13', 2, 2, 2, NULL),
(19, '2023-06-08 23:22:00', 1, 1, 1, NULL),
(20, '2023-06-08 23:22:00', 1, 2, 1, NULL);

--
-- Триггеры `orders`
--
DELIMITER $$
CREATE TRIGGER `delivery_status` BEFORE INSERT ON `orders` FOR EACH ROW BEGIN
    DECLARE default_status_id INT;
    SELECT status_id INTO default_status_id FROM Statuses WHERE name = 'в процессе';
    SET NEW.status_id = default_status_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `product_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`product_id`, `name`, `price`, `quantity`) VALUES
(1, 'Спортивные костюм ', '200.00', 10),
(2, 'Ботинки ', '100.00', 6);

-- --------------------------------------------------------

--
-- Структура таблицы `statuses`
--

CREATE TABLE `statuses` (
  `status_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `statuses`
--

INSERT INTO `statuses` (`status_id`, `name`) VALUES
(1, 'в процессе'),
(2, 'отправлено ');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `administrators`
--
ALTER TABLE `administrators`
  ADD PRIMARY KEY (`admin_id`);

--
-- Индексы таблицы `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Индексы таблицы `deliverypoints`
--
ALTER TABLE `deliverypoints`
  ADD PRIMARY KEY (`point_id`);

--
-- Индексы таблицы `managers`
--
ALTER TABLE `managers`
  ADD PRIMARY KEY (`manager_id`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `status_id` (`status_id`),
  ADD KEY `delivery_point_id` (`delivery_point_id`),
  ADD KEY `cust_id` (`cust_id`,`prod_id`),
  ADD KEY `prod_id` (`prod_id`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Индексы таблицы `statuses`
--
ALTER TABLE `statuses`
  ADD PRIMARY KEY (`status_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `administrators`
--
ALTER TABLE `administrators`
  MODIFY `admin_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `deliverypoints`
--
ALTER TABLE `deliverypoints`
  MODIFY `point_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `managers`
--
ALTER TABLE `managers`
  MODIFY `manager_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `statuses`
--
ALTER TABLE `statuses`
  MODIFY `status_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`status_id`),
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`delivery_point_id`) REFERENCES `deliverypoints` (`point_id`),
  ADD CONSTRAINT `orders_ibfk_5` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `orders_ibfk_6` FOREIGN KEY (`prod_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
